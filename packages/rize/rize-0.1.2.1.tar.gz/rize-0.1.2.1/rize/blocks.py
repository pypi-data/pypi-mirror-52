import os
import rize 
import sys
import nep
import time
import kapuccino
if sys.version_info[0] == 3:
    import _thread as thread
else:
    import thread



class block_program():
        def __init__(self):

            self.blackboard_model = {
                "touch":
                {
                    "left_hand": {"value":1, "time":0}, 
                    "right_hand": {"value":1, "time":0}, 
                    "head": {"value":1, "time":0}
                },
                "word":
                {
                    "value": {"value":0, "time":0}
                }
            }

            self.block_cognition = kapuccino.fsm_bt(self.blackboard_model, "ZMQ")
            thread.start_new_thread( self.block_cognition.managment)
            thread.start_new_thread( self.execution)
       

        
        def execution(self):
            node = nep.node("blackboard")             # Create a new node
            conf = node.broker("many2one")
            sub = node.new_sub("/block_program","json",conf)        # Set the topic and the config
            path = ""

            if os.environ.get('OS','') == 'Windows_NT':
                path = "C:/RIZE"
            else:
                path = rize.getRIZEpath()

            while True:
                s, msg = sub.listen()
                if s:
                    if msg["action"] == "action":
                        print (" ---- NEW ACTION ----")
                        self.block_cognition.runAction(msg["input"])
                        time.sleep(.5)
                    elif msg["action"] == "start":
                        print (" ---- NEW PROGRAM ----")
                        self.block_cognition.loadProgram(path +  "/projects/" +  str(msg["input"]))
                        time.sleep(.5)
                        self.block_cognition.stop = False
                    elif msg["action"] == "stop":
                        print (" ---- STOP PROGRAM ---- ")
                        self.block_cognition.stop = True
                    elif msg["action"] == "close":
                        self.block_cognition.stop = True
                        self.block_cognition.on = False
                        print (" ---- CLOSING... ---- ")
                        time.sleep(1)
                        break
                time.sleep(1)




class block_execution():
        def __init__(self):
                # Pub BT block program
                nep_node = nep.node("rize_block","ZMQ",False)
                conf = nep_node.broker("many2one") 
                # Block program control
                self.pub_block  = nep_node.new_pub("/block_program", "json",conf)
        
        def onStopBlockProgram(self, input_ = "", options_= ""):
                print ("STOP BLOCK PROGRAM")
                # Send specification to block program
                self.pub_block.publish({"action":"stop"}) 

        def onRunAction(self, input_="", options_=""):
                print ("DO ACTION")
                # Send specification to block program
                print (input_)
                self.pub_block.publish({"action":"action", "input":input_})

        def onBuildBlockProgram(self,input_="", options_=""):
        
                # ----- Save program -----

                project_name = input_

                if os.environ.get('OS','') == 'Windows_NT':
                    path = "C:/RIZE"
                else:
                    path = rize.getRIZEpath()

                
                path_projects = path + "/" + "projects"
                path_project = path_projects +"/" + project_name
                
                # Create folders if not created
                rize.onCreateFolder(path_project, "goal/json")
                rize.onCreateFolder(path_project, "reaction/json")
                
                l_goals = options_['name_goals']
                code_goals = options_['goals']

                l_reactions = options_['name_reactions']
                code_reactions = options_['reactions']
                
                # Save reactions and goals

                i = 0
                path = path_projects + "/" + project_name +  "/goal/json"
                for f in l_goals:
                        rize.onSaveJSON(path, f, code_goals[i])
                        i = i + 1

                i = 0
                path = path_projects + "/" + project_name +  "/reaction/json"
                for f in l_reactions:
                        rize.onSaveJSON(path, f, code_reactions[i])
                        i = i + 1

                time.sleep(.5)

                # ----- Run program -----

                print ("START BLOCK PROGRAM")
                # Send specification to block program
                # Imput is the program to run
                self.pub_block.publish({"action":"start", "input":project_name})

                return {"node":"success"}


        def onRunBlockProgram(self,input_="", options_=""):
        
                time.sleep(.5)

                # ----- Run program -----

                print ("START BLOCK PROGRAM")
                # Send specification to block program
                # Imput is the program to run
                self.pub_block.publish({"action":"start", "input":input_})

                return {"node":"success"}

        def onRunBlockModule(self,input_="", options_=""):
        
                time.sleep(.5)

                # ----- Run program -----

                print ("START BLOCK PROGRAM")
                # Send specification to block program
                # Imput is the program to run
                self.pub_block.publish({"action":"module", "input":input_, "options":options_})

                return {"node":"success"}

# --------------------------- onLaunchRobots -----------------------------
# Description:  Launch robots
def onLaunchRobots(input_, options_):
    print ("Robot launch action ... ")
    if type(input_) is str:
        robot = input_
        s, options = rize.getRobotConfiguration(robot)

        if s:
                if sys.version_info[0] == 3: # Python 3
                    middleware = options['middleware']
                    ip = options['ip']
                    name = options['name']
                    port = options['port']
                    type_ = options['type']
                    python_version = options['python']

                else: # Python 2
                    middleware = options['middleware'].encode("UTF-8")
                    ip = options['ip'].encode("UTF-8")
                    name = options['name'].encode("UTF-8")
                    port = str(options['port']).encode("UTF-8")
                    type_ = options['type'].encode("UTF-8")
                    python_version = options['python'].encode("UTF-8")

                parameters = " " + str(name) + " " + str(ip) +  " " + str(port) + " " + str(middleware)
                nep.neprun(type_,type_, parameters, python_version)

        else:
                print ("Robot configuration for *** " + robot + " *** not found")
                return {'state': "failure"}

# --------------------- onLoadProgramConfigurations -------------------------
# Description:  Load program configurations
def onLoadProgramConfigurations(input_, options_):
    project_name = input_
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = rize.getRIZEpath()
    path_projects = path + "/" + "projects"
    json_value = rize.read_json(path_projects + "/" + project_name + "/config.json")
    dict_value = rize.json2dict(json_value)
    return dict_value

# ------------------------------------ onSaveBlock -------------------------
# Description:  Save XML and JS files
def onSaveBlock(input_, options_):
    project_name = input_
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = rize.getRIZEpath()
    path_projects = path + "/" + "projects"
    path_project = path_projects + "/" + project_name
    name_block = options_["name"]
    type_ = options_["type"]

    # Save block js
    rize.onSaveFile(path_project + "/" + type_ + "/js/", name_block + ".js",  options_['code'])
    # Save block html
    rize.onSaveFile(path_project + "/" + type_ + "/xml/" , name_block + ".xml",  options_['xml'])

    return {'state': "success"}

# ------------------------------------ onBuildBlockCodeJS -----------------
# Description:  Create code.js file
def onBuildBlockCodeJS(input_):
    path = os.getcwd()
    project_name = input_
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = rize.getRIZEpath()
    path_projects = path + "/" + "projects"
    path_project = path_projects + "/" + project_name

    try:
        reaction_files = rize.getFiles(path_project + "/reaction/js")
    except:
        print ("Non reactions")
    try:
        goals_files = rize.getFiles(path_project + "/goal/js")
    except:
        print ("Non goals")
    try:
        behaviors_files = rize.getFiles(path_project + "/behavior/js")
    except:
        print ("Non behaviors")
    try:
        modules_files = rize.getFiles(path_project + "/module/js")
    except:
        print ("Non modules")

    initial = "var " + project_name + "= { \n"
    final = "\n }"

    file_w = open( path_project  + "/code.js","w") 
    file_w.write(initial) 

    all_files = [[reaction_files, "/reaction/js" ], [goals_files,"/goal/js"], [behaviors_files,"/behavior/js" ], [modules_files, "/module/js"]]

    # Write functions
    for sfiles in all_files:
        for f in sfiles[0]:
            file = open(path_project + sfiles[1]  + "/" + f, "r") 
            text = file.read() 
            file_w.write(text) 

    print ("code.js saved")
    file_w.write(final) 
    file_w.close() 
    os.chdir(path)

# ------------------------------------ onSaveBlockProgram -----------------
# Description: Save json files of a block program
def onSaveBlockProgram(input_, options_):
    
    path = os.getcwd()
    project_name = input_
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = rize.getRIZEpath()
    path_projects = path + "/" + "projects"
    path_project = path_projects +"/" + project_name
    new = options_["new"]

    # Create the projects folder if was delated
    if not os.path.exists(path_project):
        os.makedirs(path_project)

    # Save only if have a name
    if not project_name == "":

        # Save project configuration
        rize.onSaveJSON(path_project, "config" , options_["config"])

        if new: # Is a new project ?
            try:
                print ("Create folders")
                rize.onCreateFolder(path_project,"goal")
                rize.onCreateFolder(path_project,"goal/js")
                rize.onCreateFolder(path_project,"goal/json")
                rize.onCreateFolder(path_project,"goal/xml")
                rize.onCreateFolder(path_project,"reaction")
                rize.onCreateFolder(path_project,"reaction/js")
                rize.onCreateFolder(path_project,"reaction/json")
                rize.onCreateFolder(path_project,"reaction/xml")
                rize.onCreateFolder(path_project,"module")
                rize.onCreateFolder(path_project,"module/js")
                rize.onCreateFolder(path_project,"module/json")
                rize.onCreateFolder(path_project,"module/xml")
                rize.onCreateFolder(path_project,"behavior")
                rize.onCreateFolder(path_project,"behavior/js")
                rize.onCreateFolder(path_project,"behavior/json")
                rize.onCreateFolder(path_project,"behavior/xml")
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                os.chdir(path)
                return {'state': "failure"}

    print ("Building program")
    onBuildBlockCodeJS(input_)
    os.chdir(path)
    return {'state': "success"}


# ------------------------------------ onLoadBlocksPrograms -------------------------
# Description: Get list of Block projects
def onLoadBlocksPrograms(input_ = "", options_ = ""):
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = rize.getRIZEpath()

    list_projects = os.listdir(path + "/projects")
    print ("Projects")
    print (list_projects)
    result = {'projects': list_projects}
    return result
