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


# ---- copied page functions ----

@st.cache
def get_todo_lists_from_db(username:str) -> tuple:
    """ write me pls """
    username = username.lower()
    all_user_todo_list_tuples = db.get_all_todo_list_names_and_ids(username)
    return(all_user_todo_list_tuples)


def create_todo_lists_list():
    """ write me pls """
    todo_lists = st.session_state["todo_lists"]
    todo_list_names = []
    for a_list in todo_lists.items():
        todo_list_names.append(f"{a_list[0]}. {a_list[1].replace('_',' ')}")
    return(todo_list_names)


def get_id_numb_from_formatted_list_name(formatted_list_name:str) -> int:
    """ from the currently selected list, find its id for db queries """
    assigned_todo_id = int(re.search('\d+|$',formatted_list_name).group())
    return(assigned_todo_id)


# ---- new / refactored page functions ----


def get_parent_id(username:str, task_title:str):
    username = username.lower()
    parent_id = db.get_id_for_parent(username, task_title)
    return(parent_id)


# ---- session state declarations ----

if "todo_lists" not in st.session_state:
    todo_dict = {}
    db_todo_lists = get_todo_lists_from_db(user_name)
    for todo in db_todo_lists:
        todo_dict[todo[0]] = todo[1]
    st.session_state["todo_lists"] = todo_dict


# ---- custom css test ----

HABIT_HTML_TEMPLATE = """
<div style="padding-left:15px;font-family: 'Roboto', sans-serif; font-weight:600; color:grey;">{}.</div>
<div style="width:95%; height:100%; margin:5px 20px 1px 1px; padding:1px 5px 35px 15px; position:relative; border-radius:5px;
border=5px solid; box-shadow:0 0 1px 1px #eee; background-color:#31333F; font-weight:300;
border-left:10px solid #484848; color:white; font-family: 'Roboto', sans-serif;">
<h2 style="color:#eba538; font-weight:300; margin-bottom:0px;">{}</h2>
<div style="color:#efefef; font-weight:300; margin-bottom:25px; ">{}</div>
<span style="width:95%; height:100%; position:absolute; text-align:right;">{}</span>
<span style="width:95%; height:100%; position:absolute; text-align:left;">{}</span>
</div>
"""

# ---- main page ----

def run():

    # PAGE DEF THING SHOULD BE HERE BTW!

    # ---- SECTION ----
    
    # header topper
    with st.container():

        st.write("##### View Tasks")

    # ---- SECTION ----

    # todo task create intro and setup
    with st.container():

        st.write(f"### Aite {user_name}, let's get on task!")
        
        col1A, _ = st.columns([4,1])
        col1A.write("Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur \
                    voluptatum laborum ")
        st.write("---")      

    # ---- SECTION ----

    with st.container():  

        st.write(f"#### Todo Visualiser")
        #st.write("**Your New Task**")
        
        todo_list_names = create_todo_lists_list()
        assigned_todo_list = st.selectbox("Which Todo List Would You Like To See?", todo_list_names)
        todolistid = get_id_numb_from_formatted_list_name(assigned_todo_list)
        basic_tasks_dict_as_list = db.view_tasks_basic(db_username, todolistid) #FIXME : OWN FUNCTION 


            


        for taskd in basic_tasks_dict_as_list:
            
            #st.markdown(f"{taskd}")

            stc.html(HABIT_HTML_TEMPLATE.format( taskd["taskStatus"],  taskd["title"], taskd["detail"], taskd["taskParent"], taskd["taskType"]), height=200)
            
            parents_id = taskd["taskID"]
            st.write(parents_id)
            print(f"{parents_id = }")
            basic_subtasks_dict_as_list = db.view_tasks_basic(db_username, parents_id, "child")
            st.write(basic_subtasks_dict_as_list)

            st.write("---")


        st.write("---")




if __name__ == "__main__":
    run()