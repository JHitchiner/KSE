#!/usr/bin/python3

import subprocess

def whoisLookup(target):
	# Get whois information about the target site or IP address
	print('WHOIS Lookup for %s:' % target)
	print()

	isDomain = False
	# If target is a domain, remove the 'www.' part and run domain specific whois lookup
	if 'www.' in target:
		target = target[4:]
		isDomain = True

	# Run whois lookup
	try:
		output = subprocess.run(['whois', target], stdout=subprocess.PIPE).stdout.decode('utf-8')
		# Parsing specific to type of whois lookup, domain or IP
		if isDomain:
			# Clear out junk from whois domain lookup, sorry markmonitor.com :(
			junk = output.find('The Registry database contains ONLY .COM, .NET, .EDU domains')
			output = output[junk:]
			junk = (output.find('For more information on WHOIS status codes')) - 1
			output = output[:junk]
			print(output)
		else:
			# Clear out junk from whois IP lookup, sorry ARIN.net :(
			junk = output.find('NetRange:')
			output = output[junk:]
			junk = (output.find('ARIN WHOIS data and services')) - 6
			output = output[:junk]
			print(output)
	except:
		print('[!] Error in whois Lookup')

	print('='*69)