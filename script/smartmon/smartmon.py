#!/usr/bin/python

import sys
import os
import re
from subprocess import *

FILENAME="/var/cache/snmp/smart-health"
SMARTCTL="/usr/sbin/smartctl"

def _smartctl(dev, param=""):
	p = Popen('%s -a %s %s'%(SMARTCTL, dev, param), shell=True, stdout=PIPE, stderr=PIPE)
	p.wait()
	type = None
	for line in p.stdout.readlines():
		if type == None:
			if re.search('ATA Version is:', line):
				type = 'ATA'
			elif re.search('Transport protocol: SAS', line):
				type = 'SAS'
			if type == None:
				continue
		if type == 'ATA':
			if not re.search('Reallocated_Sector_Ct', line):
				continue
			line = line.strip()
			items = re.split('[ \t]+', line)
			return(int(items[5]), int(items[9]))
		elif type =='SAS':
			if re.search('SMART Health Status:', line):
				if re.search('SMART Health Status: OK', line):
					return (1,0)
				else:
					return (0,1)
	return None

def smartctl(dev, param=""):
	ret = _smartctl(dev, param)
	return ret

def output(fout, dev, threshold, current):
	if current > threshold :
		fout.write('/dev/%s: FAILED\n'%(dev))
	else:
		fout.write('/dev/%s: PASSED\n'%(dev))

def getDevices():
	result = []
	dirs = [ x for x in os.listdir('/dev') if re.match('^[s|h]d.$', x) ]
	dirs.sort()
	for dir in dirs:
		rv = smartctl('/dev/%s'%(dir))
		if rv != None:
			result.append((dir, rv[0], rv[1]))
			continue

		if os.path.exists('/dev/megaraid_sas_ioctl_node'):
			i = 0
			while True:
				rv = smartctl('/dev/%s'%(dir), '-d megaraid,%d'%(i))
				i = i+1
				if rv == None:
					break
				result.append(('%s_%d'%(dir,i), rv[0], rv[1]))
	return result

def main():
	devices = getDevices()
	fout = open(FILENAME, "wt")
	for dev in devices:
		name, threshold, current = dev
		if current > threshold :
			fout.write('%s:%s\n'%(name, 'FAILED'))
		else:
			fout.write('%s:%s\n'%(name, 'PASSED'))
	fout.close()

if __name__ == '__main__':
	main()

