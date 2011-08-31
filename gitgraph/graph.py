# -*- coding: UTF-8 -*-
#
# Copyright (C) 2011, Terrence Lee <kill889@gmail.com>
#
# See LICENSE for distribution information

from subprocess import Popen, PIPE

import pkg_resources

from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor,ITemplateProvider
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
		p = Popen('git log --graph --date-order -C -M --all --date=short --pretty=format:"%d <%h> %ad [%an] %s"', stdout=PIPE, shell=True, cwd=self.env.get_repository().gitrepo, close_fds=True)
		p_stdoutdata, p_stderrdata = p.communicate()
		graph_list = unicode(p_stdoutdata, 'utf-8', errors="ignore").split("\n")
		data = {'graph_list':graph_list}
		return 'graph.html', data, None

	# ITemplateProvider methods
	def get_htdocs_dirs(self):
		return []

	def get_templates_dirs(self):
		return [pkg_resources.resource_filename('gitgraph', 'templates')]
