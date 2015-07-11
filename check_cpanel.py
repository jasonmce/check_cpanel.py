#!/usr/bin/env python
# This script is a Nagios plugin used to check the status
# of a CPanel license
#
# Author:	Christopher Thunes
# Date:		15 June 2007
# License:	BSD License
#

# %s should be put in place of the ip address
LICENSE_CHECK_URL = "http://verify.cpanel.net/index.cgi?ip=%s"

# Regex string to search for the 'active' keyword
#regexExtractURL = r"<b>[^a-zA-Z0-9\s]*active[^a-zA-Z0-9\s<|\<br\>]*</b>"
regexExtractURL = r"active<br/>"

# Version string
version = "%prog 0.0.1"

from optparse import OptionParser
import urllib
import re
import sys
import socket

def main ( ):
	# Set up the options parser and parse the arguments
	argsparser = OptionParser(usage="%prog [options] -H hostname",version=version)
#	argsparser.add_option("-t", "--timeout", dest="timeout", help="Maximum time to try" )
	argsparser.add_option("-H", "--hostname", dest="host", help="Host to run test on" )
	(options, args) = argsparser.parse_args()

	# Check for the required hostname
	if options.host == None:
		print "-H or --hostname is required"
		sys.exit(3)
		

	numeric = None

	try:
		address = socket.gethostbyname(options.host)
	except socket.gaierror:
		printOutput( 2 )
		

	html = urllib.urlopen( LICENSE_CHECK_URL % (address) )
	regex = re.compile(regexExtractURL)

	if html == None:
		printOutput( 3 )
	
	for line in html.readlines():
		if regex.search(line):
			printOutput( 0 )

	printOutput( 1 )
	 

def printOutput ( numeric ):
	returnValues = ( 0, 2, 2, 2 )

	if numeric == 0:
		print "CPANEL OK: license active"
	elif numeric == 1:
		print "CPANEL CRITICAL: license inactive"
	elif numeric == 2:
		print "CPANEL CRITICAL: could not resolve hostname"
	elif numeric == 3:
		print "CPANEL CRITICAL: could not load license page"

	sys.exit(returnValues[numeric])

	
if __name__ == "__main__":
	main( )
