#!/usr/bin/env python

from setuptools import setup

setup(
	name = 'TracGitGraph',
	version = '0.1',
	author = 'Terrence Lee',
	author_email = 'kill889@gmail.com',
	url = 'http://github.com/bluef/trac-git-graph',
	description = 'Git graph plugin for Trac',
	
	license = 'BSD',
	
	install_requires = ['Genshi >= 0.5', 'Trac >= 0.12', 'TracGit >= 0.12.0.5'],
	
	extras_require = {'Babel': 'Babel>= 0.9.5', 'Trac': 'Trac >= 0.12'},
	
	packages = ['gitgraph'],
	package_data = {'gitgraph':['templates/*.html']},
	entry_points = {'trac.plugins':'gitgraph.graph = gitgraph.graph'},
)