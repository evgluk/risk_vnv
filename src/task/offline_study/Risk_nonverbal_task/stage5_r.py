# learning stage 5_r : learning stage5 for returning subjects. Just random rewmag/probality trials
import functions as fc

#--------------------------Main Code--------------------------------
def stage5_r(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart5(var,dbc)
    var.stg = 5 # specify number of stage
    var.sessid = session
    var.rewardGot = 0 # reset rewardGot to 0
    var.goodPokesInARoll = 0 # reset counter
    # normal trials (20 trials correct to pass)
    while var.trialCounter < var.trial: # run given number of trials
        if not var.repeatSet: # get a new setup if no violation made in the last trial
            #fc.getFixmag(var)
            fc.getYellowPos(var)
            fc.getHitmag(var)
            fc.getProb(var)
            fc.getInitStimDis(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord5(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            #var.trialCounter+=1 # plus 1 in trialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after normal block)
            var.repeatSet = True # next trial will use the same init position
            #var.goodPokesInARoll = 0 # reset goodPokesInARoll to 0
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.decision_clicks=[]
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter
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
    stage5_r(session,var,doo,myPoints,dbc,mouse) # call main function