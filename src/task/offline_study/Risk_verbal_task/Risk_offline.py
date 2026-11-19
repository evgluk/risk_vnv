#Risk task used in offline condition
#--------------import stuff----------------------------------------
import  os, datetime, copy, random
import newPoints,setup,variables,doodle
from psychopy import event
import functions as fc
#import SQL_call as sql
#------------make objects----------------------
# these objects won't be made if the file is called from another file
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
#dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)
#--------------------------Main Code--------------------------------
def Risk_offline(var,doo,myPoints,mouse,getName=True,sub_id=None,pre_points=0,gettrialn=0,pre_trials=0):
    var.trialCounter = pre_trials
    var.rewardGot = gettrialn
    var.points = pre_points # if it's the second risk session in the experiment, points are accumulated from the first long verbal session
    var.Risk = True # specify risk for specific functions
    fc.setpath() # set up directory
    fN = os.path.basename(__file__) # get expName of this file
    expName, extN = os.path.splitext(fN) # get expName and extN
    stageName = expName[:-8] # get stageName
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")# get expDate
    p_num,setiddtb, var, expName = fc.exp_setup_risk_nointernet(var,doo,getName,sub_id,expName,expDate) # setup without dtb csv data start recording
    var.verbalTotalTrial=15 #demo value
    var.pay = fc.paymentSelection(var.verbalTotalTrial)+gettrialn # select one trial(number) to actually pay the subject 
    setupList = fc.verbalSetup(var.verbalTotalTrial,var.mag,var.shortmag)  # demo setup the reward of blocks for the whole experiment
    shuffledSetupList = copy.copy(setupList)# shuffle the reward list
    random.shuffle(shuffledSetupList)
    fc.stage_instruction_off(stageName,var,doo) # show subjects stage name (long delay)
    for i in range(len(shuffledSetupList)): # apply a reward mag for each block
        var.blockRewMag = shuffledSetupList[i][0] # assign reward mag for this block
        var.blockName = i+1 # assign blockName
        var.rewmag = var.blockRewMag # assign reward mag
        fc.block_instruction_off(var,doo) # show block instruction to the subject
        while var.blockTrialCounter < shuffledSetupList[i][1]: # run pre-determined number of trials in each block 
            #if not var.sameInitPos: # get a new setup if no violation made in the last trial
            var = fc.new_trial_setup_risk(var)
            var,doo,myPoints = fc.draw_init_off(var,doo,myPoints) # start the first state
            while var.state != 'none': # go through all connected states in one trial
                #mouse.clickReset()
                var,doo,myPoints = fc.funcDic_risk_off[var.state](var,doo,myPoints)
            if fc.again_or_next(var) == 'again': # if any violations made
                var.trialCounter+=1 # plus 1 in trialCounter
                var.sameInitPos = True # next trial will use the same init position
                var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
                var.prob_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
                again = True
            else: # if no violation made
                var.rewardGot += 1  # plus 1 in rewardGot 
                var.trialCounter+=1 # plus 1 in trialCounter (total trial num)
                var.blockTrialCounter += 1  # plus 1 in blockTrialCounter (trial num in current block)
                var.pairNum+=1 # proceed to next pair
                var.reward_clicks=[]# reset reward_clicks record list
                var.prob_clicks=[] # reset prob_clicks(records the clicks during delay waiting time) list
                again = False
            if var.rewardGot == var.pay and again == False: # assign pay_delay and pay_num if the current trial is the one picked to be actually paid
                if var.choice!='b':
                    var.pay_prob = var.probmag
                else:
                    var.pay_prob = var.sure_rwd
                var.pay_num = var.rewmag
                var.GetaNum = random.randint(1,100)# get a random number between 1 to 100
                if var.GetaNum <= var.pay_prob: #Decide to if give reward based on given probability
                    var.reward_give = True
            fc.dataRecord_risk_off(var, p_num, expName) # record data for this trial
            fc.resetVar(var,again)
        var.blockTrialCounter = 0 # reset blockTrialCounter
    var.dataFile.close() # close the data file
    var.longVerbal = False # reset longVerbal boolean to be False
    endt = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S") # record end time
    fc.sessiondataRecord_risk_off(var,p_num,expName,expDate,endt,setiddtb)
    #sql.w_after_Verbal(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb) # save data of this session in database
    return p_num, var.pay, var.pay_delay, var.pay_num, var.trialCounter,var.points,

if __name__ == "__main__":
    Risk_offline(var,doo,myPoints,mouse) # run main function