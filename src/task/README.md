[email *evgeniya.lukinova@nottingham.ac.uk* for further explanations]
## Necessary setups before risk experiment (offline study)

**Computer setup:**

    1. Python 2.7 needs to be installed in your computer
    2. Download and install PsychoPy 1.83.04
    3. Download and install any MySQL user interface
    4. Check with evgeniya.lukinova@nottingham.ac.uk on 'helpers' custom module needed to access dtb
    5. Setup working path
        - In repos/code/functions.py, find setpath() function
        - sys.path.append('directory where you git cloned repos folder')
        - sys.path.append('directory where your /Python/2.7/site-packages is')
    6. Setup MySQL database
        6.1. Setup all tables(and column names) needed in our code
            -sessions
            -sessions_end
            -settings
            -subjinfo
            -trials
        6.2. Set database user name
            - In repos/code/functions, find dbconnect() function
            - Input your database user name in sql.select_user(dbc,'your user name')
        6.3. Setup a subjects pool in your database
            - In 'subjinfo' table, input information of all subjects
            - There needs to be an ID(netid) for each subject to input at the beginning of each program that will lead a unique subjid saved in the 'subjinfo' table
        6.4. Create two necessary settings
            - You can input whatever fits your need in the n/a's 
            - In 'settings' table, create rows of necessary settings for the experiment, e.g.:
| settingsid | expgroupid | data                                                                                                                             | description |
|-----------:|------------|----------------------------------------------------------------------------------------------------------------------------------|-------------|
| n/a        | n/a        | {"probability": [ 0.25, 0.5, 0.75], "rewmag": [ 2, 4, 6, 6, 6, 12, 12, 12, 18, 18, 18, 50], "surebet": 4, "refresherNum": 10, "blockTrial": 2, "passThreshold": 2} | risk   |          

**Auxiliary files catalog**
    
    1. functions.py: file which contains all functions needed for other scripts
    2. SQL_call.py: all database related commands(read and write) needed for other scripts
    3. doodle.py: defines class Doodle which creates circle/text/sound objects and modifies their properties (important file that decreases memory use)
    4. newPoints.py: defines class NewPoins which creates coin objects and modifies their properties (imported by all files that need to draw coins)
    5. setup.py: defines the window that displays stimuli and other setups (imported by all files for experiments)
    6. variables.py: defines class Variables which defines all the variables needed (imported by all files for experiments)
    7. coin_echo5.wav: the sound stimuli when getting coins
    
