# this file contains all the SQL request calls
# functions starting with 'w' are executing/writing data into dtb
# functions starting with 'r' are query/reading data from dtb
import json

# select username in the database
def select_user(dbc,name):
    dbc.use(name)

# get subject id (p_num) given netid 
def r_subjid(dbc,p_net):
    return int(dbc.query("select subjid from subjinfo where netid = '%s'" %p_net)[0][0])

# get subject id (p_num) given sessid 
def r_subjidfromsessid(dbc,session):
    return int(dbc.query("select subjid from sessions where sessid = %s" %session)[0][0])

# get adaptstage (var.adaptstg) given netid 
def r_adaptstg(dbc,p_num):
    return int(dbc.query("select stage from risk_nv_adapt where id = (select max(id) from risk_nv_adapt where subjid = %s)" %p_num)[0][0])

# get freeforced advancement (var.advancement) given netid 
def r_freeforcedadvancement(dbc,p_num):
    return int(dbc.query("select advancement from risk_nv_freeforced where id = (select max(id) from risk_nv_freeforced where subjid = %s)" %p_num)[0][0])
def r_freeforcedadvancement(dbc,p_num):
    return int(dbc.query("select advancement from risk_nv_freeforced where id = (select max(id) from risk_nv_freeforced where subjid = %s)" %p_num)[0][0])

# get the status from subjid 
def r_stagestatusfromsubjid(dbc,p_num):
    return int(dbc.query("select stagestatus from risk_nv_freeforced where id = (select max(id) from risk_nv_freeforced where subjid = %s)" %p_num)[0][0])

# get adaptschedule(var.schedule) given netid 
def r_adaptsch(dbc,p_num):
    return dbc.query("select schedule from risk_nv_adapt where subjid = %s" %p_num)[0][0]

# get adaptschedule(var.schedule) for a new subject
def r_adaptsch0(dbc):
    sch0 = int(dbc.query("select count(distinct(subjid)) from risk_nv_adapt")[0][0])
    if sch0 % 2 == 0:
        schedule = 'A'
    else: 
        schedule = 'B'
    return schedule

# decide whether adapt stage 1 passed or failed (<10% first-order violations) Sliding window of 20 last trials
def r_adapt1pass(dbc,var):
    return int(dbc.query("select sum(x.choice) from (select choice, rewmag from trials where sessid = %s and choice is not null order by trialid desc limit 20) as x where x.rewmag = 2" %var.sessid)[0][0])

# decide which probability or reward to use first
def r_adaptprob1(dbc,var,i,rewmag):
    return dbc.query("select avg(x.choice) from (select choice, rewmag from trials where sessid = %s and stage = %s and choice is not null order by trialid desc limit 20) as x where x.rewmag = %s" %(var.sessid,i-1,rewmag))[0][0]

    return dbc.query("select avg(x.choice) from (select choice, rewmag from trials where sessid = %s and stage = %s and choice is not null order by trialid desc limit 20) as x where x.rewmag = %s" %(var.sessid,i-1,rewmag))[0][0]

# decide which reward to use first
def r_freetrialrew(dbc,var,i,rewmag, p_num):
    var.sessid_pre = dbc.query("select max(sessid) from  risk_nv_freeforced where subjid = %s and advancement = %s" %(p_num, var.advancementSQL))[0][0]
    print(var.sessid_pre)
    return dbc.query("select avg(x.choice) from (select choice, rewmag from trials where sessid = %s and stage = %s and choice is not null order by trialid desc limit 30) as x where x.rewmag = %s" %(var.sessid_pre,i,rewmag))[0][0]

def r_which_new_sound_8_12(dbc,var,i, rewmag, p_num):
    var.sessid_pre = int(dbc.query("select max(sessid) from  risk_nv_freeforced where subjid = %s" %p_num)[0][0])
    sound1 = dbc.query("select rewmag from trials where sessid = %s and stage = %s and forced = 0 and rewmag = %s and choice is not null order by trialid desc limit 30" %(var.sessid,i-1,rewmag))
    sound2 =dbc.query("select rewmag from trials where sessid = %s and stage = %s and forced = 0 and rewmag = %s and choice is not null order by trialid desc limit 30" %(var.sessid_pre,i-1,rewmag))
    if sound1 == [] and sound2 == []:
        return 8
    else:
        return 12

def r_which_new_sound_5_15(dbc,var,i, rewmag, p_num):
    var.sessid_pre = int(dbc.query("select max(sessid) from  risk_nv_freeforced where subjid = %s" %p_num)[0][0])
    sound1 = dbc.query("select rewmag from trials where sessid = %s and stage = %s and forced = 0 and rewmag = %s and choice is not null order by trialid desc limit 30" %(var.sessid,i-1,rewmag))
    sound2 =dbc.query("select rewmag from trials where sessid = %s and stage = %s and forced = 0 and rewmag = %s and choice is not null order by trialid desc limit 30" %(var.sessid_pre,i-1,rewmag))
    if sound1 == [] and sound2 == []:
        return 5
    else:
        return 15

# decide which probability or reward to use first if subject starts a new session from this stage
def r_adaptprob2(dbc,var,rewmag):
    # get previous sessid number
    sessid_pre = int(dbc.query("select max(sessid) from  risk_nv_adapt where subjid = (select subjid from risk_nv_adapt where sessid = %s) and sessid !=%s" %(var.sessid,var.sessid))[0][0])
    # get average choice for specific reward magnitude and last 20 trials of the previous session
    return dbc.query("select avg(x.choice) from (select choice, rewmag from trials where sessid = %s and choice is not null order by trialid desc limit 20) as x where x.rewmag = %s" %(sessid_pre,rewmag))[0][0]

# decide whether to repeat an adapt stage
def r_adaptprob3(dbc,var,rewmag,prob):
    if rewmag == 0:
        avgchoice = dbc.query("select avg(x.choice) from (select choice, probability from trials where sessid = %s and choice is not null order by trialid desc limit 20) as x where x.probability = %s" %(var.sessid,prob))[0][0]
    elif prob == 0:
        avgchoice = dbc.query("select avg(x.choice) from (select choice, rewmag from trials where sessid = %s and choice is not null order by trialid desc limit 20) as x where x.rewmag = %s" %(var.sessid,rewmag))[0][0]
    else:
        avgchoice = dbc.query("select avg(x.choice) from (select choice, rewmag, probability from trials where sessid = %s and choice is not null order by trialid desc limit 20) as x where x.rewmag = %s and x.probability = %s" %(var.sessid,rewmag,prob))[0][0]
    # get average choice for specific reward magnitude and last 20 trials of the previous session
    return avgchoice

# decide whether to repeat an adapt stage
def r_adaptprob_nv(dbc,var):
    # get previous sessid number
    sessid_pre = int(dbc.query("select max(sessid) from sessions_end where subjid = (select subjid from sessions where sessid = %s)" %(var.sessid))[0][0])
    # get average choice for specific reward magnitude and last 20 trials of the previous session
    return dbc.query("select avg(x.choice) from (select choice, rewmag from trials where sessid = %s and choice is not null order by trialid desc limit 30) as x where x.rewmag != 2" %(sessid_pre))[0][0]


# get settingsid with given info
def r_settingsid(dbc,settingsdtb):
    return int(dbc.query("select settingsid from settings where description = '%s'" %settingsdtb)[0][0])

# get variables from given setting
def r_varset(dbc,settingsdtb):
    return json.loads(dbc.query("select data from settings where description = '%s'" %settingsdtb)[0][0])

# get the last inserted sessid
def r_lastID(dbc):
    return dbc.query('select last_insert_id()')[0][0]# added [0][0] here

# session number from risk_nv_adapt
def r_numses(dbc,subjid):
    return dbc.query('select count(distinct(sessid)) from risk_nv_adapt where subjid =%s'%(subjid)[0][0])

def r_distinct_sessions(dbc, subjid):
    print(subjid)
    i = dbc.query("select count(distinct(sessid)) from sessions_end where subjid = %s order by sessid desc"%(subjid))
    return i[0][0]

def r_advancement8_trials(dbc, sessid):
    return dbc.query("SELECT rewmag, choice FROM trials a, sessions b WHERE stage = 13 and forced = 0 AND choice is not null and a.sessid = b.sessid and subjid = %s"%(sessid))

# record session info before a learning stages session in the session table
def w_before_learning(dbc,p_num, expD, st, expN, host_ip, setiddtb):
    dbc.execute('insert into sessions (subjid, sessiondate, starttime, treatment, hostip, settingsid) values (%s, %s, %s, %s, %s, %s)',(p_num, expD, st, expN, host_ip, setiddtb))

# record data of one trial after the trial for learning stages
def w_after_LearningStages(dbc,var,sd):
    if var.stg <= 2:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.points))
    elif var.stg == 3:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points, smag) values (%s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.points, var.shortmag))
    elif var.stg == 4:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, points) values (%s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.rewmag, var.points))
    elif var.stg == 45:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, points) values (%s, %s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, 45, var.rewmag, var.probmag, var.points))
    elif var.stg == 6 or var.stg == 7 or var.stg == 8 or var.stg == 9 or var.stg == 10 or var.stg == 11 or var.stg == 12 or var.stg == 13 or var.stg == 14:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, points, forced) values (%s, %s, %s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.rewmag, var.probmag, var.points, var.forced))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, points) values (%s, %s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.rewmag, var.probmag, var.points))

# record session info after a learning stages session in the sessions_end table
def w_after_learningALL(dbc,var,p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(var.sessid, p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb))

# record session info after learning failed in the sessions_end table
def w_after_learningFail(dbc,var,p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid, learning) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(var.sessid, p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb, 'fail'))

# record forced-free experiment at the start of the session
def w_after_freeforced(dbc, var, p_num, expD):
    dbc.execute('insert into risk_nv_freeforced (subjid, sessid, recordtime, advancement, stagestatus, stageduration) values (%s, %s, %s, %s, %s, %s)',(p_num, var.sessid, expD, var.advancement, var.stagestatus , var.stageduration))

# record adapt stage at the start of the session
def w_before_adaptstage(dbc, var, p_num):
    dbc.execute('insert into risk_nv_adapt (subjid, sessid, schedule, stage, stagestatus) values (%s, %s, %s, %s, %s)',(p_num, var.sessid, var.schedule, var.adaptstg, 'start'))
# record next earned adapt stage within the session
def w_next_adaptstage(dbc, var, p_num):
    dbc.execute('insert into risk_nv_adapt (subjid, sessid, schedule, stage, stagestatus) values (%s, %s, %s, %s, %s)',(p_num, var.sessid, var.schedule, var.adaptstg, 'start'))

# record for the previous stage when it is passed
def w_pass_adaptstage(dbc, var, p_num, status):
    if status == 'pass':
        dbc.execute('insert into risk_nv_adapt (subjid, sessid, schedule, stage, stagestatus, repeattimes) values (%s, %s, %s, %s, %s, %s)',(p_num, var.sessid, var.schedule, var.adaptstg, 'pass', var.repeattime))
    else:
        p_num = r_subjidfromsessid(dbc,var.sessid)
        dbc.execute('insert into risk_nv_adapt (subjid, sessid, schedule, stage, stagestatus, repeattimes) values (%s, %s, %s, %s, %s, %s)',(p_num, var.sessid, var.schedule, var.adaptstg, status, var.repeattime+1))


# record data of one trial after the trial for adapt stages session
def w_after_adapttrial(dbc,var,sd):
    if var.initWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.adaptstg, var.points))
    elif var.fixWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.adaptstg, var.points))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, choice, points, smag) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.adaptstg, var.yrewmag, var.probmag, var.ychoice, var.points, var.shortmag))

# record data of one trial after the trial for risknv session
def w_after_risknvtrial(dbc,var,sd):
    if var.initWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.adaptstg, var.points-var.adaptpoints))
    elif var.fixWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.adaptstg, var.points-var.adaptpoints))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, choice, points, smag) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.adaptstg, var.yrewmag, var.probmag, var.ychoice, var.points-var.adaptpoints, var.shortmag))

# record data of one trial after the trial for freeforced session
def w_after_freeforcedtrial(dbc,var,sd):
    if var.initWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.points))
    elif var.fixWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.points))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, choice, points, smag, forced) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.yrewmag, var.probmag, var.ychoice, var.points, var.shortmag, var.forced))

# record session info after adapt1 failed in the sessions_end table
def w_after_adapt1Fail(dbc,var,et):
    # get session info
    p_num = r_subjidfromsessid(dbc,var.sessid)
    expD = dbc.query("select sessiondate from sessions where sessid = %s" %var.sessid)[0][0]
    expN = dbc.query("select treatment from sessions where sessid = %s" %var.sessid)[0][0]
    host_ip = dbc.query("select hostip from sessions where sessid = %s" %var.sessid)[0][0]
    setiddtb = dbc.query("select settingsid from sessions where sessid = %s" %var.sessid)[0][0]
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid, learning) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',(var.sessid, p_num, expD, et, expN, host_ip, var.trialCounter, var.points, setiddtb, 'fail'))

def w_after_adapt(dbc,var,et):
    #get session info
    p_num = r_subjidfromsessid(dbc,var.sessid)
    expD = dbc.query("select sessiondate from sessions where sessid = %s" %var.sessid)[0][0]
    expN = dbc.query("select treatment from sessions where sessid = %s" %var.sessid)[0][0]
    host_ip = dbc.query("select hostip from sessions where sessid = %s" %var.sessid)[0][0]
    setiddtb = dbc.query("select settingsid from sessions where sessid = %s" %var.sessid)[0][0]
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(var.sessid, p_num, expD, et, expN, host_ip, var.mergedTrialCounter, var.points, setiddtb))

def w_after_risknv(dbc,var,et):
    #get session info
    p_num = r_subjidfromsessid(dbc,var.sessid)
    expD = dbc.query("select sessiondate from sessions where sessid = %s" %var.sessid)[0][0]
    expN = dbc.query("select treatment from sessions where sessid = %s" %var.sessid)[0][0]
    host_ip = dbc.query("select hostip from sessions where sessid = %s" %var.sessid)[0][0]
    setiddtb = dbc.query("select settingsid from sessions where sessid = %s" %var.sessid)[0][0]
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(var.sessid, p_num, expD, et, expN, host_ip, var.trialCounter, var.points-var.adaptpoints, setiddtb))


# record session info before a mixnv or adapt session in the session table
def w_before_mixnon(dbc,p_num, expDate, stt, expName, host_ip, setiddtb):
    dbc.execute('insert into sessions (subjid, sessiondate, starttime, treatment, hostip, settingsid) values (%s, %s, %s, %s, %s, %s)',(p_num, expDate, stt, expName, host_ip, setiddtb))

# record data of one trial after the trial for mixNonverbal session
def w_after_Mixnon(dbc,var,sessid,sd):
    if var.initWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.points))
    elif var.fixWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.points))
#    elif var.choiceWrong:
#        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, points, smag) values (%s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.rewmag, var.blockProbMag, var.points, var.shortmag))
#    elif var.rewWrong:
#        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, points, smag) values (%s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.yrewmag, var.blockProbMag, var.points, var.shortmag))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, probability, choice, points, smag) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.yrewmag, var.blockProbMag, var.ychoice, var.points, var.shortmag))

# record session info after a mixNonverbal session in the sessions_end table
def w_after_mixNonALL(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',\
            (sessid, p_num, expDate, endt, expName, host_ip, var.trialCounter, var.points, setiddtb))

