# ---- imports ---- 
# for web app and test components
from pymysql import OperationalError, ProgrammingError
import pymysql
import streamlit as st
import streamlit.components.v1 as stc # < unused at present
# for datetime object
import datetime
# for regular expressions
import re
# ---- my module imports ----
# for db access
import db_integration as db
# for creating images
import artist as arty


# ---- temp globals ----
# for testing/setup

user_name = "Ceefar"
db_username = user_name.lower()

# ---- layout ----
# either use more or remove pls, as barely using rn

topper = st.container()
form_intro = st.container()


# ---- page functions ----

@st.cache
def get_todo_lists_from_db(username:str) -> tuple:
    """ write me pls """
    # have done this the long way (passing both id and name as tuple) thinking could use the id and pass it back
    # that is unnecessarily long lmao, should just have passed the name and found the id on return but ah well
    # kinda semi made it work out by adding the id to the string in the create_todo_lists_list function
    # but obvs deleting a list will throw out the ids plus have to pick apart the string on return to get the id (which is fine tbf)
    username = username.lower()
    all_user_todo_list_tuples = db.get_all_todo_list_names_and_ids(username)
    return(all_user_todo_list_tuples)


# cache it?
def get_id_numb_from_formatted_list_name(formatted_list_name:str) -> int:
    """ from the currently selected list, find its id for db queries """
    # re.findall('\d+|$', assigned_todo_list)[0] # at somepoint find out wut da fuck is the difference?
    assigned_todo_id = int(re.search('\d+|$',formatted_list_name).group())
    return(assigned_todo_id)


# cache it?
def get_main_tasks_for_todo_list_from_db_with_subcount(username:str, formatted_list_name:str) -> tuple:
    """ write me """
    username = username.lower()
    listID = get_id_numb_from_formatted_list_name(formatted_list_name)
    main_tasks_for_todo_list = db.get_main_tasks_for_todo_list_by_id(username, listID)
    for i, main_task in enumerate(main_tasks_for_todo_list):
        subtaskcount = get_parent_subtask_count(username, main_task)
        main_task += (f" [{subtaskcount}]")
        main_tasks_for_todo_list[i] = main_task
    return(main_tasks_for_todo_list)


# cache it?
def get_main_tasks_for_todo_list_from_db(username:str, formatted_list_name:str) -> tuple:
    """ write me """
    username = username.lower()
    listID = get_id_numb_from_formatted_list_name(formatted_list_name)
    main_tasks_for_todo_list = db.get_main_tasks_for_todo_list_by_id(username, listID)
    return(main_tasks_for_todo_list)
        

def get_parent_subtask_count(username:str, task_title:str):
    username = username.lower()
    subtask_count = db.get_count_of_subtasks_for_parent(username, task_title)
    return(subtask_count)


def add_basic_task_to_db(username:str, todoListID:int, taskTitle:str, taskDetail:str = "", taskParentID:int = "", task_end_date:datetime = ""):
    """ write me pls """
    if task_end_date != "":
        istimesensitive = True
    placed_at_id = db.add_todo_task_to_db_basic(username, todoListID, taskTitle, taskDetail, taskParentID, dueDate=task_end_date)
    #db.add_todo_task_to_db_basic(username, todoListID, taskTitle, taskDetail, taskParentID, istimesensitive, task_end_date)
    #print(f"{placed_at_id[0][0] = }")
    return(placed_at_id[0][0])


# cache?
def create_todo_lists_list():
    """ write me pls """
    todo_lists = st.session_state["todo_lists"]
    todo_list_names = []
    for a_list in todo_lists.items():
        todo_list_names.append(f"{a_list[0]}. {a_list[1].replace('_',' ')}")
    # legit prints the list comprehension which is super annoying as its clean af
    # [todo_list_names.append(f"{a_list[0]}. {a_list[1].replace('_',' ')}") for a_list in todo_lists.items()] 
    return(todo_list_names)


# cache?
def get_subtasks_for_parent(username, taskparentName, todolistid):
    """ write me pls """
    parentID = db.get_parent_id_from_title(username, taskparentName, todolistid)
    parent_subtasks = db.get_subtasks_for_parent_from_id(username, parentID, todolistid)
    return(parent_subtasks)


#@st.cache
def create_task_subtask_img_basic(imgname:str, userSubTasksList:list, usertitle:str):
    """ write me pls """
    imgpath = arty.draw_dynamic_task_subtask_snapshot(imgname, userSubTasksList, usertitle)
    return(imgpath)


#@st.cache
def get_tags_list(username):
    tags_list = db.get_tags_from_db(username)
    return(tags_list)


def get_todolist_id(username, lastid):
    user_todolistid = db.get_todolistid_from_taskid(username, lastid)
    return(user_todolistid)


# ---- session state declarations ----

if "todo_lists" not in st.session_state:
    todo_dict = {}
    db_todo_lists = get_todo_lists_from_db(user_name)
    for todo in db_todo_lists:
        todo_dict[todo[0]] = todo[1]
    st.session_state["todo_lists"] = todo_dict


# ---- main page ----

def run():

    # PAGE DEF THING SHOULD BE HERE BTW!

    # ---- SECTION ----
    
    # header topper
    with topper:

        st.write("##### Your Journal")

    # ---- SECTION ----

    # todo task create intro and setup
    with form_intro:

        st.write(f"### View, Save, & Create Important Entries")
        
        col1A, _ = st.columns([4,1])
        col1A.write("Shopping list ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur \
                    voluptatum laborum ")
        st.write("---")      

    # ---- SECTION ----

    with st.container():
        st.radio("Journal Select", options=["Create New", "View Saved"], horizontal=True)
        st.write("---") 


    # ---- SECTION ----

    with st.container():  

        st.write("**Your Journal Entry**")
        todo_faux_title = st.text_input("Enter A Task Title", value="A simple example", key="td_fauxtitle")
        todo_faux_detail = st.text_area("Enter Any Additional Details (Optional)", value="A more thorough example", key="td_fauxdetail")
        st.write("---")

        # skip to end/quick add button?


    # ---- SECTION ----

    with st.container():  
        st.write("**Setup Essentials**")
        todo_list_names = create_todo_lists_list()
        assigned_todo_list = st.selectbox("Want To Find An Existing Entry?", todo_list_names)
        todolistid = get_id_numb_from_formatted_list_name(assigned_todo_list)

        st.write("**Something Task**")

        checkboxcol1, checkboxcol2, checkboxcol3 = st.columns(3)
        with checkboxcol1:
            is_subtask = st.checkbox("Make It A Sub Task?")
        with checkboxcol2:
            is_datesensitive = st.checkbox("Give It An End Date?")
        with checkboxcol3:
            if is_datesensitive:
                is_timesensitive = st.checkbox("Give It An End Time?")
            else:
                is_timesensitive = st.checkbox("Give It An End Time?", disabled=True)

        if is_subtask:
            st.write("---")
            subtaskcol1, subtaskcol2 = st.columns([3,2])
            with subtaskcol1:
                todo_lists_main_tasks_listed = get_main_tasks_for_todo_list_from_db_with_subcount(user_name, assigned_todo_list)
                # print(f"{todo_lists_main_tasks_listed = }")
                taskparentName = st.selectbox("Choose A Main Task To Assign To",todo_lists_main_tasks_listed)       
                # could make dis a function but meh
                braceindex = taskparentName.rfind("[")
                if braceindex != -1:
                    taskparentName = taskparentName[:braceindex-1]

            with subtaskcol2:
                st.write("**What's A Sub Task?**")
                st.write("Explain it to me senpai")

        task_end_date = ""

        if is_datesensitive:
            st.write("---")
            timesenscol1, timesenscol2 = st.columns(2)
            with timesenscol1:
                # should sql command to grab the current date and use it as the default
                task_end_date = st.date_input("End Date", datetime.date(2022, 7, 1))
            with timesenscol2:
                if is_timesensitive:
                    task_end_time = st.time_input('End Time', datetime.time(16, 00))
        
        st.write("---")
        st.write("##")





if __name__ == "__main__":
    run()