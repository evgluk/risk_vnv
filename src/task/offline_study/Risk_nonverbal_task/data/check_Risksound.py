#!/usr/bin/env python2

"""
Sound stimuli are currently an area of development in PsychoPy

Previously we used pygame. Now the pyo library is also supported.
On OSX this is an improvement (using coreaudio rather than SDL). 
On windows this should help on systems with good sound cards, 
but this is yet to be confirmed. 
See the demo hardware>testSoundLatency too

"""
#In case we want to do the nonverbal risk task together with the nonverbal delay task, 
#we need a different sound attribute for the probability.
# 1. ramp (going up - 75%, going down - 25%, stays the same - 50%)
# 2. silent blocks (# of blocks - (1-p))

import sys
#import doodle
from psychopy import logging, prefs
logging.console.setLevel(logging.DEBUG)#get messages about the sound lib as it loads

from psychopy import sound,core, visual