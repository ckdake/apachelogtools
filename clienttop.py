#!/usr/bin/python

import time
from os import popen

class VhostTail(object):

	def __init__(self):
		self.hits = dict()
		self.count = 0
		self.starttime = time.time()
		self.logfile = popen('tail -f /var/log/remote_httpd/access_log 2>/dev/null')

	def display_list(self):
		print("\x1B[2J")
		print("%f2 req/s" %  (self.count / (time.time() - self.starttime)))
		for h,c in sorted(self.hits.items(), key=lambda(k,v):(v,k), reverse=True)[0:25]:
			print("%d \t %s" % (c,h))

	def loop_forever(self):

		while 1:
			lc = self.logfile.readline().split(' ')
			vhost = lc[7]
			self.count = self.count + 1
			if vhost not in self.hits:
				self.hits[vhost] = 1
			else:
				self.hits[vhost] = self.hits[vhost] + 1 
			if self.count % 100 is 0:	
				self.display_list()

def main():
	try:
		vhosttail = VhostTail()
		vhosttail.loop_forever()

	except KeyboardInterrupt:
	        print '^C received, shutting down'

if __name__ == '__main__':
    main()

