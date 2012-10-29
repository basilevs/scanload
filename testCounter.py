#!/usr/bin/python

from pycamac import Server, Af
from time import clock, sleep
from classes import Counter

class Counter1(object):
	def __init__(self, module):
		self.module = module
	def clear(self, ch):
		b = ch * 2 #channel base
		self.module.af(Af(b+1, 9))
		self.module.af(Af(b, 9))
	def read(self, ch):
		b = ch * 2 #channel base
		high = self.module.afr24(Af(b+1, 0))
		low  = self.module.afr24(Af(b, 0))
		rv  = ((high & 0xffff) << 16) + low
		print "high: 0x%06x, low: 0x%06x, result: 0x%x" % (high, low, rv)
		return rv
	def increment(self, ch):
		b = ch * 2 #channel base
		self.module.af(Af(b, 25))
		

i       = Server().getInterface(0)
counter = Counter(i.getCrate(2).getModule(8))
channel = 0
#lock    = i.getCrate(3) 

cycles = -1
start = clock()-0.00001
count = counter.read(channel)-1
#counter.clear(channel)
#for i in range(0, 65000):
#	counter.increment(channel)

while True:
	cycles+=1
	newcount1 = counter.read(channel)
#	print "First read:", cycles, newcount1
	newcount2 = counter.read(channel)
#	print "Second read:", cycles, newcount2, "Speed: ", cycles/(clock() - start)
	if (newcount1 != newcount2):
		raise RuntimeError("%d != %d" % (newcount1, newcount2))
	if (newcount2 < count):
		raise RuntimeError("%d < %d" % (newcount1, count))
	if (newcount2 != count + 1):
		raise RuntimeError("%d != %d + 1" % (newcount1, count))
	counter.increment(channel)
	count = newcount2
	#lock.c(1)
	
	sleep(0.000001)
