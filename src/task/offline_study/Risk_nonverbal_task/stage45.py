# learning stage 4-5 merged : learn to click in yellow circle to get reward with 50% probability
# (just min and max magnitudes)
import functions as fc

#--------------------------Main Code--------------------------------
def stage45(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart5(var,dbc)
    var.stg = 45 # specify number of stage
    var.goodPokesInARoll = 0 # reset counter
    var.rewardGot = 0
    var.sessid = session # specify sessid
    highlowIndex = 0 # make high low reward mag index start from 0
    var = fc.makeHighLowRew_freeforced(var) # generate a high & low reward list
    passStage45 = False # variable only necessary for the risk_nv_freeforced.py task
    # the min and max reward mag trial block (12 trials)
    while var.rewardGot < var.highLowTrialNum_n and var.timer.getTime() > 0: # highLowTrialNum_n should be equal to the size of the highLowReward list. 
        var.forcedTrial = True # set a boolean for later use
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            #var = fc.getFixmag(var)
            fc.getYellowPos(var)
            var = fc.getHighLowRew(var, highlowIndex)
            var = fc.getInitStimDis(var)
            var.probmag = var.prob50 # set the reward probability to 50%
            var.sndprobmag = 4  
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord5(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.forcedTrialCounter+=1 # plus 1 in forcedTrialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # plus 1 in mergedTrialCounter (will be reset to 0 after min-max block)
            var.repeatSet = True # next trial will use the same init position
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else:
            var.trialCounter+=1 # plus 1 in trialCounter(normal trials)
            var.forcedTrialCounter+=1 # plus 1 in forcedTrialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # plus 1 in mergedTrialCounter (will be reset to 0 after min-max block)
            highlowIndex+=1 # proceed to next high & low reward mag
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
    var.forcedTrial = False # after forced trials, set this to False
    var.mergedTrialCounter = 0 # resert mergedTrialCounter
    passStage45 = True

    return var, passStage45

if __name__ == "__main__":
    stage45(var.sessid,var,doo,myPoints,dbc) # call main function