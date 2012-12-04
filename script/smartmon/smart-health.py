#!/usr/bin/env python

import sys
import sys
import os
import re
import getopt
import csv

FILENAME = "/var/cache/snmp/smart-health"
DEV_OK = 0
DEV_UNKNOWN = 30
DEV_FAILED = 50

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "")
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(1)
	
	if len(args) > 1:
		usage()
		sys.exit(1)
	
	if len(args) == 0:
		action = 'Health'
	else:
		action=args[0]
	
	if not os.path.exists(FILENAME):
		sys.exit(1)
	
	fin = open(FILENAME, 'rt')
	lines = fin.readlines()
	
	i = 0
	for line in lines:
		line = line.strip()
		dev, result = [ x.strip() for x in line.split(':')]
		if dev == None or result == None:
			continue

		if action == 'Health':
			if result ==  'PASSED':
				print DEV_OK
			elif result == 'FAILED':
				print DEV_FAILDED
			else:
				print DEV_UNKNOWN	
		elif action == 'Index':
			print i
		elif action == 'DeviceDescr':
			print dev
		i = i + 1

	fin.close()


if __name__ == "__main__":
	main()
