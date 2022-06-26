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
    """ self referencing af """
    username = username.lower()
    parent_id = db.get_id_for_parent(username, task_title)
    return(parent_id)


def toggle_task_status(db_username, taskID, agree):
    """ write me """
    db.update_task_status(db_username, taskID, agree)


# ---- session state declarations ----

if "todo_lists" not in st.session_state:
    todo_dict = {}
    db_todo_lists = get_todo_lists_from_db(user_name)
    for todo in db_todo_lists:
        todo_dict[todo[0]] = todo[1]
    st.session_state["todo_lists"] = todo_dict


# ---- custom css test ----

# FIXME: THIS *** IMPORTANT - IF NO DETAIL IS RESIZED SO NEED TO UPDATE THE HEIGHT! *** # 

PARENT_HTML_TEMPLATE = """
<div style="padding-left:15px;font-family: 'Roboto', sans-serif; font-weight:600; color:grey;">{}</div>
<div style="width:90%; height:100%; margin:5px 20px 1px 1px; padding:1px 5px 35px 15px; position:relative; border-radius:5px;
border=5px solid; box-shadow:0 0 1px 1px #eee; background-color:#31333F; font-weight:300;
border-left:10px solid #484848; color:white; font-family: 'Roboto', sans-serif; box-shadow: 10px 10px 5px 5px rgba(0,0,0,0.15);">
<h2 style="color:#eba538; font-weight:300; margin-bottom:0px;">{}</h2>
<div style="color:#efefef; font-weight:300; margin-bottom:25px; ">{}</div>
<span style="width:95%; height:100%; position:absolute; text-align:right; font-size:0.9rem; color:#949494;">{}</span>
<span style="width:95%; height:100%; position:absolute; text-align:left;">{}</span>
</div>
"""

# N0TE THE BOX SHADOW LOOKS MUCH BETTER ON DARK THEME - SO IMPLEMENT DARK STYLE THEME AS THE PRESET PLS
CHILD_HTML_TEMPLATE = """
<div style="padding-left:15px; padding-top:10px; font-family: 'Roboto', sans-serif; font-weight:600; color:grey;">{}</div>
<div style="width:60%; height:100%; margin:5px 20px 1px 1px; padding:1px 0px 35px 10px; position:relative; border-radius:5px;
border=5px solid; box-shadow:0 0 1px 1px #eee; background-color:#31333F; font-weight:300;
border-left:10px solid #484848; color:white; font-family: 'Roboto', sans-serif; box-shadow: 8px 5px 5px 5px rgba(49,51,63,0.15);">
<h2 style="color:#{}; font-weight:300; margin-bottom:0px;">{}</h2>
<div style="color:#efefef; font-weight:300; ">{}</div>
<span style="width:95%; height:100%; position:absolute; text-align:right; font-size:0.9rem; color:#949494;">{}</span>
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
        

        def check_for_status_toggle(taskid, previousvalue):
            """ 
            uses the taskid (which is the key of the widget), plus 2 predeclared session state vars, a changing *current* value and a fixed *previous* value
            and compares them, as on first run through these vars will be the same (nothing has changed so previous and current match),
            but when one is toggled, the true current (which is the state of the toggle with the same key as its taskid) will now be different from the previous value,
            implemented this way as, well A im still getting to grips with session state, and B because the vars are declared in a loop, 
            so before when one was toggled they would all toggle and become their opposites, this resolves that problem.
            this function is called via callback, when the given widget is toggled, the args are passed on change.
            """
            # the session state is set by taskid for each toggle widget, but tho its a number must be access as a string
            session_string = str(taskid)
            true_current = st.session_state[session_string]
            #print(f"{st.session_state[session_string] = }")
            if true_current != previousvalue:
                #send the id to be updated
                print(f"UPDATE {taskid}")
                toggle_task_status(db_username, taskid, previousvalue)


        for j, taskd in enumerate(basic_tasks_dict_as_list):
            
            st.write("---")
            st.write("##")
            st.write(f"##### Main Task {j+1}")

            stc.html(PARENT_HTML_TEMPLATE.format(taskd["taskStatus"], taskd["title"], taskd["detail"], taskd["createdDate"], taskd["taskType"]), height=200)
            
            parents_id = taskd["taskID"]

            basic_subtasks_dict_as_list = db.view_tasks_basic(db_username, parents_id, "child")
            #_, subtaskcol2 = st.columns([1,6]) 

            # YOU DONT NEED TO USE COL HERE JUST USE THE WIDTH % AND MARGIN/PADDING THEN CAN USE COLS FOR THE SLIDER
            # OR IDK JUST FIGURE IT OUT, POSSIBLY COULD REVERT TO CHECKBOX

            #with subtaskcol2:
                #only_once = True
            for i, subtaskd in enumerate(basic_subtasks_dict_as_list):

                actual_current_status = db.get_current_status(db_username, subtaskd["taskID"])
                
                if subtaskd["taskID"] not in st.session_state:
                    st.session_state[subtaskd["taskID"]] = actual_current_status

                if subtaskd["taskStatus"] == "completed":
                    stc.html(CHILD_HTML_TEMPLATE.format(subtaskd["taskStatus"], "32CD32", subtaskd["title"], subtaskd["detail"], subtaskd["createdDate"], subtaskd["taskType"]), height=160)
                else:
                    stc.html(CHILD_HTML_TEMPLATE.format(subtaskd["taskStatus"], "eba538", subtaskd["title"], subtaskd["detail"], subtaskd["createdDate"], subtaskd["taskType"]), height=160)
                #stc.html(CHILD_HTML_TEMPLATE.format(subtaskd["taskStatus"], subtaskd["title"], subtaskd["detail"], subtaskd["createdDate"], subtaskd["taskType"]), height=160)
                
                actual_current_status = db.get_current_status(db_username, subtaskd["taskID"])
                st.session_state[f'{subtaskd["taskID"]}PREV'] = actual_current_status
                slidercol1, _ = st.columns([4,2])
                # changed from slider, looks cleaner, plus more options for additions (extra user inputs) now too
                with slidercol1:
                    
                    #status_select = st.select_slider(f'Set Status', value=actual_current_status, options=['in_progress','completed'], key=subtaskd["taskID"], on_change=check_for_status_toggle, args=[subtaskd["taskID"], st.session_state[f'{subtaskd["taskID"]}PREV']])
                    print(f"{actual_current_status = }")
                    if actual_current_status == "completed":
                        radioindexint = 1
                    else:
                        radioindexint = 0
                    st.radio("Set Status", index=radioindexint, options=['in_progress','completed'], key=subtaskd["taskID"], on_change=check_for_status_toggle, args=[subtaskd["taskID"], st.session_state[f'{subtaskd["taskID"]}PREV']])
                st.write("---")


                    

        st.write("---")



    # css testing
    st.markdown(unsafe_allow_html=True, body=f"""
            <style>
            .css-8msczc{{
                margin-bottom: -10px
            }}
            .css-1ws1sb4.e1tzin5v0{{
                gap:0rem;
            }}
            .stCheckbox{{
                padding: 10px 0px 10px 10px
            }}
            </style>
        """)
        #css-1jae3nz



if __name__ == "__main__":
    run()


