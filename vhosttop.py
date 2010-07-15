#!/usr/bin/python

import sys
import argparse
import time
import os


class VhostTail(object):

	def __init__(self,args):
		self.vhostpos = args.vhostpos
		self.updatefrequency = args.updatefrequency
		self.hits = dict()
		self.bits = dict()
		self.codes = dict()
		self.bitcount = 0
		self.count = 0
		self.codecount = 0
		self.starttime = time.time()
		self.lastdisplay = 0
		if not os.path.isfile(args.logfile[0]):
			print 'no such log file!'
			sys.exit(2)
		self.logfile = os.popen('tail -f ' + args.logfile[0] + ' 2>/dev/null')

	def display_list(self):
		self.lastdisplay = time.time()
		print("\x1B[2J")
		print("%-6.2f Mbps" % (self.bitcount / 1024 / 1024 / (time.time() - self.starttime)))
		print("%-6.2f req/s" %  (self.count / (time.time() - self.starttime)))
		print("response codes:")
		print("reqs \t % \t code ")
		for h,c in sorted(self.codes.items(), key=lambda(k,v):(v,k), reverse=True)[0:10]:
			print("%d \t %-6.2f \t %s" % (c,((100.0 * c)/self.codecount),h))

		print ("vhosts:")
		print ("reqs \t kb ")
		for h,c in sorted(self.hits.items(), key=lambda(k,v):(v,k), reverse=True)[0:30]:
			if h not in self.bits:
				self.bits[h] = 0
			print("%d \t %d \t %s" % (c,self.bits[h] / 1024,h))

	def loop_forever(self):

		while 1:
			l = self.logfile.readline()
			try:
				self.count = self.count + 1
				
				vl = l.split(' ')

				#count the hits
				vhost = vl[self.vhostpos]
				if vhost not in self.hits:
					self.hits[vhost] = 1
				else:
					self.hits[vhost] = self.hits[vhost] + 1 

				bl = l.split('"')
				if len(bl) >= 3:
					bl2 = bl[2].split(' ')
					if len(bl2) >= 3:
						#count the bits
						if bl2[2] != '-':
							self.bitcount = self.bitcount + int(bl2[2])
							if vhost not in self.bits:
								self.bits[vhost] = int(bl2[2])
							else:
								self.bits[vhost] = self.bits[vhost] + int(bl2[2])
	
						#count the response codes
						self.codecount = self.codecount + 1
						if bl2[1] not in self.codes:
							self.codes[bl2[1]] = 1
						else:
							self.codes[bl2[1]] = self.codes[bl2[1]] + 1 

				# display the count
				if self.lastdisplay < (time.time() - self.updatefrequency):	
					self.display_list()
			except:
				continue

def main():
	logfile="/var/log/apache2/access_log"
	vhostpos = 5
	updatefrequency = 2

	parser = argparse.ArgumentParser(description='Show "top" like data based on vhost frequency in a log file')
	parser.add_argument('--logfile', nargs=1, type=str, help="path to apache log file", default="/var/log/apache2/access_log")
	parser.add_argument('--vhostpos', nargs=1, type=int, default=0, help="position in logfile of vhost name")
	parser.add_argument('--updatefrequency', nargs=1, type=int, default=2, help="how many seconds between screen updates")
	args = parser.parse_args()

	try:
		vhosttail = VhostTail(args)
		vhosttail.loop_forever()
	except KeyboardInterrupt:
	        print '^C received, shutting down'
		sys.exit(2)

if __name__ == '__main__':
    main()

