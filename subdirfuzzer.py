#!/usr/bin/python3

# Using requests lib for this module and urllib for another as wanted to get experience using
# both. Looks weird but its ok :)
import requests
import queue
import threading

def subDirFuzz(target, numthreads, numlines):
	# Sub Directory fuzzer that will try X amount of common sub directories from config
	# Credits to James Fisher for his directory-list-2.3-medium.txt database
	numthreads = int(numthreads)
	numlines = int(numlines)
	POSITIVE_HTTP_CODES = [200, 204, 301, 302, 307]

	# Set lines to a max of 220545 (as that is the size of the db file - 1)
	if numlines > 220545:
		numlines = 220545
	# Add a / to the end of target if it doesnt have it
	if target[-1] != '/':
		target += '/'

	# First determine if it is https or http
	protocol = 'https://'
	if requests.head(protocol+target).status_code == 404:
		# HTTPS can not be found so is http
		protocol = 'http://'

	print('Sub-Directory Fuzzer v1.0:')
	print('Running with {} threads, scanning {} potential subdirectories on {}...'.format(numthreads, numlines, protocol+target))
	print()

	# Then determine if a random url will result in a 404, if not then scan is useless
	if requests.head(protocol+target+'/wchbhwebh13ef348hgun53f78hvu8in357').status_code != 404:
		print('[!] Random URL resulted in a non-404 page, scanning will not work')
		print('='*69)
		return

	# Bunch of threading stuff with queues that I barely understand lol
	# But basically will read the set amount of lines from the database and load into a queue
	# Then a set amount of threads will go through and test if it exists on the web app

	def checksubdir(address):
		r = requests.head(address)
		if r.status_code in POSITIVE_HTTP_CODES:
			print('Found {} - [{}]'.format(address, r.status_code))

	# This is the thread worker, each worker is a new thread and there are numthreads x workers
	def worker():
		while True:
			address = q.get()
			if address is None:
				break
			checksubdir(address)
			q.task_done()

	# Create a queue for subdirs to be checked, and created numthreads x threads to work it
	q = queue.Queue()
	threads = []
	for i in range(numthreads):
		t = threading.Thread(target=worker)
		t.start()
		threads.append(t)

	database = open('subdirdb.txt', 'r')
	for l in range(0, numlines):
		# Put in the queue the exact address to check eg www.google.com/XXX
		line = database.readline()
		line = line[:-1]
		q.put(protocol+target+line)

	# Blocks until all threads are done
	q.join()

	# Stop workers and destroy threads
	for i in range(numthreads):
		q.put(None)
	for t in threads:
		t.join()

	print('='*69)