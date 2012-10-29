#!/usr/bin/python

from pycamac import Server, Af, Error
from classes import Counter, UrrMover, KvchMover
from time import sleep
import getopt
from sys import argv, exit
interface = Server().getInterface(0)
crate = interface.getCrate(2)
exposition = 10
steps = 38
stepSize = 1
switchChan = 1

opts, args = getopt.getopt(argv[1:], "ht:c:l:n:")

for o, a in opts:
	if o == "-t":
		exposition = float(a)
	elif o == "-c":
		steps = int(a)
	elif o == "-l":
		stepSize = float(a)
	elif o == "-n":
		switchChan = int(a)
	else:
		print """
-h        - show help
-t number - exposition in seconds
-l number - time of step in seconds
-c number - a number of steps
-n number - a channel of Urr to switch
"""
		exit(1)

counter = Counter(interface.getCrate(2).getModule(8))
#mover = KvchMover(crate.getModule(20))
mover = UrrMover(crate.getModule(20), switchChan, 0)
counterChannels = [0, 1]

print argv[0], "-t", exposition, "-c", steps, "-l", stepSize
counter.clear(0)


for i in range(0, steps):
	mover.move(stepSize)
	for chan in counterChannels:
		counter.clear(chan)
	sleep(exposition)
	values = map(lambda chan: counter.read(chan)/exposition, counterChannels)
	print i, "\t", "\t".join(map(str, values))





