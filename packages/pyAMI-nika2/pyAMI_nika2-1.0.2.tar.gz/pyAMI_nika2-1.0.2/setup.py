#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
# Author  : Jerome ODIER, Jerome FULACHIER, Fabian LAMBERT
#
# Email   : jerome.odier@lpsc.in2p3.fr
#           jerome.fulachier@lpsc.in2p3.fr
#           fabian.lambert@lpsc.in2p3.fr
#
#############################################################################

import os, pyAMI_nika2.config

#############################################################################

if __name__ == '__main__':
	#####################################################################

	try:
		from setuptools import setup

	except ImportError:
		from distutils.core import setup

	#####################################################################

	scripts = [
		'ami_nika2',
	]

	if os.name == 'nt':
		scripts.append('ami_nika2.bat')

	#####################################################################

	setup(
		name = 'pyAMI_nika2',
		version = pyAMI_nika2.config.version,
		author = 'Jerome Odier, Fabian Lambert',
		author_email = 'jerome.odier@cern.ch, fabian.lambert@lpsc.in2p3.fr',
		description = 'Python AMI Metadata Interface (pyAMI) for NIKA 2',
		url = 'http://ami.in2p3.fr/',
		license = 'CeCILL-C',
		packages = ['pyAMI_nika2'],
		package_data = {'': ['README', 'CHANGELOG', '*.txt'], 'pyAMI_nika2': ['*.txt']},
		scripts = scripts,
		install_requires = ['pyAMI_core'],
		platforms = 'any',
		zip_safe = False
	)

#############################################################################
