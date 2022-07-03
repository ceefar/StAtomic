# ---- IMPORTS ---- 
# for db
import pymysql
import os
from dotenv import load_dotenv
# for datetime
import datetime
# testing sumnt
import streamlit as st


# ---- DATABASE INIT ----

# load environment variables from .env file
# singleton doesnt rerun, unlike st.cache decorator -> theres not return value so does this even matter?
@st.experimental_singleton
def load_env():
    load_dotenv()

load_dotenv()
    
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

# establishes the database connection from .env file
connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    database = database
)

def add_to_db(command):
    """ adds values to the db with no return value, based on the given command (query) """
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    connection.commit()
    cursor.close()

def get_from_db(command):
    """ gets a result from the db, based on the given command (query) """
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    myresult = cursor.fetchall()
    connection.commit()
    cursor.close()
    return(myresult)

def close_connection():
    connection.close()

# ---- END DATABASE INIT ----


# ---- CORE DB INTERACTIONS ----


def create_all_tasks_v0_db():
    pass


def create_habits_v0_db():
    """ stores habits only, unsure if using one or both (i.e. habits and all or just all), starting with just this for now """
    create_table_query = "CREATE TABLE IF NOT EXISTS habits_v0 (habitid INT AUTO_INCREMENT, user_habit TEXT, habit_alignment ENUM('positive', 'neutral', 'negative'), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (habitid))"                             


def create_habit_tags_v0_db():
    """ relational table links tags to habits """
    create_table_query = "CREATE TABLE IF NOT EXISTS habittags_v0 (habittagid INT AUTO_INCREMENT, habitid INT NOT NULL, tagid INT, PRIMARY KEY(habittagid), FOREIGN KEY (habitid) REFERENCES habits_v0(habitid), FOREIGN KEY (tagid) REFERENCES tags_v0(tagid))" 


# N0TE PROBABLY ALSO NEED TAG TYPE TABLE - IF DO NEED IT EITHER WAY TBF CAN DO WITHOUT FOR NOW
def create_tags_list_v0_db():
    """ stores user created tags, not 100% sure as to where fk should have gone, possibly here, also unsure on constaint since now what you can't delete a habit? or tag? or wut?! - need to test """
    create_table_query = "CREATE TABLE IF NOT EXISTS tags_v0 (tagid INT AUTO_INCREMENT, tag VARCHAR(255), tagtype VARCHAR(255), PRIMARY KEY(tagid))"


def get_base_habit_data_v0():
    """ grabs just the data from the habits_v0 table """
    #get_habit_data_query = "SELECT * FROM habits_v0 LIMIT 1"
    get_habit_data_query = "SELECT * FROM habits_v0"
    habit_data = get_from_db(get_habit_data_query)
    #print(f"{habit_data = }")
    return(habit_data)


def add_habit_to_db_v0():
    pass


# ---- T0DO LIST ----
# each named list is a todo that can have tasks added to it

# IMPORTANT! -> NEED A LIST OF ACTUAL T0DO LISTS AS A TABLE, SO CAN ADD TAGS N I GUESS LIKE STATS N SHIT

# main task and subtask heirarchical, toggle task is one that *has* to be done repeatedly - has a deadline and a reset which will turn it back on. (sumnt like that anyway, also considered like a floating task but couldnt really solidify the concept)
# critical, urgent/high, moderate, low/meh, none (toggle? toggle default anyway?)
# either due date or due date time not both (due date could still theoretically have the time and just end at 11:59:59 but whatever can figure out later)
# actually just going slightly excess on things to add that may be temp or atleast optional but is easier to judge if they exist first
# this includes impact/benefits (what will you get out of this task)
# NOT INCLUDED BUT REALLY COULD -> timeframe (is like due date but instead of a date its like a range right maybe test actually quantifiable - few days, 1 week, fortnight, etc, vs more abstract like rapid term, short term, medium term, long term...
# note certain things may be more relavent for toggle tasks or even habits but thats why we do lots of experimenting at this stage
# difficulty could be named better, would prefer to be more about how far its pushing you outside your existing comfort zone but can have that as the descript for now anyways
# consider that some things are more valid for certain types of task or like habits almost right like alignment for example or again timeframe
# todolistid is the name of the todo list (storing all in one now) to do list id is that todolist (make a table for this! as need to link them)
def create_new_todo_list_db(username:str = "default"):
    """ main list, stores todo items and subtasks, for now anyway """
    final_table_name = convert_todo_list_name_to_table_name(username) # note -> just added todoListID & taskTitle not null, if it breaks shit then just remove for now
    create_table_query = (f"CREATE TABLE IF NOT EXISTS {username}_todo (taskid INT AUTO_INCREMENT, todoListID INT NOT NULL, taskTitle VARCHAR(255) NOT NULL, taskDetail TEXT,\
                            taskType ENUM('main_task', 'sub_task', 'toggle_task'), taskParentID INT, \
                            taskStatus ENUM('in_progress', 'completed', 'paused'),\
                            taskUrgency ENUM('critical', 'urgent', 'moderate', 'low', 'none'),\
                            taskImpact ENUM('massive', 'significant', 'limited', 'minor'),\
                            taskDifficulty ENUM('complicated','complex','average','simple'),\
                            isTimeSensitive BOOL, dueDate DATE, dueDateTime DATETIME, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                            updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (taskid), FOREIGN KEY (todoListID) REFERENCES {username}_todo_id_name(todoListID))")        
    add_to_db(create_table_query)                      


def create_todo_id_name_relational_db(username):
    """ links todoListID (_todo) with todoListName (here) """
    create_table_query = f"CREATE TABLE IF NOT EXISTS {username}_todo_id_name (todoListID INT AUTO_INCREMENT, todoListName VARCHAR(255), PRIMARY KEY(todoListID))"
    add_to_db(create_table_query)  


# so for this now ig tag type will be stuff like UI or the page name in question or like the debug/fixme, etc
def create_tags_list_db(username:str = "default"):
    """ creates default table that stores default tags for tasks (not overarching todo lists) """
    create_table_query = f"CREATE TABLE IF NOT EXISTS {username}_tags (tagid INT AUTO_INCREMENT, tag VARCHAR(255), tagtype VARCHAR(255), PRIMARY KEY(tagid))"
    add_to_db(create_table_query) 


# note should all be not null but leaving for now
def create_todo_tags_relational_db(username:str = "default"):
    """ relational table links tags to todo tasks, assumption here is that one db for one user (is just testing ffs chill is fine) so is fine to have as one overarching table, obvs instead could have 1 long table and id for each todoList which would be like each table but is fine for now """
    create_table_query = f"CREATE TABLE IF NOT EXISTS {username}_todotags (todoTagID INT AUTO_INCREMENT, todoListID VARCHAR(255),\
                        todoTaskID INT NOT NULL, tagID INT, PRIMARY KEY(todotagid),\
                        FOREIGN KEY (todoTaskID) REFERENCES {username}_todo(taskid) ON DELETE CASCADE ON UPDATE CASCADE,\
                        FOREIGN KEY (todoListID) REFERENCES {username}_todo_id_name(todoListID) ON DELETE CASCADE ON UPDATE CASCADE,\
                        FOREIGN KEY (todoTagID) REFERENCES {username}_tags(tagid) ON DELETE CASCADE ON UPDATE CASCADE)" 
    add_to_db(create_table_query)                        


def get_base_todo_data():
    """ grabs just the data from the habits_v0 table """
    #get_habit_data_query = "SELECT * FROM habits_v0 LIMIT 1"
    get_habit_data_query = "SELECT * FROM habits_v0"
    habit_data = get_from_db(get_habit_data_query)
    #print(f"{habit_data = }")
    return(habit_data)


# ---- string manipulation ----

def convert_todo_list_name_to_table_name(todo_title:str):
    """ just converts spaces to underlines, for sure will be edge cases, using split will be better but is fine for now """
    split_title = todo_title.replace(" ","_")
    return(split_title)


# ---- crud main todo lists ----

# for create (multi-use tbf, recategorise once have more functionality)

def get_all_todo_list_names_and_ids(username:str) -> tuple:
    """ write me pls """
    get_todo_lists_query = f"SELECT * FROM {username}_todo_id_name"
    get_todo_lists = get_from_db(get_todo_lists_query)
    # print(f"{get_todo_lists = }")
    return(get_todo_lists)


def get_main_tasks_for_todo_list_by_id(username, list_id):
    """ currently not bringing taskID but leaving code here incase need shortly in future (if so parameter refactor), but rn only using taskTitle """
    # get_main_tasks_query = f"SELECT taskid, taskTitle FROM {username}_todo WHERE todoListID = {listID} AND taskType = 'main_task'"
    get_main_tasks_query = f"SELECT taskTitle FROM {username}_todo WHERE todoListID = {list_id} AND taskType = 'main_task'"
    main_tasks = get_from_db(get_main_tasks_query)
    main_tasks_listed = []
    [main_tasks_listed.append(task[0]) for task in main_tasks]
    # print(f"{main_tasks_listed = }")
    return(main_tasks_listed)


def get_count_of_subtasks_for_parent(username, task_title):
    """ simple count of each main tasks sub tasks """
    get_task_id_query = f"SELECT taskid FROM {username}_todo WHERE taskTitle = '{task_title}'"
    task_id = get_from_db(get_task_id_query)
    listID = task_id[0][0]
    get_count_of_sub_tasks_query = f"SELECT COUNT(taskParentID) FROM {username}_todo WHERE taskParentID = {listID} AND taskType = 'sub_task'"
    get_subtask_count = get_from_db(get_count_of_sub_tasks_query)
    #print(f"{get_subtask_count = }")
    return(get_subtask_count[0][0])


def get_parent_id_from_title(username:str, taskParentTitle:str, listID:int) -> int:
    """ write me plis """
    get_parent_id_query = f"SELECT taskid FROM {username}_todo WHERE taskTitle = '{taskParentTitle}' AND todoListID = {listID} AND taskType = 'main_task'"
    parent_id = get_from_db(get_parent_id_query)
    #print(f"{parent_id = }")
    parentID = parent_id[0][0]
    return(parentID)


def get_subtasks_for_parent_from_id(username:str, parentID:str, listID:int):
    """ write me plis """
    get_subtasks_for_parent_query = f"SELECT taskTitle FROM {username}_todo WHERE taskParentID = {parentID} AND todoListID = {listID} AND taskType = 'sub_task'"
    parent_subtasks = get_from_db(get_subtasks_for_parent_query)
    subtasks_listed = []
    [subtasks_listed.append(task[0]) for task in parent_subtasks]
    #print(f"{subtasks_listed = }")
    return(subtasks_listed)


def add_todo_task_to_db_basic(username:str, todoListID, taskTitle, taskDetail="", taskParentID="", taskUrgency="", taskImpact="", taskDiff="", isTimeSensitive="", dueDate="", dueDateTime=""):
    """ add task super basic first version... """
    # can do very easy if blank stuff, but just starting with parent id stuff for now
    
    if dueDate:
        isTimeSensitive = True

    if taskDetail == "":
        if taskParentID == "":
            if isTimeSensitive:
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskType, taskStatus, isTimeSensitive, dueDate) VALUES ({todoListID}, '{taskTitle}', 1, 1, 1, '{dueDate}')"
            else:
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskType, taskStatus, isTimeSensitive) VALUES ({todoListID}, '{taskTitle}', 1, 1, 0)"
        else:
            # else has parent 
            if isTimeSensitive:
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskType, taskParentID, taskStatus, isTimeSensitive, dueDate) VALUES ({todoListID}, '{taskTitle}', 2, {taskParentID}, 1, 1, '{dueDate}')"
            else:
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskType, taskParentID, taskStatus, isTimeSensitive) VALUES ({todoListID}, '{taskTitle}', 2, {taskParentID}, 1, 0)"
    else:
        # if has task detail
        if taskParentID == "":
            if isTimeSensitive:
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskDetail, taskType, taskStatus, isTimeSensitive, dueDate) VALUES ({todoListID}, '{taskTitle}', '{taskDetail}', 1, 1, 1, '{dueDate}')"
            else:
                # not time sensitive
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskDetail, taskType, taskStatus, isTimeSensitive) VALUES ({todoListID}, '{taskTitle}', '{taskDetail}', 1, 1, 0)"
        else:
            # else has parent 
            if isTimeSensitive:
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskDetail, taskType, taskParentID, taskStatus, isTimeSensitive, dueDate) VALUES ({todoListID}, '{taskTitle}', '{taskDetail}', 2, {taskParentID}, 1, 1, '{dueDate}')"
            else:
                add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskDetail, taskType, taskParentID, taskStatus, isTimeSensitive) VALUES ({todoListID}, '{taskTitle}', '{taskDetail}', 2, {taskParentID}, 1, 0)"

    add_to_db(add_table_query)

    get_last_id_query = "SELECT LAST_INSERT_ID()"
    get_last_id = get_from_db(get_last_id_query)
    #print(f"{get_last_id = }")
    return(get_last_id)


def get_tags_from_db(username):
    """ write me """
    get_tags_query = f"SELECT tag, tagtype FROM {username}_tags"
    get_tags = get_from_db(get_tags_query)
    tags_list = []
    for tags in get_tags:
        tagstr = f"{tags[0]} [{tags[1]}]"
        #tagstr = f"{tags[0]} - {tags[1]}"
        tags_list.append(tagstr)
    #print(f"{tags_list = }")
    return(tags_list)


def get_todolistid_from_taskid(username, taskid):
    """ write me """
    get_todlistid_query = f"SELECT todoListID from {username}_todo WHERE taskid = {taskid}"
    get_todolistid = get_from_db(get_todlistid_query)
    #print(f"{get_todolistid[0][0] = }")
    return(get_todolistid[0][0])


def get_todolistname_from_its_id(username, todolistid):
    """ write me """
    get_todolistname_query = f"SELECT todoListName from {username}_todo_id_name WHERE todoListID = {todolistid}"
    get_todolistname = get_from_db(get_todolistname_query)
    #print(f"{get_todolistname[0][0] = }")
    return(get_todolistname[0][0])


def get_tagid_from_tag_plus_group(username, tagname, taggroup):
    """ write me """
    get_tagid_query = f"SELECT tagid from {username}_tags WHERE tag = '{tagname}' AND tagtype = '{taggroup}'"
    get_tagid = get_from_db(get_tagid_query)
    #print(f"{get_tagid[0][0] = }")
    return(get_tagid[0][0])


def add_todotags_for_new_task(username, listid, lasttaskid, tagid):
    """ write me """
    add_todotags_query = f"INSERT INTO {username}_todotags (todoListID, todoTaskID, tagID) VALUES ({listid}, {lasttaskid}, {tagid})"
    add_to_db(add_todotags_query)


# ---- v0.31 subtask view page ----

def view_tasks_basic(username:str, anID:int, parent_child_or_all:str = "parent"):
    """ write me plis """
    if parent_child_or_all == "parent":
        task_type = "main_task"
        get_tasks_basic_af_query = f"SELECT taskTitle, taskDetail, taskType, taskParentID, taskStatus, dueDate, DATE(created), DATE(updated), taskid, DATEDIFF(DATE(updated), DATE(created)) FROM {username}_todo WHERE todoListID = {anID} AND taskType = '{task_type}'"
    elif parent_child_or_all == "child":
        task_type = "sub_task"
        get_tasks_basic_af_query = f"SELECT taskTitle, taskDetail, taskType, taskParentID, taskStatus, dueDate, DATE(created), DATE(updated), taskid, DATEDIFF(DATE(updated), DATE(created)) FROM {username}_todo WHERE taskParentID = {anID} AND taskType = '{task_type}'"
    else:
        get_tasks_basic_af_query = f"SELECT taskTitle, taskDetail, taskType, taskParentID, taskStatus, dueDate, DATE(created), DATE(updated), taskid, DATEDIFF(DATE(updated), DATE(created)) FROM {username}_todo WHERE todoListID = {anID}"
    
    tasks_basic_af = get_from_db(get_tasks_basic_af_query)
    subtasks_listed = []
    for task in tasks_basic_af:
        task_dict = {}
        task_dict["title"] = task[0]
        if task[1]:
            task_dict["detail"] = task[1]
        else:
            task_dict["detail"] = " "
        task_dict["taskType"] = task[2]
        task_dict["taskParent"] = task[3]
        task_dict["taskStatus"] = task[4]
        task_dict["dueDate"] = task[5]
        task_dict["createdDate"] = task[6]
        task_dict["updatedDate"] = task[7]
        task_dict["taskID"] = task[8]  
        task_dict["dateDiff"] = task[9]
        subtasks_listed.append(task_dict)      

    #[subtasks_listed.append(task) for task in tasks_basic_af]
    #print(f"{subtasks_listed} = ")
    return(subtasks_listed)


def get_id_for_parent(username, task_title):
    """ legit would be an easy refactor of the count sub tasks function for this but since doing refactor shortly anyway is pointless """
    get_task_id_query = f"SELECT taskid FROM {username}_todo WHERE taskTitle = '{task_title}'"
    task_id = get_from_db(get_task_id_query)
    listID = task_id[0][0]
    return(listID)
 

def update_task_status(username:str, taskid, currentStatus:bool):
    """ current mostly for testing """
    # could literally just query to check it and then would be 100% sure but just do like this for now for rapid testing
    get_current_status_query = f"SELECT taskStatus FROM {username}_todo WHERE taskid = {taskid}"
    get_current_status = get_from_db(get_current_status_query)
    current_status = get_current_status[0][0]
    print(f"{taskid} : {current_status = }")

    if currentStatus == "in_progress":     
        update_task_query = f"UPDATE {username}_todo SET taskStatus = 'completed' WHERE taskid = {taskid}" # 1
    elif currentStatus == "completed":
        update_task_query = f"UPDATE {username}_todo SET taskStatus = 'in_progress' WHERE taskid = {taskid}" # 0 
    add_to_db(update_task_query)


def get_current_status(username:str, taskid):
    """ used to accurately preset toggle value """
    get_current_status_query = f"SELECT taskStatus FROM {username}_todo WHERE taskid = {taskid}"
    get_current_status = get_from_db(get_current_status_query)
    current_status = get_current_status[0][0]
    #print(f"CURRENT STATUS : {current_status = }")
    return(current_status)



# ---- v0.32 [NEW] view page ----


def view_tasks_toggle(username:str, listID:int, parent_child_or_all:str, specificTaskIDTitle:int = "", handyfilter:str = "", taskstatusfilter:str = "", filter_tags_list:list = [""]): # mutable default! -> change this once is final (so isn't default? even possible tho?)
    """ first attempt at dynamically creating the query (as opposed to a big ass switch case), sure requires if statements here but isn't *only* if statements """
    # note handy filter can be turned off so *needs* the default value

    # doesn't change in any cases, and if ever wanna add stuff is easy af, do all future queries like this yanno
    prefix_part = "SELECT t1.taskTitle, t1.taskDetail, t1.taskType, t1.taskParentID, t1.taskStatus, t1.dueDate, DATE(t1.created), DATE(t1.updated), t1.taskid, DATEDIFF(DATE(t1.updated), DATE(t1.created)), t2.todoTaskID, t2.tagID, t3.tagid, t3.tag, t3.tagtype"
    prefix_part_no_tags = "SELECT t1.taskTitle, t1.taskDetail, t1.taskType, t1.taskParentID, t1.taskStatus, t1.dueDate, DATE(t1.created), DATE(t1.updated), t1.taskid, DATEDIFF(DATE(t1.updated), DATE(t1.created))"

    # think only this part should have the actual WHERE tho, as it will for sure be in every single query
    from_part = f"FROM {username}_todo t1"
    where_todo_id_part = f"WHERE t1.todoListID = {listID}"


    # VIEW TYPE TOGGLE
    if parent_child_or_all == "Main Tasks Only":
        where_task_type_part = f"AND t1.taskType = 'main_task'"
    elif parent_child_or_all == "Subtasks Only":
        where_task_type_part = f"AND t1.taskType = 'sub_task'"
    elif parent_child_or_all == "Main Task + Subtasks":
        where_task_type_part = ""


    # ALL TASKS OR SPECIFIC TASK DROPDOWN
    if specificTaskIDTitle == "All Tasks":
        where_parentid_part = ""
    elif specificTaskIDTitle != "":
        parentID = get_from_db(f"SELECT taskid FROM {username}_todo WHERE taskTitle = '{specificTaskIDTitle}'")
        print(f"{parentID[0][0] = }")
        if parent_child_or_all == "Subtasks Only":
            where_parentid_part = f"AND t1.taskParentID = {parentID[0][0]}"
        else:
            where_parentid_part = f"AND t1.taskParentID = {parentID[0][0]} OR t1.taskid = {parentID[0][0]}"
    else:
        where_parentid_part = ""


    # HANDY FILTER - note could pass limit amount as parameter in future and let the user set it but is fine as is for now
    limit_amount = 5
    if handyfilter != "": # swear if handyfilter: would have been fine you mong
        if handyfilter == "Recent Tasks":
            order_by_part = "ORDER BY t1.created DESC"
            limit_part = f"LIMIT {limit_amount}"
        elif handyfilter == "Oldest Tasks":
            order_by_part = "ORDER BY t1.created ASC"
            limit_part = f"LIMIT {limit_amount}"
        elif handyfilter == "Stalled Tasks":
            order_by_part = "AND t1.updated IS NOT NULL ORDER BY DATEDIFF(DATE(t1.updated), DATE(t1.created)) DESC"
            limit_part = f"LIMIT {limit_amount}"
        else:
            order_by_part = ""
            limit_part = ""
    else:
        order_by_part = "" 
        limit_part = ""

    # note for stalled, puts null at the bottom which i dont want so removing null for now as **TEMPORARY** fix
    # COULD BE A FIX TO SET UPDATED OF NULL FIELDS TO THEIR CREATE DATE BUT IDK IF THATS POSSIBLE

    # couldnt really decide on what to do for stalled, heres some queries that got left out incase you wanna change it
    # AND updated IS NOT NULL ORDER BY DATEDIFF(DATE(updated), CURDATE()) ASC


    # STATUS FILTER
    if taskstatusfilter != "":
        if taskstatusfilter == "In Progress Tasks":
            where_status_part = "AND t1.taskStatus = 1"
        elif taskstatusfilter == "Completed Tasks":
            where_status_part = "AND t1.taskStatus = 2"
        else:
            where_status_part = ""
    else:
        where_status_part = ""    


    # TAGS FILTER
    # for reference, the below queries both do the same thing, one with join, one without
    # SELECT t1.taskTitle, t1.taskDetail, t1.taskType, t1.taskParentID, t1.taskStatus, t1.dueDate, DATE(t1.created), DATE(t1.updated), t1.taskid, t2.todoTaskID, t2.tagID FROM ceefar_todo t1 INNER JOIN ceefar_todotags t2 ON t2.todoTaskID = t1.taskid
    # SELECT t1.taskTitle, t1.taskDetail, t1.taskType, t1.taskParentID, t1.taskStatus, t1.dueDate, DATE(t1.created), DATE(t1.updated), t1.taskid, t2.todoTaskID, t2.tagID FROM ceefar_todo t1, ceefar_todotags t2 WHERE todoTaskID = taskid

    # some kinda for loop here but just doing simple real quick to test
    try:
        if filter_tags_list[0] != "":
            inner_join_part = f"INNER JOIN {username}_todotags t2 ON t2.todoTaskID = t1.taskid"
            second_inner_join_part = f"INNER JOIN {username}_tags t3 ON t3.tagid = t2.tagID"
            where_inner_join_part = f"AND t2.tagID = {filter_tags_list[0]}"
            # pops of the query we've already added in "where_inner_join_part"
            has_tags = True
            filter_tags_list.pop(0) 
        else:
            #inner_join_part = f", {username}_todotags t2"
            #second_inner_join_part = f", {username}_tags t3"
            inner_join_part = ""
            second_inner_join_part = ""
            where_inner_join_part = ""
            has_tags = False
    except IndexError:
        #inner_join_part = f", {username}_todotags t2"
        #second_inner_join_part = f", {username}_tags t3"
        inner_join_part = ""
        second_inner_join_part = ""
        where_inner_join_part = ""    
        has_tags = False


    final_tagid_string = ""
    
    for tagid in filter_tags_list:
        final_tagid_string += (f"OR t2.tagID = {tagid} ")

    #print(f"{final_tagid_string = }")

    if has_tags:
        final_query = prefix_part + " " + from_part + " " + inner_join_part + " " + second_inner_join_part + " " + where_todo_id_part + " " + where_inner_join_part + " " + final_tagid_string + " " + where_task_type_part + " " + where_parentid_part + " " + where_status_part + " " + order_by_part + " " + limit_part
    else:
        final_query = prefix_part_no_tags + " " + from_part + " " + inner_join_part + " " + second_inner_join_part + " " + where_todo_id_part + " " + where_inner_join_part + " " + final_tagid_string + " " + where_task_type_part + " " + where_parentid_part + " " + where_status_part + " " + order_by_part + " " + limit_part

    print(f"\n{final_query = }")

    tasks_basic_af = get_from_db(final_query)
    subtasks_listed = []
    for task in tasks_basic_af:
        task_dict = {}
        task_dict["title"] = task[0]
        if task[1]:
            task_dict["detail"] = task[1]
        else:
            task_dict["detail"] = " "
        task_dict["taskType"] = task[2]
        task_dict["taskParent"] = task[3]
        task_dict["taskStatus"] = task[4]
        task_dict["dueDate"] = task[5]
        task_dict["createdDate"] = task[6]
        task_dict["updatedDate"] = task[7]
        task_dict["taskID"] = task[8]  
        task_dict["dateDiff"] = task[9]
        if has_tags:
            task_dict["todoTaskID"] = task[10]
            task_dict["tagID"] = task[11]
            task_dict["tagid"] = task[12]
            task_dict["tag"] = task[13]
            task_dict["tagtype"] = task[14]
        subtasks_listed.append(task_dict)     

        # SOME WAY TO MERGE IN CASE OF THE SAME TODOTASKID - wont be that hard since we have that var tbf! (just adding shit on to the dict, appending to task[13] & task[14]) 

    #print(f"{subtasks_listed} = ")
    return(subtasks_listed)


def get_days_between_a_days_and_today(a_day):
    """ get days between any date and today using mysql """
    days_between = get_from_db(f"SELECT DATEDIFF(CURDATE(), '{str(a_day)}')")
    return(days_between[0][0])


def get_task_status_from_task_title(username:str , task_title:str) -> str:
    """ self referencing af - used as part of img creation, should properly plan for this stuff in refactor (is a lot to do just one person tho but meh) """
    # wouldnt be surprised if have this already yanno
    # try except (index error?)
    task_status = get_from_db(f"SELECT taskStatus FROM {username}_todo WHERE taskTitle = '{task_title}'")
    task_status = task_status[0][0]
    if task_status:
        #print(f"{task_status = }")
        return(task_status)


# use task id to get tag id 
# then use tag id to get tagsnames 
def get_tagnames_from_taskid(username, taskid) -> list|tuple|None:
    """ write me """
    try:
        get_tagid = get_from_db(f"SELECT tagID FROM {username}_todotags WHERE todoTaskID = {taskid}")

        # print(f"{get_tagid = }")
        
        tagid_list = []
        if len(get_tagid) > 1:
            for tagsid in get_tagid:
                tagid_list.append(tagsid[0]) 
        else:
            # is just 1
            tagid = get_tagid[0][0]
            get_tagnames = get_from_db(f"SELECT tag, tagtype FROM {username}_tags WHERE tagid = {tagid}")
            tag_names = get_tagnames[0] # WANT AS TUPLE BTW SO NEED TO SORT THIS HERE!
            return(tag_names)
    
    except IndexError:
        # print("No Tag")
        return(None)

    # print(f"{tagid_list = }")

    tags_name_list = []
    if tagid_list:
        for tagid in tagid_list:
            get_tagnames = get_from_db(f"SELECT tag, tagtype FROM {username}_tags WHERE tagid = {tagid}")
            tag_names = get_tagnames[0]
            tags_name_list.append(tag_names)

    # print(f"{tags_name_list = }")
    return(tags_name_list)



# LOL THIS ISNT WHAT I WANTED BUT JUST LEAVING AS PROBABLY WILL USE EVENTUALLY
def get_tagid_from_formatted_tag(username, formatted_tag:str):
    """ write me """
    tagndx = formatted_tag.rfind("[")
    tag_name = formatted_tag[:tagndx-1].strip()
    tag_group = formatted_tag[tagndx+1:-1]
    get_tagid_query = f"SELECT tagid from {username}_tags WHERE tag = '{tag_name}' AND tagtype = '{tag_group}'"
    get_tagid = get_from_db(get_tagid_query)
    user_tagid = get_tagid[0][0]
    return(user_tagid[0][0])


# ---- stats / insights ----

def get_count_all_tasks(username) -> int:
    """ write me pls """
    main_task_count = get_from_db(f"SELECT COUNT(taskType) FROM {username}_todo WHERE taskType = 'main_task'")
    main_task_count = int(main_task_count[0][0])
    # print(f"{main_task_count = }")
    return(main_task_count)


# ---- mood tracker ----

def create_mood_table():
    """ from manual sql query """
    create_mood_table_query = "CREATE TABLE IF NOT EXISTS mood_monitor (mood_indx INT AUTO_INCREMENT NOT NULL PRIMARY KEY, user_id INT NOT NULL, mood_entry ENUM('worst','awful','bad','below average','average','above average','good','great','amazing') NOT NULL, mood_notes VARCHAR(1000), day_number INT DEFAULT (WEEKDAY(CURDATE())), week_number INT DEFAULT (WEEK(CURDATE())), entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)"
    add_to_db(create_mood_table_query)


# could be one function and parameters, but better -> make it a class! oooo
def get_current_date():
    """ self referencing """
    current_date = get_from_db("SELECT CURDATE()")
    current_date = str(current_date[0][0])
    return(current_date)


def get_current_dayname():
    """ self referencing """
    current_dayname = get_from_db(f"SELECT DAYNAME(CURDATE())")
    current_dayname = str(current_dayname[0][0])
    return(current_dayname)


def get_current_week_number():
    """ self referencing """
    current_weeknumb = get_from_db(f"SELECT WEEK(CURDATE())")
    current_weeknumb = current_weeknumb[0][0]
    return(current_weeknumb)


def get_this_weeks_logged_mood_basics(username:str):
    """ write me pls """
    # obvs need to do username number shit but just forcing for now
    if username == "ceefar":
        user_id = 3
    current_weeknumb = get_current_week_number()
    get_weeks_mood_basics_query = f"SELECT day_number, mood_entry+0 FROM mood_monitor WHERE user_id = {user_id} AND week_number = {current_weeknumb}"
    weeks_mood_basics = get_from_db(get_weeks_mood_basics_query)
    # print(weeks_mood_basics)
    return(weeks_mood_basics)


def get_previous_sunday_mood_int(username:str) -> int:
    """ used for ... """
    # BIG TO N0TE - MONDAY IS 0, DOES THAT FUCK UP ANYTHING?
    # obvs need this function to get username to id from user_info table 
    if username == "ceefar":
        user_id = 3
    previous_week_numb = (get_current_week_number() - 1)
    #print(f"{get_current_week_number() = }")
    #print(f"{previous_week_numb = }")
    get_previous_sunday_mood = get_from_db(f"SELECT mood_entry+0 FROM mood_monitor WHERE user_id = {user_id} AND week_number = {previous_week_numb} AND day_number = 6")
    try:
        get_previous_sunday_mood = int(get_previous_sunday_mood[0][0])
        # return if not empty clause pls
        return(get_previous_sunday_mood)
    except IndexError:
        return(None)


def log_user_mood_for_day(username:str, mood_entry, mood_notes:str = None):
    """ write me """
    if username == "ceefar":
        user_id = 3
    if mood_notes:    
        # truncate the notes if too long (unless can force that in the text entry)
        add_to_db(f"INSERT INTO mood_monitor (user_id, mood_entry, mood_notes) VALUES ({user_id}, '{mood_entry}', '{mood_notes}')")
    else:
        add_to_db(f"INSERT INTO mood_monitor (user_id, mood_entry) VALUES ({user_id}, '{mood_entry}')")
    

def get_all_week_numbs_for_user(username:str):
    """ constraining to this year only btw """
    if username == "ceefar":
        user_id = 3
    get_week_numbs = get_from_db(f"SELECT DISTINCT week_number FROM mood_monitor WHERE user_id = {user_id} AND YEAR(entry_date) = 2022 ORDER BY week_number") 
    week_numb_list = []
    [week_numb_list.append(week_numb[0]) for week_numb in get_week_numbs] 
    return(week_numb_list)


def get_mood_data_for_given_week_numb(username:str, givenweek:int) -> tuple:
    """ write me """
    if username == "ceefar":
        user_id = 3
    get_week_mood_data = f"SELECT day_number, mood_entry+0 FROM mood_monitor WHERE user_id = {user_id} AND week_number = {givenweek} ORDER BY day_number"
    weeks_mood_data = get_from_db(get_week_mood_data)
    #print(f"{weeks_mood_data = }") 
    final_week_list = []

    def add_day(j):
        """ if you find the day numb in the given week data tuple then add its mood int else add none, pls note bool here is critical """
        daydone = False
        for week in weeks_mood_data:
            if week[0] == j:
                final_week_list.append(int(week[1]))
                daydone = True
        if daydone == False:
            final_week_list.append(None)
    
    for i in range(7):
        add_day(i)

    #print(f"{final_week_list = }") 
    final_week_tuple = tuple(final_week_list)
    #print(f"{final_week_tuple = }") 
    return(final_week_tuple)


# ---- main ----

def main():
    username = "ceefar"
    create_todo_id_name_relational_db(username)
    create_new_todo_list_db(username)
    create_tags_list_db(username)
    create_todo_tags_relational_db(username)
    


# ---- driver ----

if __name__ == "__main__":
    main()



"""
    for i in range(7):
        if i == 0:
            mondone = False
            for week in weeks_mood_data:           
                if week[0] == 0:
                    final_week_list.append(week[1])
                    mondone = True
            if mondone == False:
                final_week_list.append(None)
        if i == 1:
            tuedone = False
            for week in weeks_mood_data:           
                if week[0] == 1:
                    final_week_list.append(week[1])
                    tuedone = True
            if tuedone == False:
                final_week_list.append(None)
        if i == 2:
            weddone = False
            for week in weeks_mood_data:           
                if week[0] == 2:
                    final_week_list.append(week[1])
                    weddone = True
            if weddone == False:
                final_week_list.append(None)
        if i == 3:
            thudone = False
            for week in weeks_mood_data:           
                if week[0] == 3:
                    final_week_list.append(week[1])
                    thudone = True
            if thudone == False:
                final_week_list.append(None)                
        if i == 4:
            fridone = False
            for week in weeks_mood_data:           
                if week[0] == 4:
                    final_week_list.append(week[1])
                    fridone = True
            if fridone == False:
                final_week_list.append(None)     
        if i == 5:
            satdone = False
            for week in weeks_mood_data:           
                if week[0] == 5:
                    final_week_list.append(week[1])
                    satdone = True
            if satdone == False:
                final_week_list.append(None)
        if i == 6:
            sundone = False
            for week in weeks_mood_data:           
                if week[0] == 6:
                    final_week_list.append(week[1])
                    sundone = True
            if sundone == False:
                final_week_list.append(None)      
"""