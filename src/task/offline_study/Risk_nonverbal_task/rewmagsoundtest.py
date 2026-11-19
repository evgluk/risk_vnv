#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from psychopy import logging, prefs
logging.console.setLevel(logging.DEBUG)  # get messages about the sound lib as it loads

prefs.hardware['audioLib'] = ['pygame'] # sets pygame as the preffered sound library, needed to be able to use .play(loops = ...)

from psychopy import sound, core

#print('rewmag = 2')
#coinsound = sound.Sound('coin_echo5.wav')
#coinsound.play(loops = 1)
#core.wait(4)
#print('rewmag = 5')
#coinsound = sound.Sound('coin_echo5.wav')
#coinsound.play(loops = 4)
#core.wait(4)
#print('rewmag = 8')
#coinsound = sound.Sound('coin_echo5.wav')
#coinsound.play(loops = 7)
#core.wait(4)
#print('rewmag = 12')
#coinsound = sound.Sound('coin_echo5.wav')
#coinsound.play(loops = 11)
#core.wait(4)
#print('rewmag = 15')
#coinsound = sound.Sound('coin_echo5.wav')
#coinsound.play(loops = 14)
#core.wait(4)
#print('rewmag = 18')
#coinsound = sound.Sound('coin_echo5.wav')
#coinsound.play(loops = 17)
#core.wait(4)
#print('all coin sounds played')

import doodle, variables
import functions as fc

var = variables.Variables() # this class defines all the common variables needed in the whole experiment
doo = doodle.Doodle() # a class that does most of the drawing in the experiment
#var.shortmag = 0.5
#var.sndprobmag = 4 # 50 % probability
#var.probdiscounter = 1.2
#fc.instruction(var,doo)
#print('rewmag = 2')
#
#var.shortmag = 2
#fc.instruction(var,doo)
#print('rewmag = 5')
#
#var.shortmag = 4
#fc.instruction(var,doo)
#print('rewmag = 8')
#
#var.shortmag = 6
#fc.instruction(var,doo)
#print('rewmag = 12')
#
#var.shortmag = 8
#fc.instruction(var,doo)
#print('rewmag = 15')
#
#var.shortmag = 10
#fc.instruction(var,doo)
#print('rewmag = 18')
#
#var.shortmag = 0.5
#var.sndprobmag = 16 # 25 % probability
#var.probdiscounter = 1.2
#fc.instruction(var,doo)
#print('rewmag = 2')
#
#var.shortmag = 2
#fc.instruction(var,doo)
#print('rewmag = 5')
#
#var.shortmag = 4
#fc.instruction(var,doo)
#print('rewmag = 8')
#
#var.shortmag = 6
#fc.instruction(var,doo)
#print('rewmag = 12')
#
#var.shortmag = 8
#fc.instruction(var,doo)
#print('rewmag = 15')
#
#var.shortmag = 10
#fc.instruction(var,doo)
#print('rewmag = 18')
#
#var.shortmag = 0.5
#var.sndprobmag = 1 # 75 % probability
#var.probdiscounter = 1.2
#fc.instruction(var,doo)
#print('rewmag = 2')
#
#var.shortmag = 2
#fc.instruction(var,doo)
#print('rewmag = 5')
#
#var.shortmag = 4
#fc.instruction(var,doo)
#print('rewmag = 8')
#
#var.shortmag = 6
#fc.instruction(var,doo)
#print('rewmag = 12')
#
#var.shortmag = 8
#fc.instruction(var,doo)
#print('rewmag = 15')
#
#var.shortmag = 10
#fc.instruction(var,doo)
#print('rewmag = 18')

var.shortmag = 0.3
var.sndprobmag = 1 # 66 % probability
var.probdiscounter = 1.2
fc.instruction(var,doo)
print('rewmag = 2') #new

var.shortmag = 1
fc.instruction(var,doo) # new
print('rewmag = 5')

var.shortmag = 2
fc.instruction(var,doo)
print('rewmag = 8') # 5

var.shortmag = 4
fc.instruction(var,doo)
print('rewmag = 12') # 8

#var.shortmag = 5
#fc.instruction(var,doo)
#print('rewmag = 15') # new
#
#var.shortmag = 6
#fc.instruction(var,doo)
#print('rewmag = 18') # 12
#
#var.shortmag = 8
#fc.instruction(var,doo)
#print('rewmag = 22') # 15
#
#var.shortmag = 9
#fc.instruction(var,doo)
#print('rewmag = 25') # new
#
#var.shortmag = 10
#fc.instruction(var,doo)
#print('rewmag = 28') # 18

core.quit()
