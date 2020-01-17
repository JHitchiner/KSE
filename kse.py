#!/usr/bin/python3

import sys
import os
import configparser
from robotstxtcheck import *
from whoislookup import *
from subdirfuzzer import *

def setup():
	# Validate IP address/Domain name given
	# Get target IP or Domain name from command arguments then test if it is valid
	try:
		target = sys.argv[1]
		r = os.system('ping -c 1 %s >/dev/null 2>&1' % target)
		if r != 0:
			sys.exit(0)
	except:
		print('[!] No valid IP address or Domain name found, please use format "python3 kse.py 255.255.255.255" or "python3 kse.py www.example.com"')
		sys.exit(0)
	return target

def main():
	# =======================================================
	# KSE v 1.0
	# Kinda Shitty Enumerator, for web applications
	# =======================================================

	# To do list:
	# Finish basic modules
	# Add colour to important findings, eg robots.txt if sitemap is found

	# Validate target IP / domain
	target = setup()

	# Put in some sort of success screen script start here
	print('='*69)
	print('KSE Script v 1.0 by James Hitchiner')
	print('='*69)

	# Scan config file and run the modules that are activated to run
	config = configparser.ConfigParser()
	config.read('config.cfg')
	
	# Completed Modules
	if config['Modules']['robotstxtcheck'] == '1':
		checkRobotsTxt(target)
	if config['Modules']['whoislookup'] == '1':
		whoisLookup(target)
	# Working on modules
	if config['Modules']['subdirfuzzer'] == '1':
		# Pass config values through as ints
		numthreads = int(config['SubDirFuzzer']['numthreads'])
		numlines = int(config['SubDirFuzzer']['numlines'])
		subDirFuzz(target, numthreads, numlines)
	



if __name__ == "__main__":
    main()