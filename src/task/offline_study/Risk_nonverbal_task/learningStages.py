# Learning stages for the  subjects who come the first time
#-------------------imports--------------------------------------------------------------------
import  os,gc, datetime
import newPoints,stage0,stage1,stage2,stage3,stage4,stage5,setup,variables,doodle
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
def learn(var,doo,myPoints,dbc,mouse): # main function of the learning stages for returning subjects
    fc.setpath() # set up directory
    #------------participant info collecting------------------------
    setup.dataCollectGui()
    var.expInfo = setup.username()
    gc.enable()
    #-------------database setup ------------------------------------
    fN = os.path.basename(__file__)
    p_num, expD, st, expN, host_ip,p_net = fc.get_netid(var,doo,dbc,fN)
    setiddtb,var = fc.initialSetup(var,dbc)
    #--------------------data start write-----------------------------
    sql.w_before_learning(dbc,p_num, expD, st, expN, host_ip, setiddtb)
    var.sessid = sql.r_lastID(dbc)

    # go through all stages and record number of coins earned and trials done in each stage
    # 4 correct trials in a row to pass each stage
    
    var = stage0.stage0(var.sessid,var,doo,myPoints,dbc,mouse)
    Points0,trials0 = fc.total_Points_trialCounter(var)
    fc.reset_Points_trialCounter(var)

    var = stage1.stage1(var.sessid,var,doo,myPoints,dbc,mouse)
    Points1,trials1 = fc.total_Points_trialCounter(var)
    fc.reset_Points_trialCounter(var)

    rewardG=var.rewardGot

    var = stage2.stage2(var.sessid,var,doo,myPoints,dbc,mouse)
    Points2,trials2 = fc.total_Points_trialCounter(var)
    fc.reset_Points_trialCounter(var)

    rewardG=rewardG+var.rewardGot

    var = stage3.stage3(var.sessid,var,doo,myPoints,dbc,mouse)
    Points3,trials3 = fc.total_Points_trialCounter(var)
    fc.reset_Points_trialCounter(var)

    rewardG=rewardG+var.rewardGot
    var.LearningFail = trials1/2+trials2/2+trials3/2

    #print var.rewardGot, rewardG, var.LearningFail,var.goodPokesInARoll
    if rewardG<var.LearningFail and var.goodPokesInARoll<4:
        print("Sorry, you did not pass learning")
        LearningStageTotalPoints = Points0+Points1+Points2+Points3
        ttrials = trials0+trials1+trials2+trials3
        et = datetime.datetime.now() # record end time
        sql.w_after_learningFail(dbc,var,p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb) # save data of this session in database
        doo.instruction.text = u'Sorry, you did not pass learning'
        doo.instruction.draw()
        setup.mywin.flip()
        core.wait(2)
        core.quit() 

    var = stage4.stage4(var.sessid,var,doo,myPoints,dbc,mouse) 
    Points4,trials4 = fc.total_Points_trialCounter(var)
    fc.reset_Points_trialCounter(var)

    var = stage5.stage5(var.sessid,var,doo,myPoints,dbc,mouse) 
    Points5,trials5 = fc.total_Points_trialCounter(var)
    fc.reset_Points_trialCounter(var)

    LearningStageTotalPoints = Points0+Points1+Points2+Points3+Points4+Points5
    ttrials = trials0+trials1+trials2+trials3+trials4+trials5

    fc.show_bigCoins_total(LearningStageTotalPoints,myPoints) # show the total profits to the subjects
    fc.end_instruction(doo) # give the ending instruciton to the subject
    et = datetime.datetime.now() # record end time
    sql.w_after_learningALL(dbc,var,p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb) # save data of this session in database
    return p_net

if __name__ == '__main__':
    learn(var,doo,myPoints,dbc,mouse) # call main function of learning stages for returning subjects