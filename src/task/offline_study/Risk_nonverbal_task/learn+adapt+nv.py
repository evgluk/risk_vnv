# leaning stages + adaptive stages + Mixnonverbal task
#-------------------imports--------------------------------------------------------------------
import learningStages_n, adaptiveStages, risknv, doodle, setup, datetime, time, os, gc, newPoints, variables
from psychopy import core,event, visual
import functions as fc
import SQL_call as sql
#-------------make necessary objects------------------------------
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)
#--------------------------Main Code--------------------------------
def main(var,doo,myPoints,dbc,mouse):
    #------------participant info collecting------------------------
    fN = os.path.basename(__file__)
    setup.dataCollectGui(fN)
    var.expInfo = setup.username()
    gc.enable()
    p_net = (var.expInfo['Net ID'])
    var.adaptstg, var.schedule = fc.checkadapt(var,dbc,doo,p_net)
    # if adaptstg == 0 assign schedule A or B based on previous entry (odd number of distinct subject IDs - B, even - A)
    print var.adaptstg, var.schedule 
    if var.adaptstg == 0:
        print("new subject")
        learningStages_n.learn(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
        fc.break_instruction(doo)
        var.adaptstg = 1
        adaptiveStages.adapt(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
        #var.nvTimeout = 150 # 150 for all sessions
        print var.totalTrialCounter, var.points, var.nvTimeout
        var.adaptpoints = var.points
        # nv without blocks dependent on subject
        risknv.mixnv(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
    else:
        p_num = sql.r_subjid(dbc,p_net)
        numsess = sql.r_numses(dbc,p_num)+1 # current session
        print numsess
        if numsess==4:
            #print numsess
            #print ("add 1 everywhere")
            var.allplus1 = True
            adaptiveStages.adapt(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
            var.adaptpoints = var.points
            # nv without blocks dependent on subject
            risknv.mixnv(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
        elif numsess>=5:
            print numsess
            print ("10 nv trials")
            var.allplus1 = False
            var.trials10 = True
            var.adaptpoints = 0
            risknv.mixnv(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
        else:
            #print numsess
            # check schedule A or B
            adaptiveStages.adapt(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
            #print var.totalTrialCounter, var.points, var.nvTimeout
            var.adaptpoints = var.points
            # nv without blocks dependent on subject
            risknv.mixnv(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)

if __name__ == '__main__':
    main(var,doo,myPoints,dbc,mouse) # call main function