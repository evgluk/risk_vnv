# this file contains all the functions needed for all experiments
# !!! Check the correct path for the code repository and correct dtb user first!
# you'll need custom module 'helpers' to import the dtb settings/connection

#-----------------imports---------------------------
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import event,core,gui,visual, sound
import numpy as np  # whole numpy lib is available, prepend 'np.'
import time, datetime, os, gc, random, copy, math
import setup, newPoints, variables,doodle,platform, sys
import SQL_call as sql

# set working path in the computer so that relative packages could work
def setpath():
    if platform.system() == 'Windows': # set path in windows machines
        sys.path.append('/Users/user/repos') # !!! put in correct path first
        sys.path.append('C:\\python27\\Lib\\site-packages')
    elif platform.system() == 'Linux': # set path for linux
        sys.path.append('/home/ladmin/repos')
    else: # set path in mac machines
        user = os.getlogin()
        user = 'evgeniyalukinova'
        print(user)
        if user =='root':
            sys.path.append('<repos location')
            sys.path.append('/usr/local/lib/python3.8/site-packages')
setpath()

#--------------import helper------------------------
import helpers.DBUtilsClass as db
import helpers.net as net
import json

mouse = event.Mouse(setup.mywin)

# SETUP

# connect to database
def dbconnect():
    dbc = db.Connection('manage') # connect to database
    sql.select_user(dbc,'<your user>') # !!! put in correct user first
    return dbc

# ask subject for netid from a window shown on the screen
def get_netid(var,doo,dbc,fN,getName,sub_id):
    expName, extN = os.path.splitext(fN)    
    st = datetime.datetime.now()
    expD = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    host_ip=net.getIP()
    if getName:
        dlg = gui.DlgFromDict(dictionary=var.expInfo, title=expName)
        if dlg.OK == False: 
            core.quit()  # user pressed cancel
        else:
            setup.mywin.winHandle.activate()
        p_net = (var.expInfo['Net ID'])
        print(p_net)
        try:
            p_num = sql.r_subjid(dbc,p_net) # get subject id (p_num) given netid 
        except IndexError: # net_ID is not in the system
            print("net_ID is not in the system!")
            doo.instruction.text = u'net_ID is not in the system'
            doo.instruction.draw()
            setup.mywin.flip()
            core.wait(2)
            core.quit()
    else:
        p_net = sub_id
        p_num = sql.r_subjid(dbc,p_net)
    return p_num, expD, st, expName, host_ip,p_net

# database setup at the beginning of learning stages
def initialSetup(var,dbc):
    # use settings for test_learn (minimum number of forced trials)
    settingsdtb = 'learn_risk'
    try:
        setiddtb = sql.r_settingsid(dbc,settingsdtb)
        varsetdtb = sql.r_varset(dbc,settingsdtb)
        var.forcedTrialNum = varsetdtb['forcedTrialNum']
        var.passThreshold = varsetdtb['passThreshold']
        var.probability = varsetdtb['probability']
        var.mag = varsetdtb['rewmag']
        var.shortmag = varsetdtb['surebet']
        var.highLowProb = [max(var.probability),min(var.probability)]
        var.highLowRew = [max(var.mag),min(var.mag)]
        var.probdiscounter = varsetdtb['pdiscounter']
        var.shufflePos = varsetdtb['poscode']
        var.shuffleRew = varsetdtb['shufflerew']
        var.shuffleProb = varsetdtb['shuffleprob']
        var.shuffleProbDraw = varsetdtb['shuffleprobdraw']
    except IndexError: # settings_ID is not in the system
        print("settings_ID is not in the system!")
    return setiddtb,var

# database setup at the beginning of learning stages (new scheme)
def initialSetup_n(var,dbc):
    # use settings for test_learn (minimum number of forced trials)
    settingsdtb = 'learn_risk2'
    try:
        setiddtb = sql.r_settingsid(dbc,settingsdtb)
        varsetdtb = sql.r_varset(dbc,settingsdtb)
        var.forcedTrialNum = varsetdtb['forcedTrialNum']
        var.passThreshold = varsetdtb['passThreshold']
        var.probability = varsetdtb['probability']
        var.mag = varsetdtb['rewmag']
        var.shortmag = varsetdtb['surebet']
        var.highLowProb = [max(var.probability),min(var.probability)]
        var.highLowRew = [max(var.mag),min(var.mag)]
        var.probdiscounter = varsetdtb['pdiscounter']
        var.shufflePos = varsetdtb['poscode']
        var.shuffleProbDraw = varsetdtb['shuffleprobdraw']
    except IndexError: # settings_ID is not in the system
        print("settings_ID is not in the system!")
    return setiddtb,var

# Adaptive Stages check progress
def checkadapt(var,dbc,doo,p_net):
    try:
        p_num = sql.r_subjid(dbc,p_net) # get subject id (p_num) given netid 
        try:
            adaptstg = sql.r_adaptstg(dbc,p_num)
            adaptsch = sql.r_adaptsch(dbc,p_num)
        except IndexError: # subjid is not in the adapt table
            print("new subject")
            adaptstg = 0
            adaptsch = sql.r_adaptsch0(dbc)
    except IndexError: # net_ID is not in the system
        print("net_ID is not in the system!")
        doo.instruction.text = u'net_ID is not in the system'
        doo.instruction.draw()
        setup.mywin.flip()
        core.wait(2)
        core.quit()
    return adaptstg, adaptsch

# Adapt + NV setup
def exp_setup_n(var,doo,dbc,getName,sub_id,expName,expDate):
    stt = datetime.datetime.now()
    #-----------------data recording-----------------------------------
    if getName:
        dlg = gui.DlgFromDict(dictionary=var.expInfo, title=expName)
        if dlg.OK == False: 
            core.quit()  # user pressed cancel
        else:
            setup.mywin.winHandle.activate()
        p_net = (var.expInfo['Net ID'])
        try:
            p_num = sql.r_subjid(dbc,p_net)
            var.adaptstg, var.schedule = checkadapt(var,dbc,doo,p_net)
        except IndexError: # net_ID is not in the system
            print("net_ID is not in the system!")
            doo.instruction.text = u'net_ID is not in the system'
            doo.instruction.draw()
            setup.mywin.flip()
            core.wait(2)
            core.quit() 
    else:
        p_net = sub_id
        p_num = sql.r_subjid(dbc,p_net)
    if var.allplus1:
        settingsdtb = 'adapt_nv_risk3'
        try:
            setiddtb = sql.r_settingsid(dbc,settingsdtb)
            varsetdtb = sql.r_varset(dbc,settingsdtb)
            var.probability = varsetdtb['probability']
            var.mag = varsetdtb['rewmag']
            var.shortmag = varsetdtb['surebet']
            var.lotterylose = varsetdtb['lotterylose']
        except IndexError: # settings_ID is not in the system
            print("settings_ID is not in the system!")
    else:
        settingsdtb = 'adapt_nv_risk2' # changed from 'adapt_nv_risk'
        try:
            setiddtb = sql.r_settingsid(dbc,settingsdtb)
            varsetdtb = sql.r_varset(dbc,settingsdtb)
            var.probability = varsetdtb['probability']
            var.mag = varsetdtb['rewmag']
            var.shortmag = varsetdtb['surebet']
            var.shufflePosadapt1 = varsetdtb['poscode']
            var.shuffleRewadapt1 = varsetdtb['shufflerew']
            var.shuffleProbadapt1 = varsetdtb['shuffleprob']
            var.shuffleProbDrawadapt1 = varsetdtb['shuffleprobdraw']
        except IndexError: # settings_ID is not in the system
            print("settings_ID is not in the system!")
        
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('No.','stage','Total','hit_No.', 
        'initRT','initVT','fixVT','fixDur','bluePos','yellowPos','decisionRT','choice','yellowRew','rewMag',
        'Dist','probability','rewRT','fix_click','dec_click','rew_click','GetaNum','reward_give'))
    var.dataFile.flush()
    #remove test_ to save real data
    host_ip=net.getIP()
    sql.w_before_mixnon(dbc,p_num, expDate, stt, expName, host_ip, setiddtb) # same for adapt and mixnv session
    var.sessid = sql.r_lastID(dbc)
    return var.sessid,p_num,p_net,setiddtb,host_ip,var,dbc


# Risk_NV_Freeforced Task Setup
def exp_setup_freeforced(var,doo,dbc,getName,sub_id,expName,expDate):
    start_time = datetime.datetime.now()
    #-----------------Getting the Net ID-----------------------------------
    if getName: # Get the subject information
        dlg = gui.DlgFromDict(dictionary=var.expInfo, title=expName)
        if dlg.OK == False: 
            core.quit()  # user pressed cancel
        else:
            #setup.mywin.winHandle.maximize()
            setup.mywin.winHandle.activate()
            #setup.mywin.fullscr = True
            #setup.mywin.winHandle.set_fullscreen(True)
            setup.mywin.flip()
        p_net = (var.expInfo['Net ID']) # p_net now contains the Net ID
        print(p_net)
        #-----------------Getting the subject ID---------------------------
        try:
            p_num = sql.r_subjid(dbc,p_net) # get subject id (p_num) given netid
        except IndexError: # net_ID is not in the system
            print("net_ID is not in the system!")
            doo.instruction.text = 'net_ID is not in the system'
            doo.instruction.draw()
            setup.mywin.flip()
            core.wait(2)
            core.quit() 
    else: # don't get the subject information
        p_net = sub_id
        p_num = sql.r_subjid(dbc,p_net)
    
    #-----------------Setting up database settings-----------------------------------
    settingsdtb = 'freeforced_nv_risk' # fill in once a database setting is available
    try:
        setiddtb = sql.r_settingsid(dbc,settingsdtb)
        varsetdtb = sql.r_varset(dbc,settingsdtb)
        var.probability = varsetdtb['probability']
        var.mag = varsetdtb['rewmag']
        var.shortmag = varsetdtb['surebet']
        var.staticPos = varsetdtb['staticPoscode']
        var.shuffleProb = varsetdtb['shuffleprob']
        var.shuffleStage45ProbDraw = varsetdtb['shuffleStage45ProbDraw']
        var.shuffleFreeRew = varsetdtb['shuffleFreeRew']
        var.shuffleFreeRewExtra = varsetdtb['shuffleFreeRewExtra']
        var.shuffleForcedRew = varsetdtb['shuffleForcedRew']
        var.shuffleFreeProbDraw = varsetdtb['shuffleFreeProbDraw']
        var.shuffleForcedProbDraw = varsetdtb['shuffleForcedProbDraw']
    except IndexError: # settings_ID is not in the system
        print("settings_ID is not in the system!")
    fileName = 'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('No.','stage','Total','hit_No.', 
        'initRT','initVT','fixVT','fixDur','bluePos','yellowPos','decisionRT','choice','yellowRew','rewMag',
        'Dist','probability','rewRT','fix_click','dec_click','rew_click','GetaNum','reward_give'))
    var.dataFile.flush()
    #remove test_ to save real data
    host_ip=net.getIP()
    sql.w_before_learning(dbc,p_num, expDate, start_time, expName, host_ip, setiddtb) # record session info into sessions table, generate a session ID
    var.sessid = sql.r_lastID(dbc) # get the session ID
    return var.sessid,p_num,p_net,setiddtb,host_ip,var,dbc, start_time

# MixNonverbal database and data record setups
def exp_setup(var,doo,dbc,getName,sub_id,expName,expDate):
    stt = datetime.datetime.now()
    #-----------------data recording-----------------------------------
    if getName:
        dlg = gui.DlgFromDict(dictionary=var.expInfo, title=expName)
        if dlg.OK == False: 
            core.quit()  # user pressed cancel
        else:
            setup.mywin.winHandle.activate()
        p_net = (var.expInfo['Net ID'])
        try:
            p_num = sql.r_subjid(dbc,p_net)
        except IndexError: # net_ID is not in the system
            print("net_ID is not in the system!")
            doo.instruction.text = u'net_ID is not in the system'
            doo.instruction.draw()
            setup.mywin.flip()
            core.wait(2)
            core.quit() 
    else:
        p_net = sub_id
        p_num = sql.r_subjid(dbc,p_net)

    settingsdtb = 'nv_risk'
    try:
        setiddtb = sql.r_settingsid(dbc,settingsdtb)
        varsetdtb = sql.r_varset(dbc,settingsdtb)
        var.passThreshold = varsetdtb['passThreshold']
        var.probability = varsetdtb['probability']
        var.mag = varsetdtb['rewmag']
        var.shortmag = varsetdtb['surebet']
        var.highLowProb = [max(var.probability),min(var.probability)]
        var.highLowRew = [max(var.mag),min(var.mag)]
        var.probdiscounter = varsetdtb['pdiscounter']
        var.refresherNum = varsetdtb['refresherNum']
        var.blockTrial = varsetdtb['blockTrial']
        var.shufflePos = varsetdtb['poscode']
        var.shuffleRew = varsetdtb['shufflerew']
        var.shuffleProb = varsetdtb['shuffleprob']
    except IndexError: # settings_ID is not in the system
        print("settings_ID is not in the system!")
        
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('No.','block','Total','hit_No.', 
        'initRT','initVT','fixVT','fixDur','bluePos','yellowPos','decisionRT','choice','yellowRew','rewMag',
        'Dist','probability','decisionVT','rewRT','rewVT','fix_click','dec_click','rew_click','GetaNum','reward_give'))
    var.dataFile.flush()
    #remove test_ to save real data
    host_ip=net.getIP()
    sql.w_before_mixnon(dbc,p_num, expDate, stt, expName, host_ip, setiddtb)
    sessid = sql.r_lastID(dbc)
    return sessid,p_num,p_net,setiddtb,host_ip,var,dbc

# free trials stages setup
def setshuffleListFreeTrials(var,dbc,stg, p_num):
    var.shuffleFreeRew = []
    var.shuffleFreeProbDraw =[]
    if stg == 10: # Add 8 or 12
    # 3 sounds, 30 trials: 10 trials for each rewmag
        for i in range(3):
            var.shuffleFreeProbDraw.extend([1] * 5)
            var.shuffleFreeProbDraw.extend([0] * 5)
        var.shuffleFreeRew.extend([var.mag[0]]*10) #  always uniform
        var.shuffleFreeRew.extend([var.mag[5]]*10)
        # check if participant selected 18 more than 50%
        stg = 9
        var.advancementSQL = 4
        if sql.r_freetrialrew(dbc,var,stg,var.mag[5], p_num) > 0.5:
            # if participant choses 18 more than surebet, we add 8
            print("Add 8")
            var.shuffleFreeRew.extend([var.mag[2]]*10)
            var.new_sound = 8
        else:
            # if participant choses 18 less than surebet, we add 12
            print("Add 12")
            var.shuffleFreeRew.extend([var.mag[3]]*10)
            var.new_sound = 12
        stg = 10
    elif stg == 11: # Add 8 and 12
        # 4 sounds, 30 trials: 6 trials for rewmag 2, and 8 trials for each other rewmags 
        # for the rewmag 2
        if sql.r_which_new_sound_8_12(dbc,var,var.stg,8, p_num) == 8:
            var.new_sound = 8
        else:
            var.new_sound = 12
        var.shuffleFreeProbDraw.extend([1] * 3)
        var.shuffleFreeProbDraw.extend([0] * 3)
        for i in range(3): # for the other rewmags
            var.shuffleFreeProbDraw.extend([1] * 4)
            var.shuffleFreeProbDraw.extend([0] * 4)
        var.shuffleFreeRew.extend([var.mag[0]]*6) 
        var.shuffleFreeRew.extend([var.mag[2]]*8)
        var.shuffleFreeRew.extend([var.mag[3]]*8)
        var.shuffleFreeRew.extend([var.mag[5]]*8)
    elif stg == 12: # add 5 or 15
        # 5 sounds, 30 trials: 6 trials for each rewmag
        for i in range(5):
            var.shuffleFreeProbDraw.extend([1] * 3)
            var.shuffleFreeProbDraw.extend([0] * 3)
        var.shuffleProb.extend([var.prob50] * 30)
        var.shuffleFreeRew.extend([var.mag[0]]*6) #  always uniform
        var.shuffleFreeRew.extend([var.mag[2]]*6)
        var.shuffleFreeRew.extend([var.mag[3]]*6)
        var.shuffleFreeRew.extend([var.mag[5]]*6)
        stg = 11
        var.advancementSQL = 6
        if (sql.r_freetrialrew(dbc,var,stg,var.mag[5], p_num) + sql.r_freetrialrew(dbc,var,stg,var.mag[2], p_num) + sql.r_freetrialrew(dbc,var,stg,var.mag[3], p_num))/3 > 0.5:
            # if participant choses 18 more than surebet, we add 5
            print("Add 5")
            var.shuffleFreeRew.extend([var.mag[1]]*6)
            var.new_sound = 5
        else:
            # if participant choses 18 less than surebet, we add 15
            print("Add 15")
            var.shuffleFreeRew.extend([var.mag[4]]*6)
            var.new_sound = 15
        stg = 12
    elif stg == 13 or stg == 14: # add 5 and 15
        # 6 sounds, 30 trials: 6 trials for each rewmag, leave rewmag 2 away.
        if sql.r_which_new_sound_5_15(dbc,var,var.stg, 5, p_num) == 5:
            var.new_sound = 5
        else:
            var.new_sound = 15
        for i in range(5):
            var.shuffleFreeProbDraw.extend([1] * 3)
            var.shuffleFreeProbDraw.extend([0] * 3)
        var.shuffleFreeRew.extend([var.mag[1]]*6)
        var.shuffleFreeRew.extend([var.mag[2]]*6)
        var.shuffleFreeRew.extend([var.mag[3]]*6)
        var.shuffleFreeRew.extend([var.mag[4]]*6)
        var.shuffleFreeRew.extend([var.mag[5]]*6)

        if var.adv8check == True and var.probIndex == 0: # prob 0.25
            var.shuffleProb = []
            for i in range(5):
                var.shuffleProb.extend([0.25] * 3)
                var.shuffleProb.extend([0.5] * 3)
        elif var.adv8check == True and var.probIndex == 2:
            var.shuffleProb = []
            for i in range(5):
                var.shuffleProb.extend([0.5] * 3)
                var.shuffleProb.extend([0.75] * 3)

        i , j = random.sample(range(30), 2) # select two random indices that are not duplicates. 
        var.shuffleFreeRew[i] = var.mag[0] # change randomly two of the 30 trials to rewmag 2, need at least 2 trials of rewmag 2 in each chunk of 30 trials
        var.shuffleFreeRew[j] = var.mag[0]

    var.rewProbTuple = list(zip(var.shuffleFreeRew,var.shuffleFreeProbDraw, var.shuffleProb))
    random.shuffle(var.rewProbTuple)
    var.shuffleFreeRew,var.shuffleFreeProbDraw, var.shuffleProb = list(zip(*var.rewProbTuple))
    var.shuffleFreeRew = list(var.shuffleFreeRew)
    var.shuffleFreeProbDraw = list(var.shuffleFreeProbDraw)
    var.shuffleProb = list(var.shuffleProb)
    return var.shuffleFreeRew,var.shuffleFreeProbDraw, var.shuffleProb, var


# Adapt stages setup
# this function generates and shuffles position, reward and probability
def setshuffleList(var,dbc,stg):
    limpos = [2,3]
    var.shufflePos = []
    var.shuffleRew = []
    var.shuffleProb = []
    var.shufflePos.extend(limpos*int(var.adaptTrial/2)) # 10 times extend with limited position ids
    if stg == 2 and var.schedule=='A':
        var.shuffleProb.extend([var.prob50] * (var.adaptTrial+1)) # 20+1 times extend with 0.5 value
        var.shuffleRew.extend([var.mag[0]]*7) #  always uniform
        var.shuffleRew.extend([var.mag[2]]*7) 
        var.shuffleRew.extend([var.mag[4]]*7)
    elif stg == 2 and var.schedule=='B':
        var.shuffleRew.extend([var.mag[0]]*int(var.adaptTrial/4))
        var.shuffleRew.extend([var.mag[4]]*int(var.adaptTrial/4))
        var.shuffleRew.extend([var.mag[0]]*int(var.adaptTrial/4))
        var.shuffleRew.extend([var.mag[4]]*int(var.adaptTrial/4))
        var.shuffleProb.extend([var.prob50] * int(var.adaptTrial/2))
        if sql.r_adaptprob1(dbc,var,stg,var.mag[4]) or sql.r_adaptprob1(dbc,var,stg,var.mag[4])==0:
            print (sql.r_adaptprob1(dbc,var,stg,var.mag[4]))
            if sql.r_adaptprob1(dbc,var,stg,var.mag[4])<1:
                print ("add 0.75")
                var.addprob = 0.75
                var.shuffleProb.extend([var.probability[2]] * int(var.adaptTrial/2))
            elif sql.r_adaptprob1(dbc,var,stg,var.mag[4])==1:
                print ("add 0.25")
                var.addprob = 0.25
                var.shuffleProb.extend([var.probability[0]] * int(var.adaptTrial/2))
        else:
            # search previous sessid
            print("checking previous session")
            print(sql.r_adaptprob2(dbc,var,var.mag[4]))
            if sql.r_adaptprob2(dbc,var,var.mag[4])<1:
                print ("add 0.75")
                var.addprob = 0.75
                var.shuffleProb.extend([var.probability[2]] * int(var.adaptTrial/2))
            elif sql.r_adaptprob2(dbc,var,var.mag[4])==1:
                print ("add 0.25")
                var.addprob = 0.25
                var.shuffleProb.extend([var.probability[0]] * int(var.adaptTrial/2))
    elif stg == 3 and var.schedule=='A':
        var.shuffleProb.extend([var.prob50] * var.adaptTrial) # 20 times extend with 0.5 value
        var.shuffleRew.extend([var.mag[0]]*5) # uniform
        var.shuffleRew.extend([var.mag[2]]*5) 
        var.shuffleRew.extend([var.mag[4]]*5)
        if sql.r_adaptprob1(dbc,var,stg,var.mag[2]) or sql.r_adaptprob1(dbc,var,stg,var.mag[2])==0:
            print(sql.r_adaptprob1(dbc,var,stg,var.mag[2]))
            if sql.r_adaptprob1(dbc,var,stg,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*5)
            elif sql.r_adaptprob1(dbc,var,stg,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*5)
        else:
            # search previous sessid
            print("checking previous session")
            print(sql.r_adaptprob2(dbc,var,var.mag[2]))
            if sql.r_adaptprob2(dbc,var,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*5)
            elif sql.r_adaptprob2(dbc,var,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*5)
    elif stg == 3 and var.schedule=='B':
        var.shuffleRew.extend([var.mag[0]]*3)
        var.shuffleRew.extend([var.mag[4]]*4)
        var.shuffleRew.extend([var.mag[0]]*4)
        var.shuffleRew.extend([var.mag[4]]*3)
        var.shuffleRew.extend([var.mag[0]]*3)
        var.shuffleRew.extend([var.mag[4]]*4)
        var.shuffleProb.extend([var.probability[0]]* 7)
        var.shuffleProb.extend([var.probability[1]]* 7)
        var.shuffleProb.extend([var.probability[2]]* 7)
    elif stg == 4 and var.schedule=='A':
        var.shuffleRew.extend(var.mag*4)
        var.shuffleProb.extend([var.prob50] * var.adaptTrial) # 20 times extend with 0.5 value
    elif stg == 4 and var.schedule=='B':
        # always uniform per bundle
        var.shuffleRew.extend([var.mag[0]]*2) 
        var.shuffleRew.extend([var.mag[2]]*2) 
        var.shuffleRew.extend([var.mag[4]]*3)
        var.shuffleRew.extend([var.mag[0]]*2) 
        var.shuffleRew.extend([var.mag[2]]*3) 
        var.shuffleRew.extend([var.mag[4]]*2)
        var.shuffleRew.extend([var.mag[0]]*3) 
        var.shuffleRew.extend([var.mag[2]]*2) 
        var.shuffleRew.extend([var.mag[4]]*2)
        var.shuffleProb.extend([var.probability[0]]* 7)
        var.shuffleProb.extend([var.probability[1]]* 7)
        var.shuffleProb.extend([var.probability[2]]* 7)
    elif stg == 5 and var.schedule=='A':
        var.shuffleRew.extend(var.mag*4)
        var.shuffleProb.extend([var.prob50] * int(var.adaptTrial/2))
        if sql.r_adaptprob1(dbc,var,stg,var.mag[4]) or sql.r_adaptprob1(dbc,var,stg,var.mag[4])==0:
            print (sql.r_adaptprob1(dbc,var,stg,var.mag[4]))
            if sql.r_adaptprob1(dbc,var,stg,var.mag[4])<1:
                print ("add 0.75")
                var.addprob = 0.75
                var.shuffleProb.extend([var.probability[2]] * int(var.adaptTrial/2))
            elif sql.r_adaptprob1(dbc,var,stg,var.mag[4])==1:
                print ("add 0.25")
                var.addprob = 0.25
                var.shuffleProb.extend([var.probability[0]] * int(var.adaptTrial/2))
        else:
            # search previous sessid
            print("checking previous session")
            print(sql.r_adaptprob2(dbc,var,var.mag[4]))
            if sql.r_adaptprob2(dbc,var,var.mag[4])<1:
                print ("add 0.75")
                var.addprob = 0.75
                var.shuffleProb.extend([var.probability[2]] * int(var.adaptTrial/2))
            elif sql.r_adaptprob2(dbc,var,var.mag[4])==1:
                print ("add 0.25")
                var.addprob = 0.25
                var.shuffleProb.extend([var.probability[0]] * int(var.adaptTrial/2))
    elif stg == 5 and var.schedule=='B':
        var.shuffleProb.extend(var.probability * 8)
        var.shuffleRew.extend([var.mag[0]]*6) # uniform in bundles, 4*6=24...-20 = 4 value bundles won't be used
        var.shuffleRew.extend([var.mag[2]]*6) 
        var.shuffleRew.extend([var.mag[4]]*6)
        if sql.r_adaptprob1(dbc,var,stg,var.mag[2]) or sql.r_adaptprob1(dbc,var,stg,var.mag[2])==0:
            print(sql.r_adaptprob1(dbc,var,stg,var.mag[2]))
            if sql.r_adaptprob1(dbc,var,stg,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*6)
            elif sql.r_adaptprob1(dbc,var,stg,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*6)
        else:
            # search previous sessid
            print("checking previous session")
            print(sql.r_adaptprob2(dbc,var,var.mag[2]))
            if sql.r_adaptprob2(dbc,var,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*6)
            elif sql.r_adaptprob2(dbc,var,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*6)
    else: 
        # regular nonverbal but with 2 pokes
        var.shufflePos.extend(limpos*5)
        var.shuffleProb.extend(var.probability*10)
        var.shuffleRew.extend([var.mag[0]]*6)
        var.shuffleRew.extend([var.mag[1]]*6)
        var.shuffleRew.extend([var.mag[2]]*6)
        var.shuffleRew.extend([var.mag[3]]*6)
        var.shuffleRew.extend([var.mag[4]]*6)
    #print var.shufflePos,var.shuffleRew,var.shuffleProb
    random.shuffle(var.shufflePos)
    c = list(zip(var.shuffleRew,var.shuffleProb))
    #random.shuffle(var.shuffleRew)
    #random.shuffle(var.shuffleProb)
    random.shuffle(c)
    var.shuffleRew,var.shuffleProb = zip(*c)
    #print var.shufflePos,var.shuffleRew,var.shuffleProb
    return var.shufflePos,var.shuffleRew,var.shuffleProb,var 

# Adapt stages setup #2 - only 2 probabilities
# this function generates and shuffles position, reward and probability
def setshuffleList2(var,dbc,stg):
    limpos = [2,3]
    var.shufflePos = []
    var.shuffleRew = []
    var.shuffleProb = []
    var.shufflePos.extend(limpos*int(var.adaptTrial/2)) # 10 times extend with limited position ids
    if stg == 2 and var.schedule=='A':
        var.shuffleProb.extend([var.probability[0]] * (var.adaptTrial+1)) # 20+1 times extend with 0.5 value
        var.shuffleRew.extend([var.mag[0]]*7) #  always uniform
        var.shuffleRew.extend([var.mag[2]]*7) 
        var.shuffleRew.extend([var.mag[4]]*7)
    elif stg == 2 and var.schedule=='B':
        var.shuffleRew.extend([var.mag[0]]*int(var.adaptTrial/4))
        var.shuffleRew.extend([var.mag[4]]*int(var.adaptTrial/4))
        var.shuffleRew.extend([var.mag[0]]*int(var.adaptTrial/4))
        var.shuffleRew.extend([var.mag[4]]*int(var.adaptTrial/4))
        var.shuffleProb.extend([var.probability[0]] * int(var.adaptTrial/2))
        var.shuffleProb.extend([var.probability[1]] * int(var.adaptTrial/2))
        print(var.shuffleRew, var.shuffleProb)
    elif stg == 3 and var.schedule=='A':
        var.shuffleProb.extend([var.prob50] * var.adaptTrial) # 20 times extend with 0.5 value
        var.shuffleRew.extend([var.mag[0]]*5) # uniform
        var.shuffleRew.extend([var.mag[2]]*5) 
        var.shuffleRew.extend([var.mag[4]]*5)
        if sql.r_adaptprob1(dbc,var,stg,var.mag[2]) or sql.r_adaptprob1(dbc,var,stg,var.mag[2])==0:
            print(sql.r_adaptprob1(dbc,var,stg,var.mag[2]))
            if sql.r_adaptprob1(dbc,var,stg,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*5)
            elif sql.r_adaptprob1(dbc,var,stg,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*5)
        else:
            # search previous sessid
            print("checking previous session")
            print(sql.r_adaptprob2(dbc,var,var.mag[2]))
            if sql.r_adaptprob2(dbc,var,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*5)
            elif sql.r_adaptprob2(dbc,var,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*5)
    elif stg == 3 and var.schedule=='B':
        # always uniform per bundle
        var.shuffleRew.extend([var.mag[0]]*3) 
        var.shuffleRew.extend([var.mag[2]]*3) 
        var.shuffleRew.extend([var.mag[4]]*4)
        var.shuffleRew.extend([var.mag[0]]*3) 
        var.shuffleRew.extend([var.mag[2]]*4) 
        var.shuffleRew.extend([var.mag[4]]*3)
        var.shuffleProb.extend([var.probability[0]]* int(var.adaptTrial/2))
        var.shuffleProb.extend([var.probability[1]]* int(var.adaptTrial/2))
    elif stg == 4 and var.schedule=='A':
        var.shuffleRew.extend(var.mag*4)
        var.shuffleProb.extend([var.prob50] * var.adaptTrial) # 20 times extend with 0.5 value
    elif stg == 4 and var.schedule=='B':
        var.shuffleProb.extend(var.probability * 10)
        var.shuffleRew.extend([var.mag[0]]*5) # uniform in bundles
        var.shuffleRew.extend([var.mag[2]]*5) 
        var.shuffleRew.extend([var.mag[4]]*5)
        if sql.r_adaptprob1(dbc,var,stg,var.mag[2]) or sql.r_adaptprob1(dbc,var,stg,var.mag[2])==0:
            print(sql.r_adaptprob1(dbc,var,stg,var.mag[2]))
            if sql.r_adaptprob1(dbc,var,stg,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*5)
            elif sql.r_adaptprob1(dbc,var,stg,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*5)
        else:
            # search previous sessid
            print("checking previous session")
            print(sql.r_adaptprob2(dbc,var,var.mag[2]))
            if sql.r_adaptprob2(dbc,var,var.mag[2])<.5:
                print ("add 12")
                var.addrew = 12
                var.shuffleRew.extend([var.mag[3]]*5)
            elif sql.r_adaptprob2(dbc,var,var.mag[2])>=.5:
                print ("add 5")
                var.addrew = 5
                var.shuffleRew.extend([var.mag[1]]*5)
    else: 
        # regular nonverbal but with 2 pokes
        var.shufflePos.extend(limpos*5)
        var.shuffleProb.extend(var.probability*15)
        var.shuffleRew.extend([var.mag[0]]*6)
        var.shuffleRew.extend([var.mag[1]]*6)
        var.shuffleRew.extend([var.mag[2]]*6)
        var.shuffleRew.extend([var.mag[3]]*6)
        var.shuffleRew.extend([var.mag[4]]*6)
    #print var.shufflePos,var.shuffleRew,var.shuffleProb
    random.shuffle(var.shufflePos)
    c = list(zip(var.shuffleRew,var.shuffleProb))
    #random.shuffle(var.shuffleRew)
    #random.shuffle(var.shuffleProb)
    random.shuffle(c)
    if stg<5:
        #determine list subset divider, then sort per subset
        d = random.randint(5, 15)
        #print d
        ca = c[0:d]
        ca.sort(key = lambda x: x[1], reverse=True)
        cb = c[d:]
        cb.sort(key = lambda x: x[1], reverse=True)
        ca.extend(cb)
    else:
        #determine list 2 subset dividers, then sort per subset
        d = [random.randint(5, 15) for p in range(0, 2)]
        #print d
        ca = c[0:d[0]]
        ca.sort(key = lambda x: x[1], reverse=True)
        cb = c[d[0]:(d[0]+d[1])]
        cb.sort(key = lambda x: x[1], reverse=True)
        ca.extend(cb)
        if (d[0]+d[1])<30:
            cc = c[(d[0]+d[1]):]
            cc.sort(key = lambda x: x[1], reverse=True)
            ca.extend(cc)
    #print len(c), len(ca), len(var.shufflePos)
    var.shuffleRew,var.shuffleProb = zip(*ca)
    #print var.shufflePos,var.shuffleRew,var.shuffleProb
    return var.shufflePos,var.shuffleRew,var.shuffleProb,var 

# determine whether to run this adaptive stage again or go to the next adaptive stage
def again_or_next_stage(dbc,var):
    if var.adaptstg == 1:
        var.repeatstage = False
    if var.adaptstg == 2 and var.schedule=='A':
        print(sql.r_adaptprob3(dbc,var,var.mag[2],0),sql.r_adaptprob3(dbc,var,var.mag[4],0)) # 0 for any probability (although just 0.5)
        print(sql.r_adapt1pass(dbc,var)) # check first-order violations
        if sql.r_adaptprob3(dbc,var,var.mag[2],0)<=sql.r_adaptprob3(dbc,var,var.mag[4],0) and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 2 and var.schedule=='B':
        # get added probabilities
        choiceprobadd = sql.r_adaptprob3(dbc,var,var.mag[4],var.addprob)
        choiceprob1 = sql.r_adaptprob3(dbc,var,var.mag[4],var.probability[1])
        print(var.addprob, choiceprobadd, choiceprob1)
        print(sql.r_adapt1pass(dbc,var))
        if var.addprob<var.probability[1] and choiceprobadd<=choiceprob1 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        elif var.addprob>var.probability[1] and choiceprobadd>=choiceprob1 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 3 and var.schedule=='A':
        # get added rewards
        choicerewadd = sql.r_adaptprob3(dbc,var,var.addrew,0)
        choicerew2 = sql.r_adaptprob3(dbc,var,var.mag[2],0)
        choicerew4 = sql.r_adaptprob3(dbc,var,var.mag[4],0)
        print(var.addrew, choicerewadd, choicerew2, choicerew4)
        print(sql.r_adapt1pass(dbc,var))
        if var.addrew<var.mag[2] and choicerewadd<=choicerew2 and choicerew2<=choicerew4 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        elif var.addrew>var.mag[2] and choicerewadd>=choicerew2 and choicerewadd<=choicerew4 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 3 and var.schedule=='B':
        choiceprob0 = sql.r_adaptprob3(dbc,var,var.mag[4],var.probability[0])
        choiceprob1 = sql.r_adaptprob3(dbc,var,var.mag[4],var.probability[1])
        choiceprob2 = sql.r_adaptprob3(dbc,var,var.mag[4],var.probability[2])
        print(choiceprob0,choiceprob1,choiceprob2)
        print(sql.r_adapt1pass(dbc,var))
        if choiceprob0<=choiceprob1 and choiceprob1<=choiceprob2 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 4 and var.schedule=='A':
        choicerew1 = sql.r_adaptprob3(dbc,var,var.mag[1],0)
        choicerew2 = sql.r_adaptprob3(dbc,var,var.mag[2],0)
        choicerew3 = sql.r_adaptprob3(dbc,var,var.mag[3],0)
        choicerew4 = sql.r_adaptprob3(dbc,var,var.mag[4],0)
        print(choicerew1, choicerew2, choicerew3, choicerew4)
        print(sql.r_adapt1pass(dbc,var))
        if choicerew1<=choicerew2 and choicerew2<=choicerew3 and choicerew3<=choicerew4 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 4 and var.schedule=='B':
        print(sql.r_adaptprob3(dbc,var,var.mag[2],0),sql.r_adaptprob3(dbc,var,var.mag[4],0)) # 0 for any probability
        print(sql.r_adapt1pass(dbc,var))
        if sql.r_adaptprob3(dbc,var,var.mag[2],0)<=sql.r_adaptprob3(dbc,var,var.mag[4],0) and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 5 and var.schedule=='A':
        # get added probabilities
        choiceprobadd = sql.r_adaptprob3(dbc,var,0,var.addprob) #0 for any reward
        choiceprob1 = sql.r_adaptprob3(dbc,var,0,var.probability[1])
        print(var.addprob, choiceprobadd, choiceprob1)
        print(sql.r_adapt1pass(dbc,var))
        if var.addprob<var.probability[1] and choiceprobadd<=choiceprob1 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        elif var.addprob>var.probability[1] and choiceprobadd>=choiceprob1 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 5 and var.schedule=='B':
        # get added rewards
        choicerewadd = sql.r_adaptprob3(dbc,var,var.addrew,0) #0 for any probability
        choicerew2 = sql.r_adaptprob3(dbc,var,var.mag[2],0)
        choicerew4 = sql.r_adaptprob3(dbc,var,var.mag[4],0)
        print(var.addrew, choicerewadd, choicerew2, choicerew4)
        print(sql.r_adapt1pass(dbc,var))
        if var.addrew<var.mag[2] and choicerewadd<=choicerew2 and choicerew2<=choicerew4 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        elif var.addrew>var.mag[2] and choicerewadd>=choicerew2 and choicerewadd<=choicerew4 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        else:
            var.repeatstage = True
    else:
        var.repeatstage = False

# determine whether to run this adaptive stage again or go to the next adaptive stage, version #2
def again_or_next_stage2(dbc,var):
    if var.adaptstg == 1:
        var.repeatstage = False
    if var.adaptstg == 2 and var.schedule=='A':
        print(sql.r_adaptprob3(dbc,var,var.mag[2],0),sql.r_adaptprob3(dbc,var,var.mag[4],0)) # 0 for any probability (although just 0.5)
        print(sql.r_adapt1pass(dbc,var)) # check first-order violations
        if sql.r_adaptprob3(dbc,var,var.mag[2],0)<=sql.r_adaptprob3(dbc,var,var.mag[4],0) and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 2 and var.schedule=='B':
        choiceprobadd = sql.r_adaptprob3(dbc,var,var.mag[4],var.probability[1])
        choiceprob1 = sql.r_adaptprob3(dbc,var,var.mag[4],var.probability[0])
        print(choiceprobadd, choiceprob1)
        print(sql.r_adapt1pass(dbc,var))
        if choiceprobadd>=choiceprob1 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 3 and var.schedule=='A':
        # get added rewards
        choicerewadd = sql.r_adaptprob3(dbc,var,var.addrew,0)
        choicerew2 = sql.r_adaptprob3(dbc,var,var.mag[2],0)
        choicerew4 = sql.r_adaptprob3(dbc,var,var.mag[4],0)
        print(var.addrew, choicerewadd, choicerew2, choicerew4)
        print(sql.r_adapt1pass(dbc,var))
        if var.addrew<var.mag[2] and choicerewadd<=choicerew2 and choicerew2<=choicerew4 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        elif var.addrew>var.mag[2] and choicerewadd>=choicerew2 and choicerewadd<=choicerew4 and sql.r_adapt1pass(dbc,var)<=2:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 3 and var.schedule=='B':
        print(sql.r_adaptprob3(dbc,var,var.mag[2],0),sql.r_adaptprob3(dbc,var,var.mag[4],0)) # 0 for any probability
        print(sql.r_adapt1pass(dbc,var))
        if sql.r_adaptprob3(dbc,var,var.mag[2],0)<=sql.r_adaptprob3(dbc,var,var.mag[4],0) and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 4 and var.schedule=='A':
        choicerew1 = sql.r_adaptprob3(dbc,var,var.mag[1],0)
        choicerew2 = sql.r_adaptprob3(dbc,var,var.mag[2],0)
        choicerew3 = sql.r_adaptprob3(dbc,var,var.mag[3],0)
        choicerew4 = sql.r_adaptprob3(dbc,var,var.mag[4],0)
        print(choicerew1, choicerew2, choicerew3, choicerew4)
        print(sql.r_adapt1pass(dbc,var))
        if choicerew1<=choicerew2 and choicerew2<=choicerew3 and choicerew3<=choicerew4 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        else:
            var.repeatstage = True
    elif var.adaptstg == 4 and var.schedule=='B':
        # get added rewards
        choicerewadd = sql.r_adaptprob3(dbc,var,var.addrew,0) #0 for any probability
        choicerew2 = sql.r_adaptprob3(dbc,var,var.mag[2],0)
        choicerew4 = sql.r_adaptprob3(dbc,var,var.mag[4],0)
        print(var.addrew, choicerewadd, choicerew2, choicerew4)
        print(sql.r_adapt1pass(dbc,var))
        if var.addrew<var.mag[2] and choicerewadd<=choicerew2 and choicerew2<=choicerew4 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        elif var.addrew>var.mag[2] and choicerewadd>=choicerew2 and choicerewadd<=choicerew4 and sql.r_adapt1pass(dbc,var)<=1:
            var.repeatstage = False
        else:
            var.repeatstage = True
    else:
        var.repeatstage = False

# new mix nonverbal shuffle list for positions, rewards and probabilities
def setshuffleList_nv(var,dbc):
    # regular nonverbal 
    # set for # trials, dependent on how many were run before
    # there are 6 positions and 6 probabilities - m1; 5 rewards - m2 multiplier
    if var.totalTrialCounter>=30 and var.totalTrialCounter<50:
        m1 = 30
        m2 = 36
    elif var.totalTrialCounter>=50 and var.totalTrialCounter<80:
        m1 = 25
        m2 = 30
    elif var.totalTrialCounter>=80 and var.totalTrialCounter<110:
        m1 = 20
        m2 = 24
    elif var.totalTrialCounter>=110 and var.totalTrialCounter<140:
        m1 = 15
        m2 = 18
    elif var.totalTrialCounter>=140 and var.totalTrialCounter<170:
        m1 = 10
        m2 = 12
    else:
        m1 = 5
        m2 = 6
    limpos = [2,3,4,5,6,7]
    var.shufflePos = []
    var.shuffleRew = []
    var.shuffleProb = []
    var.shufflePos.extend(limpos*m1)
    var.shuffleRew.extend([var.mag[0]]*m2)
    var.shuffleRew.extend([var.mag[1]]*m2)
    var.shuffleRew.extend([var.mag[2]]*m2)
    var.shuffleRew.extend([var.mag[3]]*m2)
    var.shuffleRew.extend([var.mag[4]]*m2)
    print(sql.r_adaptprob_nv(dbc,var))
    if sql.r_adaptprob_nv(dbc,var)>=.5:
        print ("more 0.25")
        adaptprob = [0.25,0.25,0.25,0.5,0.5,0.75]
    else:
        print ("more 0.75")
        adaptprob = [0.25,0.5,0.5,0.75,0.75,0.75]
    var.shuffleProb.extend(adaptprob*m1)
    #print var.shufflePos,var.shuffleRew,var.shuffleProb
    random.shuffle(var.shufflePos)
    c = list(zip(var.shuffleRew,var.shuffleProb))
    #random.shuffle(var.shuffleRew)
    #random.shuffle(var.shuffleProb)
    random.shuffle(c)
    var.shuffleRew,var.shuffleProb = zip(*c)
    #print var.shufflePos,var.shuffleRew,var.shuffleProb, m1, m2
    return var.shufflePos,var.shuffleRew,var.shuffleProb,var 

# new mix nonverbal shuffle list for positions, rewards and probabilities version 2
def setshuffleList_nv2(var,dbc):
    # regular nonverbal 
    # set for # trials, dependent on how many were run before
    # there are 6 positions and 6 probabilities - m1; 5 rewards - m2 multiplier
    # total 150 trials with adapt
    if var.totalTrialCounter>=30 and var.totalTrialCounter<60:
        m1 = 20
        m2 = 24
        divd = 6
    elif var.totalTrialCounter>=60 and var.totalTrialCounter<90:
        m1 = 15
        m2 = 18
        divd = 4
    elif var.totalTrialCounter>=90 and var.totalTrialCounter<120:
        m1 = 10
        m2 = 12
        divd = 3
    else:
        m1 = 5
        m2 = 6
        divd = 1
    limpos = [2,3,4,5,6,7]
    var.shufflePos = []
    var.shuffleRew = []
    var.shuffleProb = []
    var.shufflePos.extend(limpos*m1)
    var.shuffleRew.extend([var.mag[0]]*m2)
    var.shuffleRew.extend([var.mag[1]]*m2)
    var.shuffleRew.extend([var.mag[2]]*m2)
    var.shuffleRew.extend([var.mag[3]]*m2)
    var.shuffleRew.extend([var.mag[4]]*m2)
    adaptprob = [0.5,0.5,0.5,0.75,0.75,0.75]
    var.shuffleProb.extend(adaptprob*m1)
    #print var.shufflePos,var.shuffleRew,var.shuffleProb
    random.shuffle(var.shufflePos)
    c = list(zip(var.shuffleRew,var.shuffleProb))
    #random.shuffle(var.shuffleRew)
    #random.shuffle(var.shuffleProb)
    random.shuffle(c)
    #determine list N subset dividers, then sort per subset
    d = [random.randint(10, 20) for p in range(0, divd)]
    #print d
    lb = 0
    ub = 0
    for dv in range(len(d)):
        if dv==0:
            ca = c[0:d[dv]]
            ca.sort(key = lambda x: x[1])
            ub+=d[dv]
            #print ca
        elif dv>0 & dv<(len(d)-1):
            lb+=d[dv-1]
            ub+=d[dv]
            cb = c[lb:ub]
            cb.sort(key = lambda x: x[1])
            ca.extend(cb)
            #print lb, ub, ca
    if ub<len(c):
        cc = c[ub:]
        ca.extend(cc) # no blocks for the last trials
        #print('last block')
        #print ca
    #print len(c), len(ca), len(var.shufflePos)
    var.shuffleRew,var.shuffleProb = zip(*ca)
    if var.trials10:
        var.shufflePos = [2,3,4,5,6,7,2,3,4,5]
        random.shuffle(var.shufflePos)
        var.shuffleRew = [2, 12, 8, 5, 18, 12, 2, 8, 18, 5]
        var.shuffleProb = [0.5, 0.5, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 0.75, 0.75]
        var.nvTrial = 10
    print(var.shufflePos,var.shuffleRew,var.shuffleProb, m1, m2, divd)
    return var.shufflePos,var.shuffleRew,var.shuffleProb,var 

# MixNonverbal experiment setups
# this function generates the trial numbers for each block and the overall structure of this session
def nonverbalSetup(totalTrialNumber,probList):
    blockInfoList = []
    blockTotal = totalTrialNumber * 0.2
    for prob in probList:
        blockInfoList.append([prob])
    for setNum in range(len(blockInfoList)):
        if setNum == len(blockInfoList)-1:
            totalBeforeLast= 0
            for i in range(setNum):
                totalBeforeLast+=blockInfoList[i][1]
            trialNum = int(totalTrialNumber-totalBeforeLast)
            blockInfoList[setNum].append(trialNum)
        elif setNum < len(blockInfoList)-1:
            trialNum = random.randint(blockTotal-2,blockTotal+2)
            blockInfoList[setNum].append(trialNum)
    return blockInfoList

# this function generates the trial numbers for each block and the overall structure of this session predetermined 
# and same for all participants
def nonverbalpredetSetup(totalTrialNumber,probList):
    blockInfoList = []
    blockTotal = totalTrialNumber * 0.2
    for prob in probList:
        blockInfoList.append([prob])
    for setNum in range(len(blockInfoList)):
        if setNum == len(blockInfoList)-1:
            totalBeforeLast= 0
            for i in range(setNum):
                totalBeforeLast+=blockInfoList[i][1]
            trialNum = int(totalTrialNumber-totalBeforeLast)
            blockInfoList[setNum].append(trialNum)
        elif setNum < len(blockInfoList)-1:
            blockInfoList[setNum].append(blockTotal)
    return blockInfoList

# DRAWING

# draw all the circles 
def circles(var,doo): # draws all the circles
    for i in range(len(var.elX)): # loop over all circles
        doo.circle.fillColor = var.gray2 # set circle color to be gray
        if i==0:
            doo.circle.size = var.circle_reward
        else:
            doo.circle.size = var.circle_fullSize
        doo.circle.pos = ([var.elX[i],var.elY[i]]) # set individual circle positions
        doo.circle.draw() # draw each circle

#  draw all the circles in black during violation
def wrongCircles(var,doo):
    for i in range(len(var.elX)): # loop over all circles
        doo.circle.fillColor = var.black # set circle color to be black
        doo.circle.pos = ([var.elX[i],var.elY[i]]) # set individual circle positions
        if i==0:
            doo.circle.size = var.circle_reward
        else:
            doo.circle.size = var.circle_fullSize
        doo.circle.draw() # draw each circle

#this function draws the initiation circle
def initCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.initPosCode],var.elY[var.initPosCode]])
    doo.circle.fillColor = var.white
    doo.circle.size = var.circle_fullSize
    doo.circle.draw()
    doo.circle.fillColor=var.gray2
    doo.circle.size = var.circle_innerSize
    circleInitIn = doo.circle
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize
    return circleInitIn

#this function colors the initiation circle in white for fixation
def fixCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.initPosCode],var.elY[var.initPosCode]])
    doo.circle.fillColor=var.white
    doo.circle.size = var.circle_fullSize+2
    doo.circle.draw()
    circleFixIn = doo.circle
    doo.circle.size=var.circle_fullSize
    return circleFixIn

#this function draws the sure bet blue circle
def blueCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.bluePosCode],var.elY[var.bluePosCode]])
    doo.circle.fillColor = var.cyan
    doo.circle.size=var.circle_fullSize-1
    circleBlue = doo.circle
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize
    return circleBlue

#this function draws the sure bet yellow circle
def yellowCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.yellowPosCode],var.elY[var.yellowPosCode]])
    doo.circle.fillColor = var.yellow
    doo.circle.size=var.circle_fullSize-1
    circleYellow = doo.circle
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize
    return circleYellow

# draw the reward circle
def rewardCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.rewPosCode],var.elY[var.rewPosCode]]) # set reward port position
    doo.circle.size = var.circle_reward # set the size of the outer reward circle
    doo.circle.fillColor = var.purple # set the corlor of the outer reward circle
    doo.circle.draw() # draw the outer reward circle
    doo.circle.size = var.circle_fullSize # set the size of the inner reward circle
    doo.circle.fillColor = var.white # set the corlor of the inner reward circle
    circleRewIn = doo.circle # make the inner circle a variable
    doo.circle.draw() # draw the inner reward circle
    doo.circle.size = var.circle_reward # set the circle size back to full size
    return circleRewIn # return the inner circle object for later use

# draw the cross - zero reward
def redCross(var,doo):
    doo.cross.text = u'+' # rotated plus will be a cross
    doo.cross.pos=np.array([var.elX[var.rewPosCode]+5,var.elY[var.rewPosCode]+5]) # set the position of the cross
    doo.cross.draw() # draw the cross

#this functions draws everyting at the beginning of each trial while waiting for poke in initCircle
def draw_initCircle(var,doo,myPoints):
    circles(var,doo)
    initCircle(var,doo)
    mouse.clickReset()
    event.Mouse(win=setup.mywin)  
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.state = 'wait_for_initPort_poke'
    return var,doo,myPoints

#this function draws the fixation circle 
def draw_fixCircle(var,doo,myPoints):
    var.timeStart2 = time.time()
    timeStartFix = time.time()
    timeEndFix = time.time()
    circles(var,doo)
    fixCircle(var,doo)
    mouse.clickReset()
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    beingPressed = False
    while timeEndFix-timeStartFix <= var.fixDur:
        mouse.getPressed()
        if mouse.mouseMoved(distance=var.radius, reset=(var.elX[var.initPosCode],var.elY[var.initPosCode])):
            timeEnd = time.time()
            var.wait_for_fixViolation_poke_time = timeEnd-timeStartFix
            var.fixWrong = True
            var.state = 'violationSound'
            return var,doo,myPoints
        elif mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                fix_click_time = timeEnd-timeStartFix
                var.fixation_clicks.append(format(str(fix_click_time),'')+'-'+str(var.initPosCode))
            beingPressed = True
        timeEndFix = time.time()
    var.learnedFix +=1
    if var.stg == 2:
        var.goodPokesInARoll += 1
    if var.stg == 2:
        var.state = 'draw_rewardCircle'
    elif var.stg == 3:
        var.state = 'draw_blueCircle'
    elif var.stg >= 4:
        var.state = 'RR_Sound'
    return var,doo,myPoints

#this function draws the sure bet blue circle and everything else
def draw_blueCircle(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    mouse.clickReset()
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.state = 'wait_for_bluePort_poke'
    return var,doo,myPoints

#this function generates and plays the sound of getting a risky reward (RR)
def RR_Sound(var,doo,myPoints):
    toneMag=doo.toneMag(var.hitmag)
    toneMag.play()
    RRTimeStart = time.time()
    RRTimeEnd = time.time()
    beingPressed=False
    while RRTimeEnd-RRTimeStart < var.RRSoundDur:
        mouse.getPressed()
        if mouse.mouseMoved(distance=var.radius, reset=(var.elX[var.initPosCode],var.elY[var.initPosCode])):
            timeEnd = time.time()
            var.wait_for_fixViolation_poke_time = timeEnd-var.timeStart2
            var.fixWrong = True
            toneMag.stop()
            var.state = 'violationSound'
            return var,doo,myPoints
        elif mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                fix_click_time = timeEnd-var.timeStart2
                var.fixation_clicks.append(format(str(fix_click_time),'')+'-'+str(var.initPosCode))
            beingPressed = True
        elif not mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            beingPressed = False
        RRTimeEnd = time.time()
    if var.stg == 4:
        var.state = 'draw_yellowCircle'
    elif var.stg >= 5:
        var.state = 'riskySound'
    return var,doo,myPoints

#this function plays the probability sound 
def riskySound(var,doo,myPoints):
    toneProb=doo.toneProb(var.hitmag,var.sndprobmag, var.probdiscounter)
    toneProb.play()
    probTimeStart = time.time()
    probTimeEnd = time.time()
    beingPressed=False
    while probTimeEnd-probTimeStart < var.probSoundDur:
        mouse.getPressed()
        if mouse.mouseMoved(distance=var.radius, reset=(var.elX[var.initPosCode],var.elY[var.initPosCode])):
            timeEnd = time.time()
            var.wait_for_fixViolation_poke_time = timeEnd-var.timeStart2
            var.fixWrong = True
            toneProb.stop()
            var.state = 'violationSound'
            return var,doo,myPoints
        elif mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                fix_click_time = timeEnd-var.timeStart2
                var.fixation_clicks.append(format(str(fix_click_time),'')+'-'+str(var.initPosCode))
            beingPressed = True
        elif not mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            beingPressed = False
        probTimeEnd = time.time()
    toneProb.stop()
    if (var.stg == 6 or var.stg == 7 or var.stg == 8 or var.stg == 9 or var.stg == 10 or var.stg == 11 or var.stg == 12 or var.stg == 13 or var.stg == 14) and var.forced == 0:
        var.state = 'draw_stimCircles'
    else:
        var.state = 'draw_yellowCircle'
    return var,doo,myPoints

# probability sound instruction before the experiment
def instruction(var,doo):
    event.Mouse(visible=False)
    var.RRSoundDur = 2
    toneProb=doo.toneProb(var.shortmag,var.sndprobmag, var.probdiscounter)
    setup.mywin.flip()
    core.wait(1)
    toneProb.play()
    core.wait(2)
    var.RRSoundDur = 0.48
    event.Mouse(visible=True)
    return var

def draw_yellowCircle(var,doo,myPoints):
    circles(var,doo)
    yellowCircle(var,doo)
    mouse.clickReset()
    myPoints.totalUpdate(var.points)
    setup.mywin.flip(clearBuffer=True)
    var.state = 'wait_for_yellowPort_poke'
    return var,doo,myPoints

#this function draws the stimulus circles in MixNonverbal task
def draw_stimCircles(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    yellowCircle(var,doo)
    mouse.clickReset()
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.state = 'wait_for_choice_poke'
    return var,doo,myPoints

# draw everyting at the beginning of each trial while waiting for the choice
def draw_rewardCircle(var,doo,myPoints):
    circles(var,doo) # draw all the basic circles
    rewardCircle(var,doo) # draw the reward circle
    if var.stg == 0: # reset mouse position at the beginning of the each trial if in stage 0
        event.Mouse(win=setup.mywin) 
    mouse.clickReset()
    myPoints.totalUpdate(var.points) # draw the total points earned
    setup.mywin.flip() # show all the drawings
    var.state = 'wait_for_rewardPort_poke' # return the name of next state
    return var,doo,myPoints

#this function is checking whether the mouse clicks within init port
def wait_for_initPort_poke(var,doo,myPoints):
    reDrawInit(var,doo,myPoints)
    var.timeStart1 = time.time()
    while True:
        if mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            timeEnd1 = time.time()
            var.wait_for_init_poke_time = timeEnd1-var.timeStart1
            #var.trialsCorrect += 1 
            if var.wait_for_init_poke_time <= var.standardRT_get_reward:
                var.learnedInitPoke += 1
                if var.stg == 1:
                    var.goodPokesInARoll += 1
            else:
                if var.stg < 4:
                    var.goodPokesInARoll = 0
            if var.stg == 1:
                var.state = 'draw_rewardCircle'
            elif var.stg >= 2:
                var.state = 'draw_fixCircle'
                
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(initCircle(var,doo))==False:
            timeEnd2 = time.time()
            var.wait_for_initViolation_poke_time = timeEnd2-var.timeStart1
            var.initWrong = True
            var.state = 'violationSound'
            return var,doo,myPoints

#this function is checking whether the mouse clicks within blue port
#def wait_for_bluePort_poke(var,doo,myPoints):
#    reDrawBlue(var,doo,myPoints)
#    var.timeStart3 = time.time()
#    beingPressed = False
#    #while True:
#        #if sum(mouse.getPressed())==0:
#            #break
#    while True:
#        if mouse.isPressedIn(blueCircle(var,doo),buttons=[0]):
#            var.blueWrong = False
#            timeEnd = time.time()
#            var.wait_for_blue_poke_time = timeEnd-var.timeStart3
#            if var.wait_for_blue_poke_time <= var.standardRT_get_reward:
#                var.learnedBluePoke += 1
#                if var.stg == 3:
#                    var.goodPokesInARoll += 1
#            else:
#                var.goodPokesInARoll = 0
#            var.state = 'draw_rewardCircle'
#            return var,doo,myPoints
#        elif mouse.getPressed()[0]>0 and not mouse.isPressedIn(rewardCircle(var,doo),buttons=[0]): # button 0 is pressed
#            if not beingPressed: # initial detection
#                timeEnd = time.time()
#                var.wait_for_blueViolation_poke_time = timeEnd-var.timeStart3
#                mouse_loc = mouse.getPos()
#                var.decision_clicks.append(str(var.wait_for_blueViolation_poke_time)+'-'+str(mouse_loc))
#                beingPressed = True
#            beingPressed = False
#        # Wait until all buttons are released
#        elif sum(mouse.getPressed())==0:
#            beingPressed = False
#        while any(mouse.getPressed()):
#            pass
#        #elif mouse.getPressed()[0]>0 and mouse.isPressedIn(blueCircle(var,doo))==False:
#            #timeEnd = time.time()
#            #var.wait_for_blueViolation_poke_time = timeEnd-var.timeStart3
#            #var.blueWrong = True
#            #var.state = 'wait_for_bluePort_poke' #changed from 'violationSound'
#        return var,doo,myPoints

def wait_for_bluePort_poke(var,doo,myPoints):
    reDrawBlue(var,doo,myPoints)
    var.timeStart3 = time.time()
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True:
        if mouse.isPressedIn(blueCircle(var,doo),buttons=[0]):
            var.blueWrong = False
            timeEnd = time.time()
            var.wait_for_blue_poke_time = timeEnd-var.timeStart3
            if var.wait_for_blue_poke_time <= var.standardRT_get_reward:
                var.learnedBluePoke += 1
                if var.stg == 3:
                    var.goodPokesInARoll += 1
            else:
                var.goodPokesInARoll = 0
            var.state = 'draw_rewardCircle'
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(blueCircle(var,doo))==False:
            timeEnd = time.time()
            var.wait_for_blueViolation_poke_time = timeEnd-var.timeStart3
            #var.blueWrong = True
            #var.state = 'wait_for_bluePort_poke' #changed from 'violationSound'
            return var,doo,myPoints


#this function is checking whether the mouse clicks within yellow port
#def wait_for_yellowPort_poke(var,doo,myPoints):
#    reDrawYellow(var,doo,myPoints)
#    var.timeStart3 = time.time()
#    beingPressed = False
#    #while True:
#        #if sum(mouse.getPressed())==0:
#            #break
#    while True:
#        if mouse.isPressedIn(yellowCircle(var,doo),buttons=[0]):
#            var.yellowWrong = False
#            timeEnd = time.time()
#            var.wait_for_yellow_poke_time = timeEnd-var.timeStart3
#            if var.wait_for_yellow_poke_time <= var.standardRT_get_reward:
#                var.learnedYellowPoke += 1
#                if var.stg == 4:
#                    if not var.forcedTrial:
#                        var.goodPokesInARoll += 1
#                    else:
#                        var.goodPokesInARoll = 0
#            if var.stg==4:
#                var.state = 'draw_rewardCircle'
#            if var.stg==5:
#                var.GetaNum = random.random() # get a random number between 0 and 1
#                if var.GetaNum <= var.probmag: #decide whether to give reward based on given probability
#                    var.reward_give = True
#                    var.state =  'draw_rewardCircle' # return the name of next state
#                else:
#                    var.reward_give = False
#                    var.rewardGot += 1 # plus 1 in rewardGot
#                    var.wait_for_reward_poke_time = 0 
#                    var.learnedRewPoke += 1 # plus 1 in learnedRewPoke if the click was quick enough (assume the subject learned)
#                    var.goodPokesInARoll += 1 
#                    mouse.clickReset() # reset mouse click
#                    circles(var,doo) # draw all the basic circles 
#                    myPoints.totalUpdate(var.points) # draw the total coins earned (new earned added)
#                    setup.mywin.flip(clearBuffer=True)
#                    var.state = 'none'
#            return var,doo,myPoints
#        elif mouse.getPressed()[0]>0 and not mouse.isPressedIn(rewardCircle(var,doo),buttons=[0]): # button 0 is pressed
#            if not beingPressed: # initial detection
#                timeEnd = time.time()
#                var.wait_for_yellowViolation_poke_time = timeEnd-var.timeStart3
#                mouse_loc = mouse.getPos()
#                var.decision_clicks.append(str(var.wait_for_yellowViolation_poke_time)+'-'+str(mouse_loc))
#                beingPressed = True
#            beingPressed = False
#        # Wait until all buttons are released
#        elif sum(mouse.getPressed())==0:
#            beingPressed = False
#        while any(mouse.getPressed()):
#            pass
#        #elif mouse.getPressed()[0]>0 and mouse.isPressedIn(yellowCircle(var,doo))==False:
#            #timeEnd = time.time()
#            #var.wait_for_yellowViolation_poke_time = timeEnd-var.timeStart3
#            #var.yellowWrong = True
#            #var.state = 'wait_for_yellowPort_poke' #changed from 'violationSound'
#        return var,doo,myPoints

def wait_for_yellowPort_poke(var,doo,myPoints):
    reDrawYellow(var,doo,myPoints)
    var.timeStart3 = time.time()
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True:
        if mouse.isPressedIn(yellowCircle(var,doo),buttons=[0]):
            var.yellowWrong = False
            timeEnd = time.time()
            var.wait_for_yellow_poke_time = timeEnd-var.timeStart3
            if var.wait_for_yellow_poke_time <= var.standardRT_get_reward:
                var.learnedYellowPoke += 1
                if var.stg == 4:
                    if not var.forcedTrial:
                        var.goodPokesInARoll += 1
                    else:
                        var.goodPokesInARoll = 0
            if var.stg==4:
                var.state = 'draw_rewardCircle'
            if var.stg==5 or var.stg==45:
                #var.GetaNum = random.random() # get a random number between 0 and 1
                if len(var.shuffleStage45ProbDraw) > 0 and var.advancement == 0:
                    var.GetaNum = var.shuffleStage45ProbDraw[var.rewardGot] # predetermined list for stage 45
                elif var.forced == 1 and var.adv8check == False: # is a forced trial
                    var.GetaNum = var.shuffleForcedProbDraw[var.rewForcedIndex]
                elif var.forced == 1 and var.adv8check == True: # special for advancement 8
                    var.GetaNum = random.random()
                    print("var.GetaNum: " + str(var.GetaNum))
                    print("var.GetaNum <= var.probmag: " + str(var.GetaNum <= var.probmag))
                else:
                    var.GetaNum = var.shuffleForcedProbDraw[var.rewardGot] # predetermined random value from settings (0 or 1)
                if var.GetaNum <= var.probmag: #decide whether to give reward based on given probability
                    print("give reward")
                    var.reward_give = True
                    var.state =  'draw_rewardCircle' # return the name of next state
                else:
                    print("give no reward")
                    var.reward_give = False
                    var.rewardGot += 1 # plus 1 in rewardGot
                    var.wait_for_reward_poke_time = 0 
                    var.learnedRewPoke += 1 # plus 1 in learnedRewPoke if the click was quick enough (assume the subject learned)
                    var.goodPokesInARoll += 1 
                    mouse.clickReset() # reset mouse click
                    circles(var,doo) # draw all the basic circles 
                    myPoints.totalUpdate(var.points) # draw the total coins earned (new earned added)
                    setup.mywin.flip()
                    var.state = 'none'
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(yellowCircle(var,doo))==False:
            timeEnd = time.time()
            var.wait_for_yellowViolation_poke_time = timeEnd-var.timeStart3
            #var.yellowWrong = True
            #var.state = 'wait_for_yellowPort_poke' #changed from 'violationSound'
            return var,doo,myPoints


#this function is checking whether the mouse clicks within choice ports
#def wait_for_choice_poke(var,doo,myPoints):
#    reDrawStim(var,doo,myPoints)
#    var.timeStart3 = time.time()
#    beingPressed = False
#    #while True:
#        #if sum(mouse.getPressed())==0:
#            #break
#    while True:
#        if mouse.isPressedIn(blueCircle(var,doo),buttons=[0]):
#            var.choiceWrong = False
#            var.yrewmag = var.rewmag
#            var.rewmag = var.shortmag
#            #print var.yrewmag, var.rewmag
#            var.choice = 'b'
#            getInitStimDis_exp(var)
#            timeEnd = time.time()
#            var.wait_for_choice_poke_time = timeEnd-var.timeStart3 # changed from blue
#            if var.wait_for_choice_poke_time <= var.standardRT_get_reward:
#                var.learnedChoicePoke += 1
#                var.goodPokesInARoll += 1
#            var.GetaNum = []
#            var.reward_give = []
#            var.state = 'draw_rewardCircle'
#            return var,doo,myPoints
#        elif mouse.isPressedIn(yellowCircle(var,doo),buttons=[0]):
#            var.choiceWrong = False
#            var.yrewmag = var.rewmag
#            #print var.yrewmag, var.rewmag
#            var.choice = 'y'
#            getInitStimDis_exp(var)
#            timeEnd = time.time()
#            var.wait_for_choice_poke_time = timeEnd-var.timeStart3
#            if var.wait_for_choice_poke_time <= var.standardRT_get_reward: # changed from yellow
#                var.learnedChoicePoke += 1
#                var.goodPokesInARoll += 1
#            var.GetaNum = random.random() # get a random number between 0 and 1
#            if var.GetaNum <= var.probmag: #decide whether to give reward based on given probability
#                var.reward_give = True
#                var.state =  'draw_rewardCircle' # return the name of next state
#            else:
#                var.reward_give = False
#                var.state = 'none'
#                var.rewardGot += 1 # plus 1 in rewardGot
#                var.wait_for_reward_poke_time = 0 
#                var.learnedRewPoke += 1 # plus 1 in learnedRewPoke if the click was quick enough (assume the subject learned)
#                var.goodPokesInARoll += 1 
#                var.rewmag = 0
#                mouse.clickReset() # reset mouse click
#                circles(var,doo) # draw all the basic circles 
#                myPoints.totalUpdate(var.points) # draw the total coins earned (new earned added)
#                setup.mywin.flip(clearBuffer=True)
#            return var,doo,myPoints
#        elif mouse.getPressed()[0]>0 and not mouse.isPressedIn(rewardCircle(var,doo),buttons=[0]): # button 0 is pressed
#            if not beingPressed: # initial detection
#                timeEnd = time.time()
#                var.wait_for_choiceViolation_poke_time = timeEnd-var.timeStart3
#                mouse_loc = mouse.getPos()
#                var.decision_clicks.append(str(var.wait_for_choiceViolation_poke_time)+'-'+str(mouse_loc))
#                beingPressed = True
#            beingPressed = False
#        # Wait until all buttons are released
#        elif sum(mouse.getPressed())==0:
#            beingPressed = False
#        while any(mouse.getPressed()):
#            pass
#        #elif mouse.getPressed()[0]>0 and mouse.isPressedIn(blueCircle(var,doo))==False and mouse.isPressedIn(yellowCircle(var,doo))==False:
#            #timeEnd = time.time()
#            #var.wait_for_choiceViolation_poke_time = timeEnd-var.timeStart3
#            #var.choiceWrong = True
#            #var.state = 'wait_for_choice_poke' #changed from 'violationSound'
#        return var,doo,myPoints

def wait_for_choice_poke(var,doo,myPoints):
    reDrawStim(var,doo,myPoints)
    var.timeStart3 = time.time()
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True:
        if mouse.isPressedIn(blueCircle(var,doo),buttons=[0]):
            var.choiceWrong = False
            var.yrewmag = var.rewmag
            var.rewmag = var.shortmag
            #print var.yrewmag, var.rewmag
            var.choice = 'b'
            getInitStimDis_exp(var)
            timeEnd = time.time()
            var.wait_for_choice_poke_time = timeEnd-var.timeStart3 # changed from blue
            if var.wait_for_choice_poke_time <= var.standardRT_get_reward:
                var.learnedChoicePoke += 1
                var.goodPokesInARoll += 1
            var.GetaNum = []
            var.reward_give = []
            var.state = 'draw_rewardCircle'
            return var,doo,myPoints
        elif mouse.isPressedIn(yellowCircle(var,doo),buttons=[0]):
            var.choiceWrong = False
            var.yrewmag = var.rewmag
            #print var.yrewmag, var.rewmag
            var.choice = 'y'
            getInitStimDis_exp(var)
            timeEnd = time.time()
            var.wait_for_choice_poke_time = timeEnd-var.timeStart3
            if var.wait_for_choice_poke_time <= var.standardRT_get_reward: # changed from yellow
                var.learnedChoicePoke += 1
                var.goodPokesInARoll += 1
            # if var.adaptstg == 1: 
            #     var.GetaNum = var.shuffleProbDraw[var.rewardGot]
            if var.forced == 0 and var.adv8check == False: # is a free trial
                var.GetaNum = var.shuffleFreeProbDraw[var.rewFreeIndex] # predetermined list for forced trials
            else:
                var.GetaNum = random.random() # get a random number between 0 and 1
                print("var.GetaNum: " + str(var.GetaNum))
                print("var.GetaNum <= var.probmag: " + str(var.GetaNum <= var.probmag))
            if var.GetaNum <= var.probmag: #decide whether to give reward based on given probability
                var.reward_give = True
                print("give reward")
                var.state =  'draw_rewardCircle' # return the name of next state
            else:
                print("give no reward")
                if var.allplus1:
                    var.reward_give = False # needed for smth else
                    var.lossgive1 = True
                    var.rewmag = var.lotterylose
                    var.state =  'draw_rewardCircle' # return the name of next state
                else:
                    var.reward_give = False
                    var.state = 'none'
                    var.rewardGot += 1 # plus 1 in rewardGot
                    var.wait_for_reward_poke_time = 0 
                    var.learnedRewPoke += 1 # plus 1 in learnedRewPoke if the click was quick enough (assume the subject learned)
                    var.goodPokesInARoll += 1 
                    var.rewmag = 0
                    mouse.clickReset() # reset mouse click
                    circles(var,doo) # draw all the basic circles 
                    myPoints.totalUpdate(var.points) # draw the total coins earned (new earned added)
                    setup.mywin.flip()
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(blueCircle(var,doo))==False and mouse.isPressedIn(yellowCircle(var,doo))==False:
            timeEnd = time.time()
            var.wait_for_choiceViolation_poke_time = timeEnd-var.timeStart3
            #var.choiceWrong = True
            #var.state = 'wait_for_choice_poke' #changed from 'violationSound'
            return var,doo,myPoints


# check and record whether the mouse clicks within a certain place
#def wait_for_rewardPort_poke(var,doo,myPoints):
#    reDrawRew(var,doo,myPoints) # redraw everything
#    var.timeStart1 = time.time() # record start time of waiting for reward poke
#    beingPressed = False
#    #while True:
#        #if sum(mouse.getPressed())==0:
#            #break
#    while True: # keep checking status
#        if mouse.isPressedIn(rewardCircle(var,doo),buttons=[0]): # if mouse click in the reward port
#            timeEnd1 = time.time() # record end time of waiting for reward poke
#            var.wait_for_reward_poke_time = timeEnd1-var.timeStart1 # calculate the time taken to click in the reward port
#            var.rewardGot += 1 # plus 1 in rewardGot
#            if var.wait_for_reward_poke_time <= var.standardRT_get_reward: # check it's a quick enough click
#                var.learnedRewPoke += 1 # plus 1 in learnedRewPoke if the click was quick enough (assume the subject learned)
#                if var.stg == 0 or var.stg==5:
#                    var.goodPokesInARoll += 1 #plus 1 in goodPokesInARoll to calculate number of correct pokes in a roll (for passing the stage)
#            else: 
#                var.goodPokesInARoll = 0 # set goodPokesInARoll to 0 if it's not a quick enough click
#            if var.stg < 5:
#            var.state =  'hitSound' # return the name of next state
#        elif mouse.getPressed()[0]>0 and not mouse.isPressedIn(rewardCircle(var,doo),buttons=[0]): # button 0 is pressed
#            if not beingPressed: # initial detection
#                timeEnd = time.time()
#                var.wait_for_rewViolation_poke_time = timeEnd-var.timeStart1
#                mouse_loc = mouse.getPos()
#                var.reward_clicks.append(str(var.wait_for_rewViolation_poke_time)+'-'+str(mouse_loc))
#                beingPressed = True
#            beingPressed = False
#        # Wait until all buttons are released
#        elif sum(mouse.getPressed())==0:
#            beingPressed = False
#        while any(mouse.getPressed()):
#            pass
#        return var,doo,myPoints

def wait_for_rewardPort_poke(var,doo,myPoints):
    reDrawRew(var,doo,myPoints) # redraw everything
    var.timeStart1 = time.time() # record start time of waiting for reward poke
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True: # keep checking status
        if mouse.isPressedIn(rewardCircle(var,doo),buttons=[0]): # if mouse click in the reward port
            #var.rewWrong = False
            timeEnd1 = time.time() # record end time of waiting for reward poke
            var.wait_for_reward_poke_time = timeEnd1-var.timeStart1 # calculate the time taken to click in the reward port
            var.rewardGot += 1 # plus 1 in rewardGot
            if var.wait_for_reward_poke_time <= var.standardRT_get_reward: # check it's a quick enough click
                var.learnedRewPoke += 1 # plus 1 in learnedRewPoke if the click was quick enough (assume the subject learned)
                if var.stg == 0 or var.stg==5:
                    var.goodPokesInARoll += 1 #plus 1 in goodPokesInARoll to calculate number of correct pokes in a roll (for passing the stage)
            else: 
                if var.stg < 4:
                    var.goodPokesInARoll = 0 # set goodPokesInARoll to 0 if it's not a quick enough click
            var.state =  'hitSound' # return the name of next state
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(rewardCircle(var,doo))==False: # if mouse click NOT in the reward port
            timeEnd2 = time.time() # record end time of waiting for the wrong poke
            var.wait_for_rewViolation_poke_time = timeEnd2-var.timeStart1 # calculate the time taken to make the wrong click
            #var.rewWrong = True # mark rewWrong to be true for later use
            #var.state = 'wait_for_rewardPort_poke' # changed from 'violationSound' # return the name of next state
            return var,doo,myPoints


#this function redraws everything while waiting for init poke
def reDrawInit(var,doo,myPoints):
    circles(var,doo)
    initCircle(var,doo)
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()

#this function redraws everything while waiting for blue port poke
def reDrawBlue(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()

#this function redraws everything while waiting for yellow port poke
def reDrawYellow(var,doo,myPoints):
    circles(var,doo)
    yellowCircle(var,doo)
    myPoints.totalUpdate(var.points)
    setup.mywin.flip(clearBuffer=True)

#this function draws everything while waiting for a choice
def reDrawStim(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    yellowCircle(var,doo)
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()

# redraw everything while waiting for a reward poke
def reDrawRew(var,doo,myPoints):
    circles(var,doo) # draw all the basic circles
    rewardCircle(var,doo) # draw the reward circle
    myPoints.totalUpdate(var.points)# draw the total points earned in nonverbal
    setup.mywin.flip() # show all the drawing

# generate and play the violation sound and the wrong circles
def violationSound(var,doo,myPoints):
    toneOut2 = doo.violationSound() # make a object of the violation sound
    mouse.clickReset() # reset mouse
    while True:
        toneOut2.setVolume(0.025) # set the volume of the violation sound
        toneOut2.play() # play the violation sound
        wrongCircles(var,doo) # draw the violation black circles
        myPoints.totalUpdate(var.points)# draw the total points earned in nonverbal
        setup.mywin.flip() # show all the drawings
        wrongTimeStart = time.time() 
        wrongTimeEnd = time.time()
        while wrongTimeEnd-wrongTimeStart<= var.vioSoundDur: # play the violation sound for a certain duration
            wrongTimeEnd = time.time()
        var.state = 'none'  # return the name of next state (end of a trial)
        return var,doo,myPoints

# generate and play the hit sound
def hitSound(var,doo,myPoints):
    mouse.clickReset() # reset mouse click
    circles(var,doo) # draw all the basic circles
    myPoints.nowtotalUpdate(var.rewmag) # draw the coins earned in this trial
    myPoints.totalUpdate(var.points) # draw the total coins earned
    setup.mywin.flip() # show all the drawings
    showCoinTimeStart = time.time() # record start time of showing coins
    showCoinTimeEnd = time.time() #  record end time of showing coins
    while showCoinTimeEnd-showCoinTimeStart<= var.showCoinDur: # show the coins for certain duration
        showCoinTimeEnd = time.time()
    var.points+=var.rewmag # add reward magnitude of this trial to total points earned
    circles(var,doo) # draw all the basic circles 
    myPoints.totalUpdate(var.points) # draw the total coins earned (new earned added)
    setup.mywin.flip(clearBuffer=True) # show all the drawings (total coins updated, coins in the reward port disappeared)
    var.rew_sound.play(loops = var.rewmag-1) # play the reward sound, 
    playRewTimeStart = time.time() # record start time of playing reward sound
    playRewTimeEnd = time.time() #  record end time of showing coins
    beingPressed = False # set a boolean to indicate whether mouse is clicked
    while playRewTimeEnd-playRewTimeStart<= var.hitSoundDur*var.rewmag:  # play the reward sound for certain duration, at the same time record any clicks
        if mouse.isPressedIn(doo.circle0(),buttons=[0]): # check if click in circle 0
            if not beingPressed:
                timeEnd = time.time() 
                reward_click_time = timeEnd-playRewTimeStart # calculate the time taken to make the click
                var.reward_clicks.append(str(reward_click_time)+'-'+str(0)) # record the click during reward sound
            beingPressed = True # set the boolean beingPressed to be True
        elif mouse.isPressedIn(doo.circle1(),buttons=[0]): # check if click in circle 1
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(1))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle2(),buttons=[0]): # check if click in circle 2
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(2))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle3(),buttons=[0]): # check if click in circle 3
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(3))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle4(),buttons=[0]): # check if click in circle 4
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(4))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle5(),buttons=[0]): # check if click in circle 5
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(5))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle6(),buttons=[0]): # check if click in circle 6
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(6))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle7(),buttons=[0]): # check if click in circle 7
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(7))
            beingPressed = True
        elif mouse.getPressed()[0]>0 \
        and not mouse.isPressedIn(doo.circle7(),buttons=[0]) and not mouse.isPressedIn(doo.circle6(),buttons=[0]) \
        and not mouse.isPressedIn(doo.circle5(),buttons=[0]) and not mouse.isPressedIn(doo.circle4(),buttons=[0]) \
        and not mouse.isPressedIn(doo.circle3(),buttons=[0]) and not mouse.isPressedIn(doo.circle2(),buttons=[0]) \
        and not mouse.isPressedIn(doo.circle1(),buttons=[0]) and not mouse.isPressedIn(doo.circle0(),buttons=[0]) : # check if click not in any circles
            if not beingPressed: # if didn't press in any circle before
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+'other')
            beingPressed = True
        elif sum(mouse.getPressed())==0: # if didn't press anywhere during reward sound
            beingPressed = False # set boolean beingPressed to be false
        playRewTimeEnd = time.time()
    var.state = 'none'  # return the name of next state (end of a trial)
    return var,doo,myPoints

def zeroReward(var,doo,myPoints):
    mouse.clickReset() # reset mouse click
    circles(var,doo) # draw all the basic circles
    redCross(var,doo) # zero coins earned in this trial
    myPoints.totalUpdate(var.points) # draw the total coins earned
    setup.mywin.flip() # show all the drawings
    core.wait(1) # keep the drawings for 1 second
    var.state = 'none'  # return the name of next state (end of a trial)
    return var,doo,myPoints

# determine whether to run this trial again or go to next trial
def again_or_next(var):
    if var.initWrong or var.fixWrong: # if any violations are made, run this trial again with same settings
        #var.rewWrong = False # reset the boolean for next trial
        var.initWrong = False # reset the boolean for next trial
        var.fixWrong = False # reset the boolean for next trial
        #var.blueWrong = False # reset the boolean for next trial
        #var.yellowWrong = False # reset the boolean for next trial
        #var.choiceWrong = False # reset the boolean for next trial
        return 'again'
    else: # otherwise run next trial with new settings
        var.repeatSet = False
        return 'next'

# determine whether the subject has learned the task
def passStageTest(var):
    if var.goodPokesInARoll >= var.passThreshold: # if the number of correct trials in a row exceed certain number, assume the subject has learned the task
        return 'pass'

# determine whether the subject has learned the task
def passStage45Test(var):
    if var.goodPokesInARoll >= var.stage45trial: # if the number of correct trials exceed certain number, assume the subject has learned the task
        return 'pass'

# show all the big coins at the end of a session/block
def show_bigCoins(var,myPoints):
    myPoints.stackAllbig(var.points) # draw all the big coins
    setup.mywin.flip() # show the drawings
    core.wait(2) # keep the drawings for 2 seconds
    var.dataFile.close() # close the data file

#this function gets a random duration of the fixation
def getFixmag(var):
    random.shuffle(var.fixmag)
    var.fixDur = var.fixmag[random.randint(0,len(var.fixmag)-1)]
    return var

#this function gets one random position code for blue circle port from predetermined random sequence of ports
def getBluePos(var):
    if len(var.staticPos) > 0: # if the staticPos variable has been assigned values, blue circle position is static
        var.bluePosCode = var.staticPos[0] # first value is the static position value for the blue circle
    else:
        if var.stg==3:
            var.bluePosCode = var.shufflePos[var.rewardGot]
        else:
            var.bluePosCode = var.shufflePos[var.rewardGot]
        for i in range(2,8):
            if var.bluePosCode == i:
                var.bluePos = i

#this function gets one random position code for yellow circle port from predetermined random sequence of ports
#def get_forcedYellowPosCode(var):
#    var.yellowPosCode = var.D15Pairs[random.randint(0,len(var.D15Pairs)-1)]
#    for i in range(2,8): 
#        if var.yellowPosCode == i:
#            var.yellowPos = i
#    return var

#this function gets one random position code for yellow circle port from predetermined random sequence of ports
def getYellowPos(var):
    if len(var.staticPos) > 0: # if the staticPos variable has been assigned values, yellow circle position is static
        var.yellowPosCode = var.staticPos[1] # second value is the static position value for the yellow circle
    else: # if the staticPos variable has not been assigned values, yellow circle position is not static
        if var.stg==4:
            var.yellowPosCode = var.shufflePos[var.rewardGot+8]
        else:
            var.yellowPosCode = var.shufflePos[var.rewardGot]
        for i in range(2,8):
            if var.yellowPosCode == i:
                var.yellowPos = i

# this function generates a high low (6 in total) reward list
def makeHighLowRew(var):
    for i in range(np.int(var.forcedTrialNum/2)-1):
        var.highLowRew.append(max(var.mag))
        var.highLowRew.append(min(var.mag))
        #random.shuffle(var.highLowRew)
    return var

# this function generates a high low (6 interleaved + 3 max + 3 min = 12 in total) reward list
def makeHighLowRew_n(var):
    for i in range(np.int(var.forcedTrialNum/2)-1):
        var.highLowRew.append(max(var.mag))
        var.highLowRew.append(min(var.mag))
        #random.shuffle(var.highLowRew)
    var.highLowRew.append(max(var.mag))
    var.highLowRew.append(max(var.mag))
    var.highLowRew.append(max(var.mag))
    var.highLowRew.append(max(var.mag))
    var.highLowRew.append(min(var.mag))
    var.highLowRew.append(min(var.mag))
    var.highLowRew.append(min(var.mag))
    var.highLowRew.append(min(var.mag))
    return var

# This is a function for the stage45 learning in the risk_nv_freeforced task. 
# this function generates a high low (20 max(reward = 18) + 20 low(reward = 2) + 5 max + 5 low + 5 max + 5 low) reward list
def makeHighLowRew_freeforced(var):
    # var.mag contains magnitude of rewards, in the nonverbal 2019 fall task, we only have two rewards (2 and 18).
    # we use those to create a reward list. _
    for i in  [max(var.mag), min(var.mag)]: 
        for j in range(20): 
            var.highLowRew.append(i)

    for i in range(2):
        for j in [max(var.mag), min(var.mag)]:
            for z in range(5):
                var.highLowRew.append(j)
    return var


#this function gets a random end rewmag
def getHighLowRew(var,index):
    var.rewmag = var.highLowRew[index]
    if var.rewmag == 2:
        var.hitmag = 0.5
    elif var.rewmag ==5:
        var.hitmag = 2
    elif var.rewmag ==8:
        var.hitmag = 4
    elif var.rewmag ==12:
        var.hitmag = 6
    elif var.rewmag ==15:
        var.hitmag = 8
    else:
        var.hitmag = 10
    #print var.rewmag, var.hitmag
    return var

# this function generates a high low (6 in total) reward list
def makeHighLowProb(var):
    for i in range(np.int(var.forcedTrialNum/2)-1):
        var.highLowProb.append(max(var.probability))
        var.highLowProb.append(min(var.probability))
        #random.shuffle(var.highLowProb)
    return var

#this function gets a random end rewmag
def getHighLowProb(var,index):
    var.probmag = var.highLowProb[index]
    #print var.probmag, var.highLowProb, index
    if var.probmag ==0.13:
        var.sndprobmag = 16
    else:
        var.sndprobmag = 1
    return var

#this function calculates the distance between the init port and the stimulus port
def getInitStimDis(var):
    X_init=var.elX[var.initPosCode]
    Y_init=var.elY[var.initPosCode]
    X_stim=var.elX[var.yellowPosCode]
    Y_stim=var.elY[var.yellowPosCode]
    InitStimDis_sq = (X_stim-X_init)**2+(Y_stim-Y_init)**2
    InitStimDis_real = (np.sqrt(InitStimDis_sq))
    var.initStimDis = InitStimDis_real/120.0
    return var

#this function calculates the distance between the init port and the stimulus port in mixNonverbal
def getInitStimDis_exp(var):
    X_init=var.elX[var.initPosCode]
    Y_init=var.elY[var.initPosCode]
    if var.choice == 'y':
        X_stim=var.elX[var.yellowPosCode]
        Y_stim=var.elY[var.yellowPosCode]
    elif var.choice =='b':
        X_stim=var.elX[var.bluePosCode]
        Y_stim=var.elY[var.bluePosCode]
    InitStimDis_sq = (X_stim-X_init)**2+(Y_stim-Y_init)**2
    InitStimDis_real = np.sqrt(InitStimDis_sq)
    var.initStimDis = InitStimDis_real/120
    return var

#this function creates symmetric choice positions in MixNonverbal task
def symmetricYBPair(var):
    if var.bluePosCode == 2:
        var.yellowPosCode = 3
    elif var.bluePosCode == 3:
        var.yellowPosCode = 2
    elif var.bluePosCode == 4:
        var.yellowPosCode = 5
    elif var.bluePosCode == 5:
        var.yellowPosCode = 4
    elif var.bluePosCode == 6:
        var.yellowPosCode = 7
    elif var.bluePosCode == 7:
        var.yellowPosCode = 6
    for i in range(2,8):
        if var.yellowPosCode == i:
            var.yellowPos = i
    return var

# this functions gets the reward mag for the orderly block
def getRewmag(var):
    var.rewmag = var.mag[var.rewIndex]
    if var.rewmag ==2:
        var.hitmag = 1
    elif var.rewmag ==4:
        var.hitmag = 2
    elif var.rewmag ==6:
        var.hitmag = 5
    elif var.rewmag ==12:
        var.hitmag = 8
    else:
        var.hitmag = 10
    #print var.rewmag, var.hitmag
    return var

#this function gets a random hit mag, responsible for sound frequency
# if you plan to have more than 5 values, then all 6 should be within 1-10 e.g. 1-2-4-6-8-10 values for var.hitmag
def getHitmag(var):
    if var.forced == 0 and var.schedule != "new_sound":
        var.rewmag = var.shuffleFreeRew[var.rewFreeIndex]
    elif var.forced == 1 and var.schedule != "new_sound":
        if var.adv8check == True:
            var.rewmag = var.shuffleFreeRew[var.rewFreeIndex]
        else:
            var.rewmag = var.shuffleForcedRew[var.rewForcedIndex]
    elif var.schedule != "new_sound":
        var.rewmag = var.shuffleRew[var.rewardGot]
    #print var.rewmag
    if var.rewmag == var.mag[0]:
        var.hitmag = 0.5
    elif var.rewmag == var.mag[1]:
        var.hitmag = 2
    elif var.rewmag == var.mag[2]:
        var.hitmag = 4
    elif var.rewmag == var.mag[3]:
        var.hitmag = 6
    elif var.rewmag == var.mag[4]:
        var.hitmag = 8
    elif var.rewmag == var.mag[5]:
        var.hitmag = 10
    else:
        var.hitmag = 10
    #print ymag, var.rewmag, var.hitmag
    return var

# this functions gets the probability for the orderly block
def getProbord(var):
    var.probmag = var.probability[var.probIndex]
    if var.probmag ==0.13:
        var.sndprobmag = 16
    elif var.probmag ==0.25:
        var.sndprobmag = 8
    elif var.probmag ==0.38:
        var.sndprobmag = 4
    elif var.probmag ==0.5:
        var.sndprobmag = 2
    else:
        var.sndprobmag = 1
    return var

#this function gets a random probability
def getProb(var):
    var.probmag = var.shuffleProb[var.rewardGot] # Random magnitude, for risk_nv_freeforced this has to be commented out
    #if var.probmag ==0.13:
    #    var.sndprobmag = 16
    if var.probmag ==0.25:
        var.sndprobmag = 16 # for 3 probabilities
    #elif var.probmag ==0.38:
    #    var.sndprobmag = 4
    elif var.probmag ==0.5:
        var.sndprobmag = 4 # for 3 probabilities
    else:
        var.sndprobmag = 1
    return var

def getProb_freeforced(var):

    if var.shuffle == True:
        print("shuffleProb: " + str(var.shuffleProb))
        var.probmag = var.shuffleProb[var.rewFreeIndex]
    else:
        var.probmag = var.probability[var.probIndex] # set the reward probability to 50%
    print("probmag: " + str(var.probmag))
    if var.probmag ==0.25:
        var.sndprobmag = 16 # for 3 probabilities
    elif var.probmag ==0.5:
        var.sndprobmag = 4 # for 3 probabilities
    else:
        var.sndprobmag = 1
    print("sndprobmag: " + str(var.sndprobmag))
    return var

# get block probability sound
def getProbSnd(var):
    if var.blockProbMag ==0.13:
        var.sndprobmag = 16
    elif var.blockProbMag ==0.25:
        var.sndprobmag = 8
    elif var.blockProbMag ==0.38:
        var.sndprobmag = 4
    elif var.blockProbMag ==0.5:
        var.sndprobmag = 2
    else:
        var.sndprobmag = 1
    return var

# get the total points and trial number of this stage
def total_Points_trialCounter(var):
    return var.points, var.trialCounter

# reset the total points and trial number to 0
def reset_Points_trialCounter(var):
    var.trialCounter = 0
    var.points = 0
    var.totalTrialCounter = 0

#  shows all the coins earned at the end of all learning stages
def show_bigCoins_total(totalProfits,myPoints):
    myPoints.stackAllbig(totalProfits) # draw all the big coins
    setup.mywin.flip() # show the drawings
    core.wait(2) # keep the drawings on the screen for 2 seconds

#  generate and show the end session instruction for learning stages
def end_instruction(doo):
    doo.instruction.text = u'This is the end of learning stages.\n\nThe real experiment is about to start. Please get ready.' # set the content of instruction
    doo.instruction.pos=[0,0] # set the position of the instruction
    doo.instruction.height = 30 # set the size of the instruction text
    doo.instruction.draw() # draw the instruction
    setup.mywin.flip() # show the drawings
    core.wait(10) # keep the drawings on the screen for 10 seconds

#  generate and show the end session instruction
def end_session(doo):
    doo.instruction.text = 'This is the end of the session.\n\nThank you for your participation.' # set the content of instruction
    doo.instruction.pos=[0,0] # set the position of the instruction
    doo.instruction.height = 30 # set the size of the instruction text
    doo.instruction.draw() # draw the instruction
    setup.mywin.flip() # show the drawings
    core.wait(10) # keep the drawings on the screen for 10 seconds

#this function generates the  instruction between sessions
def break_instruction(doo):
    doo.instruction.text = u'You may take a short break now.\n\nPress enter if you are ready to start the decision stages.\n\nNote: Keep your headphones on, and if you don\'t hear any sound after pressing enter, please report to the experimenter.'
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    press = event.waitKeys(keyList="return")
    while press[0]=="return":
        break

# generate the end session instruction for mix nonverbal stage
def end_instruction_timeout(doo):
    doo.instruction.text = u'This is the end of the experimental session.\n\nPlease report to the experimenter. Thank you very much for your participating!\n\n Enjoy the rest of your day :)'
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(15)
    core.quit() # closing the experiment...

# generate the end session instruction for mix nonverbal stage
def end_instruction_mixNon(doo):
    doo.instruction.text = u'This is the end of the experimental session.\n\nPlease report to the experimenter. Thank you very much for your participating!\n\n Enjoy the rest of your day :)'
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(15)

# DATA RECORDING

#-----------------data recording set up for learning stages-----------------------------------
def dataRecordStart0(var,dbc): 
    p_num = sql.r_subjidfromsessid(dbc,var.sessid)
    expName = 'stage0'
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{}\n".format('trial_No.','learned_trial_No.','rewMag','totalPoints','trialsCorrect', 
        'Reaction Time','Violation Time','rew_click'))
    var.dataFile.flush()

def dataRecordStart1(var,dbc):
    p_num = sql.r_subjidfromsessid(dbc,var.sessid)
    expName = 'stage1'
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{}\n".format('trial_No.','learned_init_No.','learned_rew_No.','rewMag','totalPoints','trialscorrect', 
        'initReaction Time','initViolation Time','rewReaction Time','rewViolation Time','rew_click'))
    var.dataFile.flush()

def dataRecordStart2(var,dbc):
    p_num = sql.r_subjidfromsessid(dbc,var.sessid)
    expName = 'stage2'
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('No.','linit_No.','lfix_No.','lrew_No.','fixDur','rewMag','totalPoints','trialscorrect', 
        'initRT','initVT','fixVT','rewRT','rewVT','fix_click','rew_click'))
    var.dataFile.flush()

def dataRecordStart3(var,dbc):
    p_num = sql.r_subjidfromsessid(dbc,var.sessid)
    expName = 'stage3'
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('No.','linit_No.','lfix_No.','lrew_No.','rewMag','Total','hit_No', 
        'initRT','initVT','fixVT','fixDur','bluePos','blueRT','blueVT','rewRT','rewVT','fix_click','dec_click','rew_click'))
    var.dataFile.flush()

def dataRecordStart4(var,dbc):
    p_num = sql.r_subjidfromsessid(dbc,var.sessid)
    expName = 'stage4'
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('totalNo.','No.','linit_No.','lfix_No.','lrew_No.','rewMag', 'Total','hit_No.', 
        'initRT','initVT','fixVT','fixDur','yellowPos','Dist','yellowRT','yellowVT','rewRT','rewVT','fix_click','dec_click','rew_click'))
    var.dataFile.flush()

def dataRecordStart5(var,dbc):
    p_num = sql.r_subjidfromsessid(dbc,var.sessid)
    expName = 'stage5'
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('totalNo.',
        'No.','linit_No.','lfix_No.','lrew_No.','rewMag','Total','hit_No.','initRT','initVT','fixVT','fixDur',
        'yellowPos','Dist','probability','yellowRT','yellowVT','rewRT','rewVT','fix_click','dec_click','rew_click','GetaNum','reward_give'))
    var.dataFile.flush()

#-----------------------------data recording after one trial-----------------------------------
# record all the data in this trial(learning stage 0)
def dataRecord0(var,dbc):
    if var.rewWrong: # record variables if subject made a reward click violation
        var.dataFile.write("{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            '/',var.wait_for_rewViolation_poke_time,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewVT': var.wait_for_rewViolation_poke_time, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    else: # record variables if subject didn't make any violations
        var.dataFile.write("{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_reward_poke_time,'/',var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewRT': var.wait_for_reward_poke_time, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush() # clear the data file for next trial
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 1)
def dataRecord1(var,dbc):
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,var.learnedInitPoke,
            var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            '/',var.wait_for_initViolation_poke_time,'/','/',var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'linit': var.learnedInitPoke,'initVT': var.wait_for_initViolation_poke_time, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
#    elif var.rewWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,var.learnedInitPoke,var.learnedRewPoke,
#            var.rewmag,var.points,var.rewardGot,var.wait_for_init_poke_time,'/','/',var.wait_for_rewViolation_poke_time,var.reward_clicks))
#        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot,  
#            'rewVT': var.wait_for_rewViolation_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,var.learnedInitPoke,var.learnedRewPoke,
            var.rewmag,var.points,var.rewardGot,var.wait_for_init_poke_time,'/',var.wait_for_reward_poke_time,'/',var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewRT': var.wait_for_reward_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 2)
def dataRecord2(var,dbc):
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,'/',var.rewmag,var.points,var.rewardGot, 
            '/',var.wait_for_initViolation_poke_time,'/','/','/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1,'points': var.points, 'trialsCorrect': var.rewardGot, 
            'linit': var.learnedInitPoke, 'initVT': var.wait_for_initViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.fixDur,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,'/','/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 
            'lfix': var.learnedFix,'fixDur': var.fixDur, 'fixVT': var.wait_for_fixViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
#    elif var.rewWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
#            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.fixDur,var.rewmag,var.points,var.rewardGot, 
#            var.wait_for_init_poke_time,'/','/','/',var.wait_for_rewViolation_poke_time,var.fixation_clicks,var.reward_clicks))
#        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
#            'rewVT': var.wait_for_rewViolation_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time,
#            'lfix': var.learnedFix,'fixDur': var.fixDur, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.fixDur,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/','/',var.wait_for_reward_poke_time,'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewRT': var.wait_for_reward_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time,
            'lfix': var.learnedFix,'fixDur': var.fixDur, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 3)
def dataRecord3(var,dbc):
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            '/',var.wait_for_initViolation_poke_time,'/','/','/','/','/','/','/',var.fixation_clicks,var.decision_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points,'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initVT': var.wait_for_initViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,var.fixDur,'/','/','/','/','/',var.fixation_clicks,var.decision_clicks,
            var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'fixVT': var.wait_for_fixViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
#    elif var.blueWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
#            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
#            var.wait_for_init_poke_time,'/','/',var.fixDur,var.bluePos,'/',var.wait_for_blueViolation_poke_time,'/','/',var.fixation_clicks,var.reward_clicks))
#        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
#            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke,'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,
#            'fixDur': var.fixDur, 'bluePos': var.bluePos, 'decisionVT':var.wait_for_blueViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
#    elif var.rewWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
#            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
#            var.wait_for_init_poke_time,'/','/',var.fixDur,var.bluePos,var.wait_for_blue_poke_time,'/','/',
#            var.wait_for_rewViolation_poke_time,var.fixation_clicks,var.reward_clicks))
#        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
#            'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time,'linit': var.learnedInitPoke, 
#            'initRT': var.wait_for_init_poke_time, 'lfix': var.learnedFix,'fixDur': var.fixDur, 'bluePos': var.bluePos, 
#            'decisionRT':var.wait_for_blue_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1, 
            var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/','/',var.fixDur,var.bluePos,var.wait_for_blue_poke_time,'/',var.wait_for_reward_poke_time,'/',
            var.fixation_clicks,var.decision_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'bluePos': var.bluePos, 'decisionRT':var.wait_for_blue_poke_time, 
            'fixClicks': var.fixation_clicks, 'decClicks': var.decision_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 4)
def dataRecord4(var,dbc):
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            '/',var.wait_for_initViolation_poke_time,'/','/','/','/','/','/','/','/',var.fixation_clicks,var.decision_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initVT': var.wait_for_initViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,var.fixDur,'/','/','/','/','/','/',
            var.fixation_clicks,var.decision_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'fixVT':var.wait_for_fixViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
#    elif var.yellowWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
#            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
#            var.wait_for_init_poke_time,'/','/',var.fixDur,var.yellowPos,var.initStimDis,'/',var.wait_for_yellowViolation_poke_time,'/','/',
#            var.fixation_clicks,var.reward_clicks))
#        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
#            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
#            'initRT': var.wait_for_init_poke_time, 'lfix': var.learnedFix,   
#            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionVT':var.wait_for_yellowViolation_poke_time, 
#            'Distance':var.initStimDis, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
#    elif var.rewWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
#            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
#            var.wait_for_init_poke_time,'/','/',var.fixDur,var.yellowPos,var.initStimDis,var.wait_for_yellow_poke_time,'/',
#            '/',var.wait_for_rewViolation_poke_time,var.fixation_clicks,var.reward_clicks))
#        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
#            'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time,'linit': var.learnedInitPoke, 
#            'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,'fixDur': var.fixDur, 'yellowPos': var.yellowPos,
#            'decisionRT':var.wait_for_yellow_poke_time, 'Distance':var.initStimDis, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/','/',var.fixDur,var.yellowPos,var.initStimDis,var.wait_for_yellow_poke_time,'/',
            var.wait_for_reward_poke_time,'/',var.fixation_clicks,var.decision_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1,'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,'fixDur': var.fixDur, 'yellowPos': var.yellowPos,
            'decisionRT':var.wait_for_yellow_poke_time, 'Distance':var.initStimDis, 'fixClicks': var.fixation_clicks,'decClicks':var.decision_clicks,
            'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 5)
def dataRecord5(var,dbc):
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            '/',var.wait_for_initViolation_poke_time,'/','/','/','/','/','/','/','/','/',var.fixation_clicks,
            var.decision_clicks,var.reward_clicks,'/','/'))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot,'linit': var.learnedInitPoke,'initVT': var.wait_for_initViolation_poke_time, 
            'fixClicks': var.fixation_clicks,  
            'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,var.fixDur,'/','/',var.probmag,'/','/','/','/',
            var.fixation_clicks,var.decision_clicks,var.reward_clicks,'/','/'))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot,'linit': var.learnedInitPoke,'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'fixVT':var.wait_for_fixViolation_poke_time, 'probability':var.probmag, 
            'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
#    elif var.yellowWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
#            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
#            var.wait_for_init_poke_time,'/','/',var.fixDur,var.yellowPos,var.initStimDis,var.probmag,'/',
#            var.wait_for_yellowViolation_poke_time,'/','/',var.fixation_clicks,var.reward_clicks,'/','/'))
#        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
#            'trialsCorrect': var.rewardGot,'linit': var.learnedInitPoke,'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,   
#            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionVT':var.wait_for_yellowViolation_poke_time, 
#            'Distance':var.initStimDis, 'probability':var.probmag, 'fixClicks': var.fixation_clicks, 
#            'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
#    elif var.rewWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
#            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
#            var.wait_for_init_poke_time,'/','/',var.fixDur,var.yellowPos,var.initStimDis,var.probmag,var.wait_for_yellow_poke_time,'/',
#            '/',var.wait_for_rewViolation_poke_time,var.fixation_clicks,var.reward_clicks,'/','/'))
#        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,
#            'points': var.points,'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time,'linit': var.learnedInitPoke, 
#            'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,'fixDur': var.fixDur, 'yellowPos': var.yellowPos,
#            'decisionRT':var.wait_for_yellow_poke_time,'Distance':var.initStimDis, 'probability':var.probmag, 
#            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.totalTrialCounter+1,
            var.mergedTrialCounter+1,var.learnedInitPoke,var.learnedFix,var.learnedRewPoke,var.rewmag,var.points,var.rewardGot, 
            var.wait_for_init_poke_time,'/','/',var.fixDur,var.yellowPos,var.initStimDis,var.probmag,var.wait_for_yellow_poke_time,'/',
            var.wait_for_reward_poke_time,'/',var.fixation_clicks,var.decision_clicks,var.reward_clicks,var.GetaNum,var.reward_give))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,
            'points': var.points,'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time,'lfix': var.learnedFix,'fixDur': var.fixDur, 'yellowPos': var.yellowPos,
            'decisionRT':var.wait_for_yellow_poke_time,'Distance':var.initStimDis,'probability':var.probmag,
            'fixClicks': var.fixation_clicks, 'decClicks':var.decision_clicks,'rewClicks': var.reward_clicks,'GetaNum':var.GetaNum,'reward_give':var.reward_give}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial (adapt and nv decision stages)
def dataRecord_adapt_nv(var,dbc):
    var.dataFile.flush()
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.adaptstg,var.points,var.rewardGot,'/',var.wait_for_initViolation_poke_time,'/','/','/','/','/','/',
            var.yrewmag,'/','/',var.blockProbMag,'/',var.fixation_clicks,var.decision_clicks,var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initVT': var.wait_for_initViolation_poke_time, 'probability':var.probmag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_adapttrial(dbc,var,sd)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.adaptstg,var.points,var.rewardGot,var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,
            var.fixDur,'/','/','/','/',var.yrewmag,'/','/',var.blockProbMag,'/',var.fixation_clicks,var.decision_clicks,
            var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur,'fixVT': var.wait_for_fixViolation_poke_time,
            'probability':var.probmag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_adapttrial(dbc,var,sd)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.adaptstg,var.points,var.rewardGot,var.wait_for_init_poke_time,'/','/',
            var.fixDur,var.bluePos,var.yellowPos,var.wait_for_choice_poke_time,var.choice,var.yrewmag,var.rewmag,
            var.initStimDis,var.blockProbMag,var.wait_for_reward_poke_time,
            var.fixation_clicks,var.decision_clicks,var.reward_clicks,var.GetaNum,var.reward_give))
        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time,
            'rewRT': var.wait_for_reward_poke_time,'Distance':var.initStimDis,
            'probability':var.probmag,'yellowRew':var.yrewmag,'choice': var.choice,'rewMag': var.rewmag,
            'fixClicks': var.fixation_clicks, 'decClicks':var.decision_clicks,'rewClicks': var.reward_clicks,'GetaNum':var.GetaNum,
            'reward_give':var.reward_give,'allplus1':var.allplus1,'lossgive1':var.lossgive1}
        sd = json.dumps(d)
        if var.choice == 'b':
            var.ychoice = 0
        elif var.choice =='y':
            var.ychoice = 1
        sql.w_after_adapttrial(dbc,var,sd)
    var.dataFile.flush()

#this function records all the data needed from each trial (adapt and nv decision stages)
def dataRecord_risknv(var,dbc):
    var.dataFile.flush()
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.adaptstg,var.points-var.adaptpoints,var.rewardGot,'/',var.wait_for_initViolation_poke_time,'/','/','/','/','/','/',
            var.yrewmag,'/','/',var.blockProbMag,'/',var.fixation_clicks,var.decision_clicks,var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points-var.adaptpoints,'trialsCorrect': var.rewardGot, 
            'initVT': var.wait_for_initViolation_poke_time, 'probability':var.probmag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_risknvtrial(dbc,var,sd)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.adaptstg,var.points-var.adaptpoints,var.rewardGot,var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,
            var.fixDur,'/','/','/','/',var.yrewmag,'/','/',var.blockProbMag,'/',var.fixation_clicks,var.decision_clicks,
            var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points-var.adaptpoints,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur,'fixVT': var.wait_for_fixViolation_poke_time,
            'probability':var.probmag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_risknvtrial(dbc,var,sd)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.adaptstg,var.points-var.adaptpoints,var.rewardGot,var.wait_for_init_poke_time,'/','/',
            var.fixDur,var.bluePos,var.yellowPos,var.wait_for_choice_poke_time,var.choice,var.yrewmag,var.rewmag,
            var.initStimDis,var.blockProbMag,var.wait_for_reward_poke_time,
            var.fixation_clicks,var.decision_clicks,var.reward_clicks,var.GetaNum,var.reward_give))
        d = {'trial': var.trialCounter+1,'points': var.points-var.adaptpoints,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time,
            'rewRT': var.wait_for_reward_poke_time,'Distance':var.initStimDis,
            'probability':var.probmag,'yellowRew':var.yrewmag,'choice': var.choice,'rewMag': var.rewmag,
            'fixClicks': var.fixation_clicks, 'decClicks':var.decision_clicks,'rewClicks': var.reward_clicks,
            'GetaNum':var.GetaNum,'reward_give':var.reward_give,'allplus1':var.allplus1,'lossgive1':var.lossgive1}
        sd = json.dumps(d)
        if var.choice == 'b':
            var.ychoice = 0
        elif var.choice =='y':
            var.ychoice = 1
        sql.w_after_risknvtrial(dbc,var,sd)
    var.dataFile.flush()

    #this function records all the data needed from each trial (adapt and nv decision stages)
def dataRecord_freeforced(var,dbc):
    var.dataFile.flush()
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.advancement,var.points,var.rewardGot,'/',var.wait_for_initViolation_poke_time,'/','/','/','/','/','/',
            var.yrewmag,'/','/',var.blockProbMag,'/',var.fixation_clicks,var.decision_clicks,var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initVT': var.wait_for_initViolation_poke_time, 'probability':var.probmag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_freeforcedtrial(dbc,var,sd)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.advancement,var.points,var.rewardGot,var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,
            var.fixDur,'/','/','/','/',var.yrewmag,'/','/',var.blockProbMag,'/',var.fixation_clicks,var.decision_clicks,
            var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur,'fixVT': var.wait_for_fixViolation_poke_time,
            'probability':var.probmag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_freeforcedtrial(dbc,var,sd)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.advancement,var.points,var.rewardGot,var.wait_for_init_poke_time,'/','/',
            var.fixDur,var.bluePos,var.yellowPos,var.wait_for_choice_poke_time,var.choice,var.yrewmag,var.rewmag,
            var.initStimDis,var.blockProbMag,var.wait_for_reward_poke_time,
            var.fixation_clicks,var.decision_clicks,var.reward_clicks,var.GetaNum,var.reward_give))
        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time,
            'rewRT': var.wait_for_reward_poke_time,'Distance':var.initStimDis,
            'probability':var.probmag,'yellowRew':var.yrewmag,'choice': var.choice,'rewMag': var.rewmag,
            'fixClicks': var.fixation_clicks, 'decClicks':var.decision_clicks,'rewClicks': var.reward_clicks,
            'GetaNum':var.GetaNum,'reward_give':var.reward_give,'allplus1':var.allplus1,'lossgive1':var.lossgive1}
        sd = json.dumps(d)
        if var.choice == 'b':
            var.ychoice = 0
        elif var.choice =='y':
            var.ychoice = 1
        sql.w_after_freeforcedtrial(dbc,var,sd)
    var.dataFile.flush()

#this function records all the data needed from each trial (mix nonverbal session)
def dataRecord_mixNon(var,dbc,sessid):
    if var.initWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.blockName,var.points,var.rewardGot,'/',var.wait_for_initViolation_poke_time,'/','/','/','/','/','/',
            var.yrewmag,'/','/',var.blockProbMag,'/','/','/',var.fixation_clicks,var.decision_clicks,var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initVT': var.wait_for_initViolation_poke_time, 'probability':var.blockProbMag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    elif var.fixWrong:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.blockName,var.points,var.rewardGot,var.wait_for_init_poke_time,'/',var.wait_for_fixViolation_poke_time,
            var.fixDur,'/','/','/','/',var.yrewmag,'/','/',var.blockProbMag,'/','/','/',var.fixation_clicks,var.decision_clicks,
            var.reward_clicks,'/','/'))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur,'fixVT': var.wait_for_fixViolation_poke_time,
            'probability':var.blockProbMag,'yellowRew':var.yrewmag,
            'fixClicks': var.fixation_clicks,'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)
#    elif var.choiceWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
#            var.blockName,var.points,var.rewardGot,var.wait_for_init_poke_time,'/','/',
#            var.fixDur,var.bluePos,var.yellowPos,'/','/',var.yrewmag,'/','/',var.blockProbMag,
#            var.wait_for_choiceViolation_poke_time,'/','/',var.fixation_clicks,var.reward_clicks,'/','/'))
#        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
#            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur, 
#            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionVT': var.wait_for_choiceViolation_poke_time, 
#            'probability':var.blockProbMag,'yellowRew':var.yrewmag, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
#        sql.w_after_Mixnon(dbc,var,sessid,sd)
#    elif var.rewWrong:
#        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
#            var.blockName,var.points,var.rewardGot,var.wait_for_init_poke_time,'/','/',
#            var.fixDur,var.bluePos,var.yellowPos,var.wait_for_choice_poke_time,var.choice,var.yrewmag,'/',
#            var.initStimDis,var.blockProbMag,'/','/',var.wait_for_rewViolation_poke_time,
#            var.fixation_clicks,var.reward_clicks,'/','/'))
#        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
#            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur, 
#            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time,
#            'rewVT': var.wait_for_rewViolation_poke_time,'Distance':var.initStimDis,
#            'probability':var.blockProbMag,'yellowRew':var.yrewmag,'choice': var.choice,
#            'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
#        sd = json.dumps(d)
#        sql.w_after_Mixnon(dbc,var,sessid,sd)
    else:
        var.dataFile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(var.trialCounter+1,
            var.blockName,var.points,var.rewardGot,var.wait_for_init_poke_time,'/','/',
            var.fixDur,var.bluePos,var.yellowPos,var.wait_for_choice_poke_time,var.choice,var.yrewmag,var.rewmag,
            var.initStimDis,var.blockProbMag,'/',var.wait_for_reward_poke_time,'/',
            var.fixation_clicks,var.decision_clicks,var.reward_clicks,var.GetaNum,var.reward_give))
        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time,
            'rewRT': var.wait_for_reward_poke_time,'Distance':var.initStimDis,
            'probability':var.blockProbMag,'yellowRew':var.yrewmag,'choice': var.choice,'rewMag': var.rewmag,
            'fixClicks': var.fixation_clicks, 'decClicks':var.decision_clicks,'rewClicks': var.reward_clicks,'GetaNum':var.GetaNum,'reward_give':var.reward_give}
        sd = json.dumps(d)
        if var.choice == 'b':
            var.ychoice = 0
        elif var.choice =='y':
            var.ychoice = 1
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    var.dataFile.flush()

#-------------------Function Name Dictionary(for recursive state calling)------------------------
funcDic = {'draw_initCircle': draw_initCircle, 'draw_fixCircle':draw_fixCircle,'draw_blueCircle':draw_blueCircle,
        'draw_yellowCircle':draw_yellowCircle,'draw_stimCircles':draw_stimCircles,'draw_rewardCircle': draw_rewardCircle,
        'wait_for_initPort_poke':wait_for_initPort_poke,'wait_for_bluePort_poke':wait_for_bluePort_poke,
        'wait_for_yellowPort_poke':wait_for_yellowPort_poke,'wait_for_choice_poke':wait_for_choice_poke,
        'wait_for_rewardPort_poke':wait_for_rewardPort_poke,
        'reDrawInit':reDrawInit,'reDrawRew':reDrawRew,'zeroReward':zeroReward,
        'violationSound':violationSound,'hitSound':hitSound,'RR_Sound':RR_Sound,'riskySound':riskySound}


#-------------------Specific functions for the Nonverbal 2019 Fall task------------------------

def reset_variables(var):
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
    start_time = datetime.datetime.now()
    var.rewForcedIndex = 0
    var.rewFreeIndex = 0
    reset_Points_trialCounter(var)
    var.sequenceIndex = 0
    var.firstOrderMistakes = []
    return expDate, start_time

def check_reset_shuffle(var, dbc, p_num):
    if var.rewForcedIndex == 80 and (var.advancement == 1 or var.advancement == 2 or var.advancement == 3 or var.advancement == 4):
        var.rewForcedIndex = 0
        np.random.shuffle(var.shuffleForcedRew)
        np.random.shuffle(var.shuffleForcedProbDraw)
    elif var.rewFreeIndex == 40 and (var.advancement == 1 or var.advancement == 2 or var.advancement == 3 or var.advancement == 4):
        var.rewFreeIndex = 0
        np.random.shuffle(var.shuffleFreeRew)
        np.random.shuffle(var.shuffleFreeProbDraw)
    elif var.rewFreeIndex == 30 and (var.advancement == 5 or var.advancement == 6 or var.advancement == 7 or var.advancement == 8 or var.advancement == 9):
        print("Reshuffling the rewards!")
        var.rewFreeIndex = 0
        random.shuffle(var.rewProbTuple)
        var.shuffleFreeRew,var.shuffleFreeProbDraw, var.shuffleProb = list(zip(*var.rewProbTuple))
        var.shuffleFreeRew = list(var.shuffleFreeRew)
        var.shuffleFreeProbDraw = list(var.shuffleFreeProbDraw)
        var.shuffleProb = list(var.shuffleProb)

def write_task_data_away(dbc, var, expDate, p_num, start_time):
    end_time = datetime.datetime.now() # record end time
    timedifference = end_time - start_time # when you subtract two datetime.time objects, you get a timedelta object. 
    var.stageduration = timedifference.total_seconds() # extract the total amount of seconds from the timedelta object.
    sql.w_after_freeforced(dbc, var, p_num, expDate) # record info about the end of the session in the risk_nv_freeforced table


def close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip):
    """
    Functions that closes the session  
    """
    show_bigCoins_total(var.totalPoints,myPoints) # show the total profits to the subjects
    write_task_data_away(dbc, var, expDate, p_num, start_time)
    end_time = datetime.datetime.now()
    end_session(doo) # give the ending instruction to the subject
    sql.w_after_learningALL(dbc,var,p_num, expDate, end_time, expName, host_ip, var.totalTrials, var.totalPoints, setiddtb) # save data of the learningstages in the sessions_end table
    core.wait(2)
    core.quit() 

def forcedTrial_yellow(var, doo, dbc, mouse, myPoints):
    """
    A forced trial only draws yellow circle, force the subject to take a risky option and will help the subject to sample more. 
    """
    var.forced = 1
    var.stg = 45 # using the stage 45 setup for var.state loop
    while var.repeatstage: # repeat the current trial if any violations are made
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            getYellowPos(var) # gets the position of the yellow circle
            if var.schedule == "new_sound":
                var.rewmag = var.new_sound
            else:
                print("\nTrial: " + str(var.trialCounter))
                print("-----------------")
                if var.adv8check == False:
                    print("var.shuffleForcedRew: "+ str(var.shuffleForcedRew))
                    print("rewForcedIndex: " + str(var.rewForcedIndex))
                    var.rewmag = var.shuffleForcedRew[var.rewForcedIndex] # set a predetermined rew magnitude
                    print("var.rewmag: "+ str(var.rewmag))
                else:
                    print("var.shuffleRew: "+ str(var.shuffleFreeRew))
                    print("rewIndex: " + str(var.rewFreeIndex))
                    var.rewmag = var.shuffleFreeRew[var.rewFreeIndex] # set a predetermined rew magnitude
                    print("var.rewmag: "+ str(var.rewmag))
            getHitmag(var)
            getProb_freeforced(var) # sets the probability clicking in the sound
            getInitStimDis(var)  # this function calculates the distance between the init port and the stimulus port
        var,doo,myPoints = draw_initCircle(var,doo,myPoints)
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = funcDic[var.state](var,doo,myPoints)
        if var.advancement == 1: # save it as stage 6 or 7
            var.stg = 6
        elif var.advancement == 2:
            var.stg = 7
        elif var.advancement == 3:
            var.stg = 8
        elif var.advancement == 4:
            var.stg = 9
        elif var.advancement == 5:
            var.stg = 10
        elif var.advancement == 6:
            var.stg = 11
        elif var.advancement == 7:
            var.stg = 12
        elif var.advancement == 8:
            var.stg = 13
        elif var.advancement == 9:
            var.stg = 14
        dataRecord5(var,dbc)
        var.stg = 45
        if again_or_next(var) == 'again': # if aFny violations made
            var.totalTrialCounter += 1 # plus 1 in totalTrialCounter
            var.repeatSet = True
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else: # if no violation made
            if var.advancement == 1: # save it as stage 6 or 7
                var.stg = 6
            elif var.advancement == 2:
                var.stg = 7
            elif var.advancement == 3:
                var.stg = 8
            elif var.advancement == 4:
                var.stg = 9
            elif var.advancement == 5:
                var.stg = 10
            elif var.advancement == 6:
                var.stg = 11
            elif var.advancement == 7:
                var.stg = 12
            elif var.advancement == 8:
                var.stg = 13
            elif var.advancement == 9:
                var.stg = 14
            var.totalTrialCounter += 1 # plus 1 in totalTrialCounter
            var.trialCounter+=1 # plus 1 in trialCounter
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            var.repearSet = False
            var.sequenceIndex += 1 # get the next sequence trial
            if var.adv8check == False:
                var.rewForcedIndex += 1 # get the next trial reward
            else:
                var.rewFreeIndex += 1 # get the next trial reward
            break

def forcedTrial_blue(var, doo, dbc, mouse, myPoints):
    """
    A forced trial only draws the yellow circle, force the subject to take a risky option and will help the subject to sample more. 
    """
    var.rewmag = var.shortmag # set rewmag to be surebet (4)
    var.forced = 1
    var.stg = 3 # using the stage 3 setup for var.state loop
    while var.repeatstage: # repeat the current trial if any violations are made
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            getBluePos(var) # gets the position of the yellow circle
        var,doo,myPoints = draw_initCircle(var,doo,myPoints)
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = funcDic[var.state](var,doo,myPoints)
        if var.advancement == 1: # save it as stage 6 or 7
            var.stg = 6
        elif var.advancement == 2:
            var.stg = 7
        elif var.advancement == 3:
            var.stg = 8
        elif var.advancement == 4:
            var.stg = 9
        elif var.advancement == 5:
            var.stg = 10
        elif var.advancement == 6:
            var.stg = 11
        elif var.advancement == 7:
            var.stg = 12
        elif var.advancement == 8:
            var.stg = 13
        elif var. advancement == 9:
            var.stg = 14
        dataRecord3(var,dbc)
        var.stg = 3
        if again_or_next(var) == 'again': # if any violations made
            var.totalTrialCounter += 1 # plus 1 in totalTrialCounter
            var.repeatSet = True
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else: # if no violation made
            var.totalTrialCounter += 1 # plus 1 in totalTrialCounter
            var.trialCounter+=1 # plus 1 in trialCounter
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            var.repearSet = False
            var.rewForcedIndex += 1 # get the next trial reward
            var.sequenceIndex += 1 # get the next sequence trial
            break

def freeTrial(var, doo, dbc, mouse, myPoints):
    """
    A free trial draws both the blue and yellow circle and let's the subject decide what option to take.
    """
    var.forced = 0
    # extra check that the var.stg has been set to the right stage number
    if var.advancement == 1:
        var.stg = 6
    elif var.advancement == 2:
        var.stg = 7
    elif var.advancement == 3:
        var.stg = 8
    elif var.advancement == 4:
        var.stg = 9
    elif var.advancement == 5:
        var.stg = 10
    elif var.advancement == 6:
        var.stg = 11
    elif var.advancement == 7:
        var.stg = 12
    elif var.advancement == 8:
        var.stg = 13
    elif var.advancement == 9:
        var.stg = 14
    while var.repeatstage: # repeat the current trial if any violations are made
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            getBluePos(var) # gets var.staticPos for the blue circle
            var = symmetricYBPair(var) # gets var.staticPos for the yellow circle
            if var.schedule == "new_sound":
                var.rewmag = var.new_sound
            else:
                print("\nTrial: " + str(var.trialCounter))
                print("-----------------")
                print("var.shuffleFreeRew: "+ str(var.shuffleFreeRew))
                print("rewFreeIndex: " + str(var.rewFreeIndex))
                var.rewmag = var.shuffleFreeRew[var.rewFreeIndex] # set a predetermined rew magnitude
                print("var.rewmag: "+ str(var.rewmag))
            getHitmag(var) # gets var.shuffleRew[var.rewardGot]
            getProb_freeforced(var) # sets the probability clicking in the sound
        var,doo,myPoints = draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = funcDic[var.state](var,doo,myPoints)
        dataRecord_freeforced(var,dbc)
        if again_or_next(var) == 'again': # if any violations made
            var.totalTrialCounter += 1 # plus 1 in totalTrialCounter
            var.repeatSet = True
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else: # if no violation made
            var.totalTrialCounter += 1 # plus 1 in totalTrialCounter
            var.trialCounter+=1 # plus 1 in trialCounter
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            var.repearSet = False
            var.sequenceIndex += 1 # get the next sequence trial
            # Update the choice that the subject made and store it. 
            if var.shuffleFreeRew[var.rewFreeIndex] == 2: 
                var.bestChoice = 'b'
            else:
                var.bestChoice = 'y'
                var.firstOrderMistakes.append("no")

            if var.bestChoice == 'b':
                if var.choice != var.bestChoice:
                    var.firstOrderMistakes.append("yes")
                else:
                    var.firstOrderMistakes.append("no")

            # make the minMaxChoices list slide. 
            if var.advancement == 1:
                if len(var.firstOrderMistakes) > 10:
                    var.firstOrderMistakes.pop(0)
            elif var.advancement == 2:
                if len(var.firstOrderMistakes) > 15:
                    var.firstOrderMistakes.pop(0)
            elif var.advancement == 3:
                if len(var.firstOrderMistakes) > 20:
                    var.firstOrderMistakes.pop(0)
            elif var.advancement == 4 or var.advancement == 5 or var.advancement == 6 or var.advancement == 7 or var.advancement == 8 or var.advancement == 9:
                if len(var.firstOrderMistakes) > 30:
                    var.firstOrderMistakes.pop(0)

            if var.schedule != "new_sound":
                print("firstOrderMistakes: " + str(var.firstOrderMistakes))
            var.rewFreeIndex += 1
            break
