# learning stage 4 : learn to click in yellow circle to get larger reward and learn to associate pitch with reward magnitude
import functions as fc

#--------------------------Main Code--------------------------------
def stage4(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart4(var,dbc)
    var.stg = 4 # specify number of stage
    var.goodPokesInARoll = 0 # reset counter
    var.rewardGot = 0
    var.sessid = session # specify sessid
    highlowIndex = 0 # make high low reward mag index start from 0
    var = fc.makeHighLowRew(var) # generate a high & low (6 in total) reward list
    # the min and max reward mag trial block (6 trials)
    while var.rewardGot < var.highLowTrialNum:
        var.forcedTrial = True # set a boolean for later use
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            #var = fc.getFixmag(var)
            fc.getYellowPos(var)
            var = fc.getHighLowRew(var,highlowIndex)
            var = fc.getInitStimDis(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord4(var,dbc) # record data
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
            var.forcedTrialCounter+=1 # plus 1 in forcedTrialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # plus 1 in mergedTrialCounter (will be reset to 0 after min-max block)
            highlowIndex+=1 # proceed to next high & low reward mag
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
    var.forcedTrial = False # after forced trials, set this to False
    var.mergedTrialCounter = 0 # reset mergedTrialCounter
    
    # the ordered trials (10 trials)
    var.forcedTrial = True # boolean for forced trials
    inc = True
    while var.rewIndex <= len(var.mag) and var.rewIndex >= 0: # go through all the ordered forced trials
        if not var.repeatSet: # if no violation made in last trial
            if var.rewIndex < len(var.mag)-1: # let reward magnitude vary from 1 to 10 and back to 1
                fc.getRewmag(var)
            else:
                inc = False
                fc.getRewmag(var)
            if inc:
                var.rewIndex +=1
            else:
                var.rewIndex -=1
            # get variables for the new trial 
            #fc.getFixmag(var)
            fc.getYellowPos(var)
            fc.getInitStimDis(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord4(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1  # plus 1 in mergedTrialCounter (will be reset to 0 after orderly forced block)
            var.repeatSet = True # next trial with the same setting
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else:
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after orderly forced block)
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
    var.forcedTrial = False # after forced trials, set this to False
    var.mergedTrialCounter = 0 # resert mergedTrialCounter
            
    # normal trials (20 correct to pass)
    while var.trialCounter < var.trial: # run given number of trials
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            #fc.getFixmag(var)
            fc.getYellowPos(var)
            fc.getHitmag(var)
            fc.getInitStimDis(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord4(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after normal block)
            #var.mergedTrialCounter+=1 # not in used here
            var.repeatSet = True # next trial will use the same setting
            #var.goodPokesInARoll = 0 # reset goodPokesInARoll to 0
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter(normal trials)
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after normal block)
            var.fixation_clicks = []# reset fixation_clicks record list
            var.decision_clicks=[]
            var.reward_clicks=[]# reset reward_clicks record list
        if fc.passStage45Test(var) == 'pass':# if this stage is passed, break the loop
            break
    var.mergedTrialCounter = 0 # resert mergedTrialCounter
    fc.show_bigCoins(var,myPoints) # show total coins earned
    return var

if __name__ == "__main__":
    stage4(var.sessid,var,doo,myPoints,dbc) # call main function