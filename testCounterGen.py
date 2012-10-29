#!/usr/bin/python
from pycamac import Server, Af
from time import clock, sleep
from classes import Counter, UrrMover

i = Server().getInterface(0)
crate = i.getCrate(2)
counter = Counter(i.getCrate(3).getModule(8))
#mover = UrrMover(crate.getModule(20), 4, 0)
channel = 0

count = 0
while True:
#	if count > 10:
#		mover.move(1)
	counter.clear(0)
	sleep(1)
	print counter.read(channel)
	count += 1
