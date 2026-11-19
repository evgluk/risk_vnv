# adaptive decision stages: start with min & max rewards and 50% probability 
# (A) - add middle magnitude; (B) - add probability
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
def adapt(var,doo,myPoints,dbc,mouse,getName=True,sub_id=None):
    fc.setpath() # set up directory
    fN = os.path.basename(__file__) # get expName of this file
    expName, extN = os.path.splitext(fN) # get expName and extN
    expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S") # get time
    var.sessid,p_num,p_net,setiddtb,host_ip,var,dbc = fc.exp_setup_n(var,doo,dbc,getName,sub_id,expName,expDate) # database setup and data start recording
    if var.adaptstg==6:
        var.adaptstg=5 # for version 3
    #print var.adaptstg
    sql.w_before_adaptstage(dbc, var, p_num)
    # the first adaptation stage is the same for all subjects (random predetermined)
    for i in range(var.adaptstg,6): # change from 7
        var.repeatstage = True
        var.repeattime = 0
        while var.repeatstage:
            nv.decisionstage(var,doo,myPoints,dbc,mouse,i)
            # check if repeat adapt stage or go further
            fc.again_or_next_stage2(dbc,var)
            var.repeattime+=1
        # save once new adapt level acquired
        if var.adaptstg<5: # change from 6
            sql.w_pass_adaptstage(dbc, var, p_num, 'pass')
            var.adaptstg+=1
            print var.adaptstg, i, var.repeattime
            sql.w_next_adaptstage(dbc, var, p_num)
    var.dataFile.close() # close the data file
    endt = datetime.datetime.now() # record end time
    sql.w_after_adapt(dbc,var,endt) # save the data of this session to database
    return var


if __name__ == "__main__":
    adapt(var,doo,myPoints,dbc,mouse) # run main function