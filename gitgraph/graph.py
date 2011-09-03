# -*- coding: UTF-8 -*-
#
# Copyright (C) 2011, Terrence Lee <kill889@gmail.com>
#
# See LICENSE for distribution information

from subprocess import Popen, PIPE

import pkg_resources

import re

from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor, ITemplateProvider, \
							add_stylesheet, add_script
from trac.util import escape, Markup

class GitGraph(Component):
	implements(INavigationContributor, IRequestHandler, ITemplateProvider)
	
	# INavigationContributor methods
	def get_active_navigation_item(self, req):
		return 'gitgraph'

	def get_navigation_items(self, req):
		yield ('mainnav', 'gitgraph', Markup('<a href="%s">Git Graph</a>' % (self.env.href.gitgraph())))

	# IRequestHandler methods
	def match_request(self, req):
		return req.path_info == '/gitgraph'

	def process_request(self, req):
		regexp = re.compile(r'^(.+?)(\s(B\[(.*?)\])? C\[(.+?)\] D\[(.+?)\] A\[(.+?)\] E\[(.+?)\] S\[(.+?)\])?$')
		
		p = Popen('git log --graph --date-order -C -M --all --date=iso --pretty=format:"B[%d] C[%H] D[%ad] A[%an] E[%ae] S[%s]"', stdout=PIPE, shell=True, cwd=self.env.get_repository().gitrepo, close_fds=True)
		p_stdoutdata, p_stderrdata = p.communicate()
		graph_raw_list = unicode(p_stdoutdata, 'utf-8', errors="ignore").split("\n")
		
		graph_list = []
		
		for graph_raw_line in graph_raw_list:
			regexp_result = regexp.search(graph_raw_line)
			
			if not regexp_result:
				continue;
			
			graph_list.append({
					"relation":regexp_result.group(1),
					"branch":regexp_result.group(4),
					"rev":regexp_result.group(5),
					"date":regexp_result.group(6),
					"author":regexp_result.group(7),
					"author_email":regexp_result.group(8),
					"subject":regexp_result.group(9),
				}
			)
		
		data = {'graph_list':graph_list}
		add_stylesheet(req, 'gitgraph/gitgraph.css')
		
		add_script(req, 'gitgraph/jquery.js')
		add_script(req, 'gitgraph/gitgraph.js')
		add_script(req, 'gitgraph/chart.js')
		return 'graph.html', data, None

	# ITemplateProvider methods
	def get_htdocs_dirs(self):
		return [('gitgraph', pkg_resources.resource_filename('gitgraph', 'htdocs'))]

	def get_templates_dirs(self):
		return [pkg_resources.resource_filename('gitgraph', 'templates')]
