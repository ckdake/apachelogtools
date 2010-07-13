#!/usr/bin/python

from py_spread.spread import Spread
import sys

if (len(sys.argv) != 2):
	print("usage: " + sys.argv[0] + " cluster-name")  
	sys.exit(1)

sp_host = '4803@localhost'
sp = Spread('', sp_host)
sp.connect()
sp.join([sys.argv[1]])
while 1:
	try:
		message = sp.receive()
		sys.stdout.write(message + "\n")
		sys.stdout.flush()
	except (KeyboardInterrupt, SystemExit):
		break
sp.leave()
sp.disconnect()
