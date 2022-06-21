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


def create_tags_list_v0_db():
    """ stores user created tags, not 100% sure as to where fk should have gone, possibly here, also unsure on constaint since now what you can't delete a habit? or tag? or wut?! - need to test """
    create_table_query = "CREATE TABLE IF NOT EXISTS tags_v0 (tagid INT AUTO_INCREMENT, tag VARCHAR(255), tagtype VARCHAR(255), PRIMARY KEY(tagid))"

# PROBABLY ALSO NEED TAG TYPE TABLE - IF DO NEED IT EITEHRWAY TBF CAN DO WITHOUT FOR NOW


def add_habit_to_db_v0():
    pass




# ---- T0DO LIST ----
 
def create_todo_v0_db():
    """ stores todo only, for now anyway, focusing this first since its waaaay easier """
    create_table_query = "CREATE TABLE IF NOT EXISTS todo_v0 (todoid INT AUTO_INCREMENT, user_title VARCHAR(255), user_todo TEXT, todo_status ENUM('in_progress', 'completed', 'paused'), created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (todoid))"                             


def add_todo_v0_db(todo_title, todo_entry):
    """ add todo v0, simple af but just starting simple af duh """
    add_table_query = f"INSERT INTO todo_v0 (user_title, user_todo, todo_status) VALUES ('{todo_title}', '{todo_entry}', 1)"
    add_to_db(add_table_query)                             

# OBVS TAGS AND SHIT BUT JUST START SIMPLE DUHHHH!



def get_base_habit_data_v0():
    """ grabs just the data from the habits_v0 table """
    #get_habit_data_query = "SELECT * FROM habits_v0 LIMIT 1"
    get_habit_data_query = "SELECT * FROM habits_v0"
    habit_data = get_from_db(get_habit_data_query)
    #print(f"{habit_data = }")
    return(habit_data)
