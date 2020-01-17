#!/usr/bin/python3

# Using requests lib for this module and urllib for another as wanted to get experience using
# both. Looks weird but its ok :)
import urllib.request

def checkRobotsTxt(target):
	# Gets robots.txt from server if it exists
	print('Robots.txt Checker:')
	print()

	# Check if target starts with http:// or not, needed for a successful request
	if 'http://' not in target:
		target = 'http://' + target

	# Send request to target/robots.txt
	try:
		url = target + '/robots.txt'
		robotstxt = urllib.request.urlopen(url).read().decode('utf-8')
		print(robotstxt)
	except:
		print('[!] No robots.txt found on target...')

	print('='*69)