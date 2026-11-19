# decision stage: adaptive or mixed nonverbal
#-------------------imports--------------------------------------------------------------------
import  os,gc, datetime, copy, random
import newPoints,setup,variables,doodle
from psychopy import event, core
import functions as fc
import SQL_call as sql
#-------------make necessary objects------------------------------
# generate objects for coins, variables, drawings, database connect, and mouse
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)
#--------------------------Main Code--------------------------------
def decisionstage(var,doo,myPoints,dbc,mouse,i):
    var.stg = 6 # specify stage number ( assign stage #6 for mixnonverbal)
    var.rewardGot = 0
    # setup decision list: adapt stage 1: random predetermined
    if i == 1:
        var.shufflePos = var.shufflePosadapt1
        var.shuffleRew = var.shuffleRewadapt1
        var.shuffleProb = var.shuffleProbadapt1
        var.shuffleProbDraw = var.shuffleProbDrawadapt1
        var.adaptTrial = 100
    else:
        if i < 5: #changed from 6
            var.adaptTrial = 20 # changed from 20
        else:
            var.adaptTrial = 30 # changed from 30, 5 rewmag values with 3 probabilities -> version 3: 2 probabilities
        # run a function to create shuffle a list for each of above
        var.shufflePos,var.shuffleRew,var.shuffleProb,var = fc.setshuffleList2(var,dbc,i)
    while var.rewardGot < var.adaptTrial:
        #print var.shuffleRew, var.shuffleProb
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            fc.getBluePos(var) # gets var.shufflePos[var.rewardGot]
            var = fc.symmetricYBPair(var)  # gets symmetric yellow position
            fc.getHitmag(var) # gets var.shuffleRew[var.rewardGot]
            fc.getProb(var) # gets var.shuffleProb[var.rewardGot]
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord_adapt_nv(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.mergedTrialCounter+=1 # total (correct and incorrect) in adaptstages
            var.repeatSet = True # next trial will use the same init position
            var.fixation_clicks = []# reset fixation_clicks record list
            var.decision_clicks=[]
            var.reward_clicks=[]# reset reward_clicks record list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter (total trial num)
            var.totalTrialCounter+=1 # total correct in adapt stages
            var.mergedTrialCounter+=1 # total (correct and incorrect) in adaptstages
            var.fixation_clicks = []# reset fixation_clicks record list
            var.decision_clicks=[]
            var.reward_clicks=[]# reset reward_clicks record list
        if i == 1 and var.rewardGot >=20:
            print var.rewardGot
            print("it's 20 or more trials")
            # do the check, only those who do <10% first-order violations can continue with sliding window till max of 50 trials
            # (20 trials, so if more than 2 trials first-order - subject fails)
            if sql.r_adapt1pass(dbc,var)>2 and var.rewardGot<100:
                print("one more trial")
                continue
            elif sql.r_adapt1pass(dbc,var)<=2 and var.rewardGot<100:
                print("adapt stage 1 passed")
                break
            print("THE END")
            et = datetime.datetime.now() # record end time
            sql.w_pass_adaptstage(dbc, var, 0, 'fail')
            sql.w_after_adapt1Fail(dbc,var,et) # save data of this session in database
            fc.show_bigCoins(var,myPoints) # show the total profits to the subjects
            var.dataFile.close() # close the data file
            fc.end_instruction_timeout(doo) # give the ending instruction to the subject
        if var.totalTrialCounter >= 150: #changed from 150
            sql.w_pass_adaptstage(dbc, var, 0, 'timeout')
            print var.totalTrialCounter
            fc.show_bigCoins(var,myPoints) # show the total profits to the subjects
            var.dataFile.close() # close the data file
            endt = datetime.datetime.now() # record end time
            sql.w_after_adapt(dbc,var,endt) # save the data of this session to database
            fc.end_instruction_timeout(doo) # give the ending instruction to the subject
            
    var.trialCounter = 0 # reset adapt stage trial counter to 0