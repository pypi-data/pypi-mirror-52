#############################################################################
# Author  : Jerome ODIER, Fabian Lambert
#
# Email   : jerome.odier@cern.ch
#           jerome.odier@lpsc.in2p3.fr
#           fabian.lambert@lpsc.in2p3.fr
#
# Version : 1.X.X for pyAMI_nika2 (2013-2019)
#
#############################################################################

try:
	#####################################################################

	import pyAMI.config, pyAMI_nika2.config

	#####################################################################

	pyAMI.config.version = pyAMI_nika2.config.version

	pyAMI.config.bug_report = pyAMI_nika2.config.bug_report

	#####################################################################

	pyAMI.config.endpoint_descrs['nika2'] = {'prot': 'https', 'host': 'ami-nika2-lpsz.in2p3.fr', 'port': '443', 'path': '/AMI/FrontEnd'}

	#####################################################################

except:

	pass

#############################################################################
