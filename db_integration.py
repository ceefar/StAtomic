# ---- IMPORTS ---- 
# for db
import pymysql
import os
from dotenv import load_dotenv


# ---- DATABASE INIT ----

# load environment variables from .env file
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
                            isTimeSensitive BOOL, dueDate TIMESTAMP, dueDateTime TIMESTAMP, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
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


def create_todo_tags_relational_db(username:str = "default"):
    """ relational table links tags to todo tasks, assumption here is that one db for one user (is just testing ffs chill is fine) so is fine to have as one overarching table, obvs instead could have 1 long table and id for each todoList which would be like each table but is fine for now """
    create_table_query = f"CREATE TABLE IF NOT EXISTS {username}_todotags (todotagid INT AUTO_INCREMENT, todolist VARCHAR(255), todoid INT NOT NULL, tagid INT, PRIMARY KEY(todotagid), FOREIGN KEY (todoid) REFERENCES {username}_todo(taskid), FOREIGN KEY (tagid) REFERENCES {username}_tags(tagid))" 
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


def get_main_tasks_for_todo_list_by_id(username, task_id):
    """ currently not bringing taskID but leaving code here incase need shortly in future (if so parameter refactor), but rn only using taskTitle """
    # get_main_tasks_query = f"SELECT taskid, taskTitle FROM {username}_todo WHERE todoListID = {listID} AND taskType = 'main_task'"
    get_main_tasks_query = f"SELECT taskTitle FROM {username}_todo WHERE todoListID = {task_id} AND taskType = 'main_task'"
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
    if taskDetail == "":
        if taskParentID == "":
            add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskType, taskStatus) VALUES ({todoListID}, '{taskTitle}', 1, 1)"
        else:
            add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskType, taskParentID, taskStatus) VALUES ({todoListID}, '{taskTitle}', 2, {taskParentID}, 1)"
    else:
        if taskParentID == "":
            add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskDetail, taskType, taskStatus) VALUES ({todoListID}, '{taskTitle}', '{taskDetail}', 1, 1)"
        else:
            add_table_query = f"INSERT INTO {username}_todo (todoListID, taskTitle, taskDetail, taskType, taskParentID, taskStatus) VALUES ({todoListID}, '{taskTitle}', '{taskDetail}', 2, {taskParentID}, 1)"

    add_to_db(add_table_query)

    get_last_id_query = "SELECT LAST_INSERT_ID()"
    get_last_id = get_from_db(get_last_id_query)
    print(f"{get_last_id = }")


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