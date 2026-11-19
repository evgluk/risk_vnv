# -*- coding: utf-8 -*-
 # -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 13:34:24 2019
@Description: Learning stages for the subjects who come the first time. Tasks are without text
and simplified. 
"""

#-------------------imports--------------------------------------------------------------------
from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame'] # sets pygame as the preffered sound library, needed to be able to use .play(loops = ...)
import  os,gc, datetime, random
from datetime import timedelta 
import newPoints,setup,variables,doodle, stage0, stage1, stage2, stage3, stage45
from psychopy import event, core
import functions as fc
import SQL_call as sql
import numpy as np
import pandas as pd

#-------------make necessary objects from other python files -----------------------------------
myPoints = newPoints.NewPoints() # a class that draws everything about the coins shown in the experiments
var = variables.Variables() # this class defines all the common variables needed in the whole experiment
doo = doodle.Doodle() # a class that does most of the drawing in the experiment
dbc = fc.dbconnect() # a function to connect to the database
mouse = event.Mouse(setup.mywin) # the setup file creates the window for all the stimuli and initializes the mouse object.

#-------------Create dataframe to hold data for advancements 5-8 -----------------------------------
# Getting the data every trial from the MySQL database to check the criteria results in delays in the task

#--------------------------Main Code-------------------------------------------------------------
def risk_nv_freeforced(var,doo,myPoints,dbc,mouse, getName = True, sub_id = None):

	fc.setpath() # set up directory for Mac or Window users. 
	gc.enable() # enabling python's automatic garbage collector, attempts to reclaim garbage, or memory occupied by objects that are no longer in use by the program.
	fN = os.path.basename(__file__) # os.path.basename is used to return the file name from the given path. 
	#------------Get date/time -----------------------------------
	expName, extN = os.path.splitext(fN) # get expName (name of the experiment) and extN (t)
	expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S") # get time
	#------------Get Participant Information -----------------------------------
	# New participants are added to the subject info database before participating in any experiment
	var.sessid,p_num,p_net,setiddtb,host_ip,var,dbc, start_time = fc.exp_setup_freeforced(var,doo,dbc,getName,sub_id,expName,expDate) # Check if participant is in the database and get necessary information.
	try: # try to get the latest stage the participant is on 
		var.advancement = sql.r_freeforcedadvancement(dbc,p_num) # Check which learning/freeforced stage the participant has advanced towards. 
		print("returning subject")
		var.session_time = 1500 # in seconds, 25 min
	except: # participant is not in the database
		var.advancement = 0 # start from 0, learning stage
		print("new subject")
		var.session_time = 1200 # in seconds, 20 min
		# Instructions
		doo.instruction.text = 'Welcome Everyone!\n\nThe first order of business is to sign the informed consent form.\nIf you have not already done that, could you raise your hand and we will get it to you.\
		\n\nPress the spacebar to continue.'
		doo.instruction.draw()
		setup.mywin.flip()
		event.waitKeys(keyList="space")
		doo.instruction.text = 'You should know that everyone here has been recruited in the same way. Also there is no deception involved in this experiment.\nEverything that we tell you is true. This is the standard practice in economics.\
		\n\nPress the spacebar to continue.'
		doo.instruction.draw()
		setup.mywin.flip()
		event.waitKeys(keyList="space")
		doo.instruction.text = 'We would like you to play the game and earn coins. You will earn 30 RMB just for participation. Coins you earn will be converted to RMB at the following rate: 1 coin = 0.05 RMB. In the game do not rush. Take your time to make decisions. Thank you!\
		\n\nPress the spacebar to start the game.'
		doo.instruction.draw()
		setup.mywin.flip()
		event.waitKeys(keyList="space")

#===================SESSION START===================

	#Press the spacebar to start the experiment.

	# if sql.r_stagestatusfromsubjid(dbc,p_num) == "PASS":
	# 	print("Previous sessid: " + str(p_num))
	# 	var.advancement = sql.r_freeforcedadvancement(dbc,p_num)
	# 	print("Passed advancement: " + str(var.advancement))
	# 	var.advancement += 1
	# 	print("New advancement: " + str(var.advancement))
	# elif sql.r_stagestatusfromsubjid(dbc,p_num) == "FAIL":
	# 	print("Previous sessid: " + str(p_num))
	# 	var.advancement = sql.r_freeforcedadvancement(dbc,p_num)
	# 	print("Passed advancement: " + str(var.advancement))
	# 	var.advancement -= 1
	# 	print("New advancement: " + str(var.advancement))

	var.timer = core.CountdownTimer(var.session_time) # create Countdowntime of 1200 seconds (20min) or 1800 seconds (30min) 
	var.sequenceIndex = 0 # index for to keep looping through the sequenceList (force-force-free)
	session = True
	var.probIndex = 1 # set standard to prob 0.5
	while session: 
		#===================LEARNING STAGES START===================
		if var.advancement == 0:
			expDate, start_time = fc.reset_variables(var)
			#--------------------Stage 0: Reward-------------------------------
			# learning stage 0 : learn to click the reward port for getting reward
			var = stage0.stage0(var.sessid,var,doo,myPoints,dbc,mouse) # if countdown timer reaches zero, the while loop in stage0.py will terminate
			var.points0,var.trials0 = fc.total_Points_trialCounter(var)
			fc.reset_Points_trialCounter(var)
			if var.timer.getTime() < 0:
				fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)
				break 

			#--------------------Stage 1: Start Poke----------------------------
			# learning stage 1 : learn to click the init port
			var = stage1.stage1(var.sessid,var,doo,myPoints,dbc,mouse) # if countdown timer reaches zero, the while loop in stage1.py will terminate
			var.points1,var.trials1 = fc.total_Points_trialCounter(var)
			fc.show_bigCoins_total((var.points0+var.points1),myPoints)
			fc.reset_Points_trialCounter(var)
			rewardG=var.rewardGot
			if var.timer.getTime() < 0:
				fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)
				break

			#--------------------Stage 2: Fixation----------------------------
			# learning stage 2 : learn to fix in the init port
			var = stage2.stage2(var.sessid,var,doo,myPoints,dbc,mouse) # if countdown timer reaches zero, the while loop in stage2.py will terminate
			var.points2,var.trials2 = fc.total_Points_trialCounter(var)
			fc.show_bigCoins_total((var.points0+var.points1+var.points2),myPoints)
			fc.reset_Points_trialCounter(var)
			rewardG=rewardG+var.rewardGot
			if var.timer.getTime() < 0:
				fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)
				break

			#--------------------Stage 3: Sure Bet----------------------------
			# learning stage 3 : learn to click in blue circle to get surebet
			var = stage3.stage3(var.sessid,var,doo,myPoints,dbc,mouse) # if countdown timer reaches zero, the while loop in stage3.py will terminate
			var.points3,var.trials3 = fc.total_Points_trialCounter(var)
			fc.show_bigCoins_total((var.points0+var.points1+var.points2+var.points3),myPoints)
			fc.reset_Points_trialCounter(var)
			# If subject didn't have 4 rewards in a row at this stage and (s)he got rewards in less than half of total number of trials
			rewardG=rewardG+var.rewardGot # the number of trials on which subject gained a reward
			var.LearningFail = var.trials1/2+var.trials2/2+var.trials3/2 # half of the total amount of trials
			if rewardG<var.LearningFail and var.goodPokesInARoll<4:
				# update freeforced table
				var.stagestatus = "FAIL" # failed the learning stage
				print("Sorry, you did not pass learning")
				fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
				# update end_sessions table 
				LearningStageTotalPoints = var.points0+var.points1+var.points2+var.points3
				ttrials = var.trials0+var.trials1+var.trials2+var.trials3
				end_time = datetime.datetime.now() # record end time
				sql.w_after_learningFail(dbc,var,p_num, expDate, end_time, expName, host_ip, ttrials, LearningStageTotalPoints, setiddtb) # save data of this session in database
				# Close the experiment
				doo.instruction.text = 'Sorry, you did not pass learning'
				doo.instruction.draw()
				setup.mywin.flip()
				core.wait(2)
				core.quit()

			if var.timer.getTime() < 0:
				fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)
				break

			#--------------------Stage 45: Learn Risky Min Max Reward---------
			# learning stage 4-5 merged : learn to click in yellow circle to get reward with 50% probability
			var, passStage45 = stage45.stage45(var.sessid, var, doo, myPoints, dbc, mouse) # if countdown timer reaches zero, the while loop in stage45.py will terminate
			var.points45, var.trials45 = fc.total_Points_trialCounter(var) 
			fc.reset_Points_trialCounter(var)
			rewardG=rewardG+var.rewardGot
			if var.timer.getTime() < 0 and passStage45 == False: # the timer might cause an inconvenience if the participant just finishes stage45.py in time (only seconds left). So added passStage45, which is true is subject finished stage45. 
				fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)
				break

			#===================LEARNING STAGES END===================
			expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
			var.stagestatus = "PASS" # compelted succefully
			var.totalPoints = var.points0+var.points1+var.points2+var.points3+var.points45
			var.totalTrials = var.trials0+var.trials1+var.trials2+var.trials3+var.trials45
			fc.show_bigCoins_total(var.totalPoints,myPoints) # show the total profits to the subjects
			#--------------------writing to database-----------------------------
			fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
			end_time = datetime.datetime.now() # record end time
			#--------------------advance the subject-----------------------------
			var.advancement = 1 # advance the subject to the next stage
			var.stagestatus = "STARTING" # compelted succefully
			start_time = datetime.datetime.now() # get starttime of starting the new stage
			fc.write_task_data_away(dbc, var, expDate, p_num, start_time) # write away that the participant is starting this stage

		#===================FORCE-FORCE-FREE START===================
		elif var.advancement == 1:
			print("\nAdvancement 1")
			print("===============")
			expDate, start_time = fc.reset_variables(var)
			var.stg = 6
			while True: # Need a while loop here otherwise var.trialCounter would be set to 0 every new trial.
				print("firstOrderMistakes: " + str(var.firstOrderMistakes))
				sequenceList = [1, 1, 2, 0, 1, 2, 1, 1, 2, 1, 0, 2, 1, 1, 2, 1, 0, 2, 1, 1, 2, 0, 1, 2, 1, 0, 2, 1, 1, 2] # force force free
				#--------------------------Sequence reset --------------------------------
				if var.sequenceIndex == 29: # when sequenceIndex reaches 3, we reset the index back to 0, so the sequence force-force-free can continue restart.  
					var.sequenceIndex = 0
				#--------------------------Forced/free trials--------------------------------
				if sequenceList[var.sequenceIndex] == 1 and var.timer.getTime() > 0: # force trial
					fc.check_reset_shuffle(var, dbc, p_num)
					fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
				elif sequenceList[var.sequenceIndex] == 2 and var.timer.getTime() > 0: # free trial
					fc.check_reset_shuffle(var, dbc, p_num)
					fc.freeTrial(var, doo, dbc, mouse, myPoints) # this function also collects the choice of the subject
				elif var.timer.getTime() > 0:
					fc.check_reset_shuffle(var, dbc, p_num)
					fc.forcedTrial_blue(var, doo, dbc, mouse, myPoints)
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points6,var.trials6 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points6
					var.totalTrials = var.totalTrials + var.trials6
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

				if len(var.firstOrderMistakes) >= 10 and var.firstOrderMistakes.count("no") > var.firstOrderMistakes.count("yes") and var.firstOrderMistakes.count("yes") <= 2:
					"""
					Once a subject separates min and max lotteries (criteria on last 10 'free' trials sum(choice(max))>sum(choice(min)) and sum(choice(min)) <= 2) and if length of trials is at least 30, 
					then proceed to next phase. 
					"""
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "PASS" # compelted succefully
					var.points6,var.trials6 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points6
					var.totalTrials = var.totalTrials + var.trials6
					fc.show_bigCoins_total(var.totalPoints,myPoints)
					var.sequenceIndex = 0 # reset
					var.firstOrderMistakes = [] # reset
					fc.write_task_data_away(dbc, var, expDate, p_num, start_time) # write away the that the participant passed this stage
					var.advancement = 2 # advance the subject to the next stage
					var.stagestatus = "STARTING" # compelted succefully
					start_time = datetime.datetime.now()
					fc.write_task_data_away(dbc, var, expDate, p_num, start_time) # write away that the participant is starting the next stage
					break
				elif var.totalTrialCounter >= 120: # also counts mistakes: clicking outside of the circles as trials
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "FAIL" # completed succefully
					var.points6,var.trials6 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points6
					var.totalTrials = var.totalTrials + var.trials6
					print("Criteria are not met for stage 1, THE END! Total trials: " + str(var.totalTrialCounter))
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)
					break
		#===================FORCE-FORCE-FREE-FREE START===================
		elif var.advancement == 2:
			print("\nAdvancement 2")
			print("===============")
			np.random.shuffle(var.shuffleForcedRew)
			np.random.shuffle(var.shuffleForcedProbDraw)
			expDate, start_time = fc.reset_variables(var)
			sequenceList = [1, 1, 2, 2] # force-force-free-free
			var.stg = 7
			while True: 
				print("firstOrderMistakes = " + str(var.firstOrderMistakes))
				#--------------------------Sequence reset --------------------------------
				if var.sequenceIndex == 4: # when sequenceIndex reaches 4, we reset the index back to 0, so the sequence force-force-free-free can continue restart.  
					var.sequenceIndex = 0
				print("SequenceList = " + str(sequenceList[var.sequenceIndex]))
				#--------------------------Forced/free trials--------------------------------
				if sequenceList[var.sequenceIndex] == 1 and var.timer.getTime() > 0: # force trial
					fc.check_reset_shuffle(var, dbc, p_num)
					fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
				elif var.timer.getTime() > 0: # free trial
					fc.check_reset_shuffle(var, dbc, p_num)
					fc.freeTrial(var, doo, dbc, mouse, myPoints) # this function also collects the choice of the subject
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points7,var.trials7 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points7
					var.totalTrials = var.totalTrials + var.trials7
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

				if len(var.firstOrderMistakes) >= 15: # 15 free trials, sequence is force-force-free-free, so are 31 trials in total
					if var.firstOrderMistakes.count("no") > var.firstOrderMistakes.count("yes") and var.firstOrderMistakes.count("yes") <= 2:
						"""
						Once a subject separates min and max lotteries (criteria on last 15 'free' trials sum(choice(max))>sum(choice(min)) and sum(choice(min)) <= 2) and if length of trials is at least 30, 
						then proceed to next phase. 
						"""
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "PASS" # compelted succefully
						var.points7,var.trials7 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points7
						var.totalTrials = var.totalTrials + var.trials7
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						print("Criteria are met for stage 2! Total trials: " + str(var.totalTrialCounter))
						var.sequenceIndex = 0 # reset
						var.firstOrderMistakes = [] # reset
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 3 # advance the subject to the next stage
						var.stagestatus = "STARTING"
						start_time = datetime.datetime.now()
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time) 
						break
					elif var.totalTrialCounter >= 30: # 30 trials
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "FAIL" # completed succefully
						var.points7,var.trials7 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points7
						var.totalTrials = var.totalTrials + var.trials7
						print("totalPoints: " + str(var.totalPoints))
						print("Criteria are not met for stage 2! Total trials: " + str(var.totalTrialCounter))
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						fc.show_bigCoins_total(var.totalPoints,myPoints) # show the total profits to the subjects
						var.advancement = 1 # depromote the subject
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" 
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.sequenceIndex = 0 # reset
						var.firstOrderMistakes = [] # reset
						break

		#===================FORCE-FREE-FREE START===================
		elif var.advancement == 3:
			print("\nAdvancement 3")
			print("===============")
			np.random.shuffle(var.shuffleForcedRew)
			np.random.shuffle(var.shuffleForcedProbDraw)
			expDate, start_time = fc.reset_variables(var)
			sequenceList = [1, 2, 2] # force-free-free
			var.stg = 8
			while True:
				#--------------------------Sequence reset --------------------------------
				if var.sequenceIndex == 3: # when sequenceIndex reaches 3, we reset the index back to 0, so the sequence force-free-free can continue restart.  
					var.sequenceIndex = 0
				#--------------------------Forced/free trials--------------------------------
				if sequenceList[var.sequenceIndex] == 1 and var.timer.getTime() > 0: # force trial
					fc.check_reset_shuffle(var, dbc, p_num)
					print("\nforcedtrial")
					fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
				elif sequenceList[var.sequenceIndex] == 2 and var.timer.getTime() > 0: # free trial
					fc.check_reset_shuffle(var, dbc, p_num)
					print("\nfreetrial")
					fc.freeTrial(var, doo, dbc, mouse, myPoints) # this function also collects the choice of the subject
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points8,var.trials8 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points8
					var.totalTrials = var.totalTrials + var.trials8
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)
				# print("firstOrderMistakes: " + str(var.firstOrderMistakes))
				if len(var.firstOrderMistakes) >= 20:
					if var.firstOrderMistakes.count("yes") > 1:
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "FAIL" 
						var.points8,var.trials8 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points8
						var.totalTrials = var.totalTrials + var.trials8
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						var.sequenceIndex = 0 # reset
						var.firstOrderMistakes = [] # reset
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 2 #
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" 
						start_time = datetime.datetime.now()
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time) # write away that the participant is starting the next stage
						break
					else:
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "PASS"
						var.points8,var.trials8 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points8
						var.totalTrials = var.totalTrials + var.trials8
						print("var.points8: " + str(var.points8))
						print("totalPoints: " + str(var.totalPoints))
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 4 # depromote the subject
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" # completed succefully
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break


		#===================FREE START - ADVANCEMENT 4===================
		elif var.advancement == 4:
			print("\nAdvancement 4")
			print("===============")
			np.random.shuffle(var.shuffleForcedRew)
			np.random.shuffle(var.shuffleForcedProbDraw)
			expDate, start_time = fc.reset_variables(var)
			var.stg = 9
			while True:
				if var.timer.getTime() > 0:
					fc.check_reset_shuffle(var,dbc, p_num)
					fc.freeTrial(var, doo, dbc, mouse, myPoints)
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points9,var.trials9 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points9
					var.totalTrials = var.totalTrials + var.trials9
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

				if len(var.firstOrderMistakes) >= 30: 
					#-----------------CHECK FIRST ORDER MISTAKES---------------
					if var.firstOrderMistakes.count("yes") > 2: # first order violations, downgrade
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "FAIL"
						var.points9,var.trials9 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points9
						var.totalTrials = var.totalTrials + var.trials9
						print("var.points9: " + str(var.points9))
						print("totalPoints: " + str(var.totalPoints))
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 3
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" # completed succefully
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break # break the while loop, start advancement 3 again (forced-free-free)
					else:
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "PASS"
						print("var.points9: " + str(var.points9))
						print("totalPoints: " + str(var.totalPoints))
						var.points9,var.trials9 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points9
						var.totalTrials = var.totalTrials + var.trials9
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 5 # depromote the subject
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" # completed succefully
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break

		#===================FREE START - ADVANCEMENT 5====================		
		elif var.advancement == 5:
			print("\nAdvancement 5")
			print("===============")
			data = {'rewmag': [], 'choice': []}
			data = pd.DataFrame(data)
			expDate, start_time = fc.reset_variables(var)
			var.stg = 10
			var.shuffleFreeRew, var.shuffleFreeProbDraw, var.shuffleProb, var = fc.setshuffleListFreeTrials(var,dbc,var.stg, p_num)
			print(var.shuffleFreeRew)
			print(var.shuffleFreeProbDraw)
			print("new sound is " + str(var.new_sound))
			sequenceList = [1, 2, 2]
			var.schedule = "new_sound"
			var.rewForcedIndex = 0
			var.rewFreeIndex = 0
			var.firstOrderMistakes = []
			var.dataIndex = 0
			print("Start Learning of new sound (forced-free-free x 2)")
			for i in range(2):
				for sequence in sequenceList:
					print("Trial: " + str(var.trialCounter))
					if sequence == 1:
						fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
					else:
						fc.freeTrial(var, doo, dbc, mouse, myPoints)
			print("End Learning of new sound")
			var.schedule = ""
			var.rewForcedIndex = 0
			var.rewFreeIndex = 0
			var.firstOrderMistakes = []
			while True:
				if var.timer.getTime() > 0:
					fc.check_reset_shuffle(var,dbc, p_num)
					fc.freeTrial(var, doo, dbc, mouse, myPoints)
					data.loc[var.dataIndex] = (var.yrewmag ,var.ychoice)
					if len(data) > 30:
						drop = var.dataIndex - 30
						print("dataIndex: " + str(var.dataIndex))
						print("dropping index: " + str(drop))
						data = data.drop(drop)
					var.dataIndex += 1
					print(data)
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points10,var.trials10 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points10
					var.totalTrials = var.totalTrials + var.trials10
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

				if len(var.firstOrderMistakes) >= 30: # 30
					#print("Probability of chosing 18: " + str(sql.r_freetrialrew(dbc,var,var.stg,18, p_num)))
					#print("Probability of chosing 2: " + str(sql.r_freetrialrew(dbc,var,var.stg,2, p_num)))
					#-----------------CHECK FIRST ORDER MISTAKES---------------
					if var.firstOrderMistakes.count("yes") > 2: # first order violations, downgrade
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "FAIL"
						var.points10,var.trials10 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points10
						var.totalTrials = var.totalTrials + var.trials10
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 4
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" # completed succefully
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.shuffleFreeRew = [2,18,18,2,18,18,2,18,2,18,2,18,2,18,18,2,18,2,18,2,2,18,18,2,2,18,2,18,2,2,18,18,2,2,2,18,2,18,2,18]
						var.shuffleForcedRew = [18,18,18,2,2,18,2,18,18,2,2,2,2,2,2,18,2,2,18,18,2,2,2,18,2,18,18,2,2,18,18,2,18,2,2,2,18,2,2,18,18,2,18,18,2,18,2,2,18,18,18,18,2,2,2,18,18,18,18,18,18,2,18,2,2,18,18,18,2,2,2,2,2,18,18,2,18,18,2,18]
						var.shuffleFreeProbDraw = [0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,0,1,1,0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,1]
						var.shuffleForcedProbDraw = [0,1,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1,1,1,0,0,0,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,1,1,1,1,0,1,1,0,1,1,0,1,0,0,1,0,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,1,0,1,1,0]
						break
					print("% Risky Option")
					print("Rewmag 2: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']) ))
					print("Rewmag " + str(var.new_sound) + ": " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == var.new_sound, 'choice'])))
					print("Rewmag 18: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice'])) )
					if np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice'])  >= np.mean(data.loc[data.loc[:, 'rewmag'] == var.new_sound, 'choice'])  >= np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']) : # completion criteria  
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "PASS"
						var.points10,var.trials10 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points10
						var.totalTrials = var.totalTrials + var.trials10
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 6
						var.stagestatus = "STARTING"
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break

		#===================FREE START - ADVANCEMENT 6====================	
		elif var.advancement == 6:
			print("\nAdvancement 6")
			print("===============")
			data = {'rewmag': [], 'choice': []}
			data = pd.DataFrame(data)
			expDate, start_time = fc.reset_variables(var)
			var.stg = 11
			var.shuffleFreeRew, var.shuffleFreeProbDraw, var.shuffleProb, var = fc.setshuffleListFreeTrials(var,dbc,var.stg, p_num)
			sequenceList = [1, 2, 2]
			var.schedule = "new_sound"
			var.rewForcedIndex = 0
			var.rewFreeIndex = 0
			var.dataIndex = 0
			var.firstOrderMistakes = []
			print("Start Learning of new sound (forced-free-free x 2)")
			for i in range(2):
				for sequence in sequenceList:
					print("Trial: " + str(var.trialCounter))
					if sequence == 1:
						fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
					else:
						fc.freeTrial(var, doo, dbc, mouse, myPoints)
			print("End Learning of new sound")
			var.schedule = ""
			var.rewForcedIndex = 0
			var.rewFreeIndex = 0
			var.firstOrderMistakes = []
			while True:
				if var.timer.getTime() > 0:
					fc.check_reset_shuffle(var,dbc, p_num)
					fc.freeTrial(var, doo, dbc, mouse, myPoints)
					data.loc[var.dataIndex] = (var.yrewmag ,var.ychoice)
					if len(data) > 30:
						drop = var.dataIndex - 30
						print("dataIndex: " + str(var.dataIndex))
						print("dropping index: " + str(drop))
						data = data.drop(drop)
					var.dataIndex += 1
					print(data)
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points11,var.trials11 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points11
					var.totalTrials = var.totalTrials + var.trials11
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

				if len(var.firstOrderMistakes) >= 30: # 30
					
					#-----------------CHECK FIRST ORDER MISTAKES---------------
					if var.firstOrderMistakes.count("yes") > 2: # first order violations, downgrade
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "FAIL"
						var.points11,var.trials11 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points11
						var.totalTrials = var.totalTrials + var.trials11
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 5 # depromote the subject
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" # completed succefully
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break
					print("% Risky Option")
					print("Rewmag 2: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']) ))
					print("Rewmag 8: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 8, 'choice']) ))
					print("Rewmag 12: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 12, 'choice']) ))
					print("Rewmag 18: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice'])) )
					if np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 12, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 8, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']): # completion criteria  
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "PASS"
						var.points11,var.trials11 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points11
						var.totalTrials = var.totalTrials + var.trials11
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 7
						var.stagestatus = "STARTING"
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break

		#===================FREE START - ADVANCEMENT 7====================	
		elif var.advancement == 7:
			print("\nAdvancement 7")
			print("===============")
			data = {'rewmag': [], 'choice': []}
			data = pd.DataFrame(data)
			expDate, start_time = fc.reset_variables(var)
			var.stg = 12
			var.shuffleFreeRew, var.shuffleFreeProbDraw, var.shuffleProb, var = fc.setshuffleListFreeTrials(var,dbc,var.stg, p_num)
			sequenceList = [1, 2, 2]
			var.schedule = "new_sound"
			var.rewForcedIndex = 0
			var.rewFreeIndex = 0
			var.dataIndex = 0
			var.firstOrderMistakes = []
			print("Start Learning of new sound (forced-free-free x 2)")
			for i in range(2):
				for sequence in sequenceList:
					print("Trial: " + str(var.trialCounter))
					if sequence == 1:
						fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
					else:
						fc.freeTrial(var, doo, dbc, mouse, myPoints)
			print("End Learning of new sound")
			var.schedule = ""
			var.rewForcedIndex = 0
			var.rewFreeIndex = 0
			var.firstOrderMistakes = []
			while True:
				if var.timer.getTime() > 0:
					fc.check_reset_shuffle(var,dbc, p_num)
					fc.freeTrial(var, doo, dbc, mouse, myPoints)
					data.loc[var.dataIndex] = (var.yrewmag ,var.ychoice)
					if len(data) > 30:
						drop = var.dataIndex - 30
						print("dataIndex: " + str(var.dataIndex))
						print("dropping index: " + str(drop))
						data = data.drop(drop)
					var.dataIndex += 1
					print(data)
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points12,var.trials12 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points12
					var.totalTrials = var.totalTrials + var.trials12
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

				if len(var.firstOrderMistakes) >= 30: #30
					#-----------------CHECK FIRST ORDER MISTAKES---------------
					if var.firstOrderMistakes.count("yes") > 2: # first order violations, downgrade
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "FAIL"
						var.points12,var.trials12 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points12
						var.totalTrials = var.totalTrials + var.trials12
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 6
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" # completed succefully
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break 
					if var.new_sound == 15:
						print("% Risky Option")
						print("Rewmag 2: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']) ))
						print("Rewmag 8: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 8, 'choice']) ))
						print("Rewmag12: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 12, 'choice']) ))
						print("Rewmag 15: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 15, 'choice']) ))
						print("Rewmag 18: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice']) ))
						if np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 15, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 12, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 8, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']): # completion criteria  
							expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
							var.stagestatus = "PASS"
							var.points12,var.trials12 = fc.total_Points_trialCounter(var)
							var.totalPoints = var.totalPoints + var.points12
							var.totalTrials = var.totalTrials + var.trials12
							fc.show_bigCoins_total(var.totalPoints,myPoints)
							fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
							var.advancement = 8 # depromote the subject
							start_time = datetime.datetime.now()
							var.stagestatus = "STARTING" # completed succefully
							fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
							break
					if var.new_sound == 5:
						print("% Risky Option")
						print("Rewmag 2: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']) ))
						print("Rewmag 5: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 5, 'choice']) ))
						print("Rewmag 8: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 8, 'choice']) ))
						print("Rewmag 12: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 12, 'choice']) ))
						print("Rewmag 18: " + str(np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice']) ))
						if np.mean(data.loc[data.loc[:, 'rewmag'] == 18, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 12, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 8, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 5, 'choice']) >= np.mean(data.loc[data.loc[:, 'rewmag'] == 2, 'choice']): # completion criteria  
							expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
							var.stagestatus = "PASS"
							var.points12,var.trials12 = fc.total_Points_trialCounter(var)
							var.totalPoints = var.totalPoints + var.points12
							var.totalTrials = var.totalTrials + var.trials12
							fc.show_bigCoins_total(var.totalPoints,myPoints)
							fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
							var.advancement = 8
							var.stagestatus = "STARTING"
							fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
							break

		#===================FREE START - ADVANCEMENT 8====================
		# Check if subject is in 4th session
		# Check if subject had 200 trials in 8th advancement
		# check across all 200 or more trials the reward probabilities criteria. 
		elif var.advancement == 8:
			print("\nAdvancement 8")
			print("===============")
			data = {'rewmag': [], 'choice': []}
			data = pd.DataFrame(data)
			old_data = {'rewmag': [], 'choice': []}
			old_data = pd.DataFrame(data)
			expDate, start_time = fc.reset_variables(var)
			var.stg = 13
			var.shuffleFreeRew, var.shuffleFreeProbDraw, var.shuffleProb, var = fc.setshuffleListFreeTrials(var,dbc,var.stg, p_num)

			#--------------INDIVIDUAL TWEAKING: SESSION CHECK--------------
			n_sessions = sql.r_distinct_sessions(dbc, p_num)
			if  n_sessions >= 3: # check if participant did 3 sessions or more
				trials = sql.r_advancement8_trials(dbc, p_num) # collect all the advancement 8 trials
				trials = pd.DataFrame(list(trials), columns=['rewmag', 'choice'])
				old_data = data.append(trials, ignore_index = True)
				print("dataframe: " + str(old_data))
				if len(old_data) >= 200 and (np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 18, 'choice']) >= \
				np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 15, 'choice']) >= np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 12, 'choice']) >= \
				np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 8, 'choice']) >= np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 5, 'choice']) >= \
				np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 2, 'choice'])):
					print("# of trials: " + str(len(old_data)))
					print("% Risky Option")
					print("Rewmag 2: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 2, 'choice']) ))
					print("Rewmag 5: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 5, 'choice']) ))
					print("Rewmag 8: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 8, 'choice']) ))
					print("Rewmag 12: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 12, 'choice']) ))
					print("Rewmag 15: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 15, 'choice']) ))
					print("Rewmag 18: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 18, 'choice']) ))
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "PASS"
					fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
					var.advancement = 9 # depromote the subject
					start_time = datetime.datetime.now()
					var.stagestatus = "STARTING" # completed succefully
					fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
			#--------------LEARNING NEW SOUND --------------
			if var.advancement == 8:
				sequenceList = [1, 2, 2]
				var.schedule = "new_sound"
				var.rewForcedIndex = 0
				var.rewFreeIndex = 0
				var.dataIndex = 0
				var.firstOrderMistakes = []
				print("Start Learning of new sound (forced-free-free x 2)")
				for i in range(2):
					for sequence in sequenceList:
						print("Trial: " + str(var.trialCounter))
						if sequence == 1:
							fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
						else:
							fc.freeTrial(var, doo, dbc, mouse, myPoints)
				print("End Learning of new sound")
				var.schedule = ""
			#--------------START FREE TRIALS--------------
				var.rewForcedIndex = 0
				var.rewFreeIndex = 0
				var.firstOrderMistakes = []
				while True:
					if var.timer.getTime() > 0:
						fc.check_reset_shuffle(var,dbc, p_num)
						fc.freeTrial(var, doo, dbc, mouse, myPoints)
						data.loc[var.dataIndex] = (var.yrewmag ,var.ychoice)
						old_data.loc[len(old_data + 1)] = (var.yrewmag ,var.ychoice)
						if len(data) > 30:
							drop = var.dataIndex - 30
							print("dropping index: " + str(drop))
							data = data.drop(drop)
						var.dataIndex += 1
						print(old_data)
					else:
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "INPROGRESS"
						var.points13,var.trials13 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points13
						var.totalTrials = var.totalTrials + var.trials13
						fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

					if var.timer.getTime() > 0 and n_sessions >= 3 and len(old_data) >= 200 and (np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 18, 'choice']) >= \
					np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 15, 'choice']) >= np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 12, 'choice']) >= \
					np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 8, 'choice']) >= np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 5, 'choice']) >= \
					np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 2, 'choice'])):
						print("# of trials: " + str(len(old_data)))
						print("% Risky Option")
						print("Rewmag 2: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 2, 'choice']) ))
						print("Rewmag 5: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 5, 'choice']) ))
						print("Rewmag 8: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 8, 'choice']) ))
						print("Rewmag 12: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 12, 'choice']) ))
						print("Rewmag 15: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 15, 'choice']) ))
						print("Rewmag 18: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 18, 'choice']) ))
						expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
						var.stagestatus = "PASS"
						var.points13,var.trials13 = fc.total_Points_trialCounter(var)
						var.totalPoints = var.totalPoints + var.points13
						var.totalTrials = var.totalTrials + var.trials13
						fc.show_bigCoins_total(var.totalPoints,myPoints)
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						var.advancement = 9 
						start_time = datetime.datetime.now()
						var.stagestatus = "STARTING" 
						fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
						break
					else:
						print("# of trials: " + str(len(old_data)))
						print("% Risky Option")
						print("Rewmag 2: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 2, 'choice']) ))
						print("Rewmag 5: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 5, 'choice']) ))
						print("Rewmag 8: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 8, 'choice']) ))
						print("Rewmag 12: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 12, 'choice']) ))
						print("Rewmag 15: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 15, 'choice']) ))
						print("Rewmag 18: " + str(np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 18, 'choice']) ))

					if len(var.firstOrderMistakes) >= 30:
						#-----------------CHECK FIRST ORDER MISTAKES---------------
						if var.firstOrderMistakes.count("yes") >= 2: # first order violations, downgrade
							expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
							var.stagestatus = "FAIL"
							var.adv8check = False
							var.probIndex = 1
							var.points13,var.trials13 = fc.total_Points_trialCounter(var)
							var.totalPoints = var.totalPoints + var.points13
							var.totalTrials = var.totalTrials + var.trials13
							fc.show_bigCoins_total(var.totalPoints,myPoints)
							fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
							var.advancement = 7 # depromote the subject
							start_time = datetime.datetime.now()
							var.stagestatus = "STARTING" 
							fc.write_task_data_away(dbc, var, expDate, p_num, start_time)
							break


		#===================FREE START - ADVANCEMENT 9====================
		elif var.advancement == 9:
			print("\nAdvancement 9")
			print("===============")
			data = {'rewmag': [], 'choice': []}
			data = pd.DataFrame(data)
			var.adv8check = True
			sequenceList = [1, 1, 2]
			var.stg = 14
			expDate, start_time = fc.reset_variables(var)

			#--------------INDIVIDUAL TWEAKING: CHECK RISKY BEHAVIOR--------------
			print("risky behavior prob: " + str((np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 18, 'choice']) + \
			np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 15, 'choice']) + np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 12, 'choice']) + \
			np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 8, 'choice']) + np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 5, 'choice'])) / 5 ))

			if (np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 18, 'choice']) + np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 15, 'choice']) + \
			np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 12, 'choice']) + np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 8, 'choice']) + \
			np.mean(old_data.loc[old_data.loc[:, 'rewmag'] == 5, 'choice'])) / 5 >= 0.5:
				print("add 0.25")
				var.probIndex = 0 # 0.25 prob
			else:
				print("add 0.75")
				var.probIndex = 2 # 0.75 prob
				
			for i in range(10): # 30 trials to learn the new probability
				for sequence in sequenceList:
					if sequence == 1:
						fc.forcedTrial_yellow(var, doo, dbc, mouse, myPoints)
					else:
						fc.freeTrial(var, doo, dbc, mouse, myPoints)
			var.shuffle = True
			var.shuffleFreeRew, var.shuffleFreeProbDraw, var.shuffleProb, var = fc.setshuffleListFreeTrials(var,dbc,var.stg, p_num)
			print("Probability Learning Ended, Probability shuffling starting: " + str(var.shuffleProb))
			var.rewForcedIndex = 0
			var.rewFreeIndex = 0
			var.firstOrderMistakes = []
			while True:
				if var.timer.getTime() > 0:
					fc.check_reset_shuffle(var,dbc, p_num)
					fc.freeTrial(var, doo, dbc, mouse, myPoints)
					data.loc[var.dataIndex] = (var.yrewmag ,var.ychoice)
					if len(data) > 30:
						drop = var.dataIndex - 30
						print("dropping index: " + str(drop))
						data = data.drop(drop)
					var.dataIndex += 1
					print(data)
				else:
					expDate = datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
					var.stagestatus = "INPROGRESS"
					var.points14,var.trials14 = fc.total_Points_trialCounter(var)
					var.totalPoints = var.totalPoints + var.points14
					var.totalTrials = var.totalTrials + var.trials14
					fc.close_session(var, doo, dbc, mouse, myPoints, start_time, expName, expDate, p_num, setiddtb, host_ip)

	#===================SESSION END===================
	return p_net

if __name__ == "__main__":
	risk_nv_freeforced(var, doo, myPoints, dbc, mouse)