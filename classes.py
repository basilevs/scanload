#!/usr/bin/python

from time import sleep
from pycamac import Error, Af

class Counter(object):
	def __init__(self, module):
		assert(module)
		self.module = module
	def clear(self, ch):
		b = ch * 2 #channel base
		try:
			self.module.af(Af(b+1, 9))
		except Error:
			pass
		try:
			self.module.af(Af(b, 9))
		except Error:
			pass
	def read(self, ch):
		b = ch * 2 #channel base
		high = self.module.afr16(Af(b+1, 0))
		low  = self.module.afr16(Af(b, 0))
		rv  = (high << 16) & 0xFF + low
#		print "High:", high, "low:", low, "result:", rv
		return rv
	def increment(self, ch):
		b = ch * 2 #channel base
		self.module.af(Af(b, 25))

class KvchMover(object):
	def __init__(self, module, moveChan = 3, stopChan = 2, backChan = None):
		self._module = module
		self._move = moveChan
		self._back = backChan
		self._stop = stopChan
	def stop(self):
		self._module.afw16(Af(0, 16), self._stop)
	def move(self, seconds):
		try:
			chan = self._move
			if (seconds < 0):
				chan = self._back
			assert(chan)
			self._module.afw16(Af(0, 16), chan)
			sleep(abs(seconds))
		finally:
			self.stop()

class UrrMover(object):
	def __init__(self, module, moveMask = 1, backMask = 0):
		assert((moveMask & backMask) == 0)
		self._module = module
		self._forward = moveMask
		self._backward = backMask
#		print "Forward", self._forward 
	def stop(self):
		self._module.afw16(Af(1,16), self._forward | self._backward)
	def move(self, seconds):
		self.stop()
		chanOn = self._forward
		chanOff = self._backward
		if (seconds < 0):
			chanOn, chanOff = chanOff, chanOn
		try:
#			print "Off", chanOff
#			print "On", chanOn
			self._module.afw16(Af(1,16), chanOff)
			self._module.afw16(Af(2, 16), chanOn)
			sleep(seconds)
		finally:
			self.stop()





