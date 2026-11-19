# decision stages: dependent on the adapt stage 6
#-------------------imports--------------------------------------------------------------------
import  os, datetime, copy, random
import newPoints,setup,variables,doodle, nv
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
def mixnv(var,doo,myPoints,dbc,mouse,getName=True,sub_id=None):
    var.stg = 6 # specify stage number ( assign stage #6 for mixnonverbal)
    var.rewardGot = 0
    fc.setpath() # set up directory
    fN = os.path.basename(__file__) # get expName of this file
    expName, extN = os.path.splitext(fN) # get expName and extN
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S") # get time
    var.sessid,p_num,p_net,setiddtb,host_ip,var,dbc = fc.exp_setup_n(var,doo,dbc,getName,sub_id,expName,expDate) # database setup and data start recording
    # run a function to create and shuffle a list for each of above
    var.shufflePos,var.shuffleRew,var.shuffleProb,var = fc.setshuffleList_nv2(var,dbc)
    print var.nvTrial
    while var.rewardGot < var.nvTrial: # 170
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
        fc.dataRecord_risknv(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.mergedTrialCounter+=1 # total (correct and incorrect) in risknv (and adapt)
            var.repeatSet = True # next trial will use the same init position
            var.fixation_clicks = []# reset fixation_clicks record list
            var.decision_clicks=[]
            var.reward_clicks=[]# reset reward_clicks record list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter (total trial num)
            var.totalTrialCounter+=1 # total in adapt stages and risknv
            var.mergedTrialCounter+=1 # total (correct and incorrect) in riskv (and adaptstages)
            var.fixation_clicks = []# reset fixation_clicks record list
            var.decision_clicks=[]
            var.reward_clicks=[]# reset reward_clicks record list
        if var.totalTrialCounter >= var.nvTimeout: #150 for first time / 150 (V3) for >>
            print var.totalTrialCounter
            fc.show_bigCoins(var,myPoints) # show the total profits to the subjects
            var.dataFile.close() # close the data file
            endt = datetime.datetime.now() # record end time
            sql.w_after_risknv(dbc,var,endt) # save the data of this session to database
            fc.end_instruction_timeout(doo) # give the ending instruction to the subject
    fc.show_bigCoins(var,myPoints) # show the total profits to the subjects
    var.dataFile.close() # close the data file
    endt = datetime.datetime.now() # record end time
    sql.w_after_risknv(dbc,var,endt) # save the data of this session to database
    fc.end_instruction_mixNon(doo) # give the ending instruction to the subject
    return var


if __name__ == "__main__":
    mixnv(var,doo,myPoints,dbc,mouse) # run main function