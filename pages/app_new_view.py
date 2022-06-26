# ---- imports ---- 
# for web app and test components
import streamlit as st
import streamlit.components.v1 as stc # < unused at present
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


# ---- copied page functions [create] ----

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


# ---- copied page functions [subtask view] ----


def get_parent_id(username:str, task_title:str):
    """ self referencing af """
    username = username.lower()
    parent_id = db.get_id_for_parent(username, task_title)
    return(parent_id)


def toggle_task_status(db_username, taskID, agree):
    """ write me """
    db.update_task_status(db_username, taskID, agree)



# ---- new / refactored page functions ----


def view_tasks_basic(db_username, todolistid):
    """ write me """
    list_of_task_dicts = db.view_tasks_basic(db_username, todolistid)
    return(list_of_task_dicts)




# ---- session state declarations ----

if "todo_lists" not in st.session_state:
    todo_dict = {}
    db_todo_lists = get_todo_lists_from_db(user_name)
    for todo in db_todo_lists:
        todo_dict[todo[0]] = todo[1]
    st.session_state["todo_lists"] = todo_dict



# ---- custom css elements ----

# was originally really just for testing tbf but leaving as might use more
MATERIAL_ICON_POSITIVE = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:#AAFF00'>add_circle</i>"
MATERIAL_ICON_NEUTRAL = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:yellow'>do_not_disturb_on</i>"
MATERIAL_ICON_NEGATIVE = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:red'>disabled_by_default</i>"
MATERIAL_ICON_TASK_ALT = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:#AAFF00'>task_alt</i>"
MATERIAL_ICON_ADD_TASK = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:#AAFF00'>add_task</i>"



# ---- main page ----

def run():

    # PAGE DEF THING SHOULD BE HERE BTW!

    # ---- SECTION ----
    
    # header topper
    with st.container():

        st.write("##### Tasks - QuickView & Download")

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

        st.write(f"#### Get Started")
        todo_list_names = create_todo_lists_list()
        assigned_todo_list = st.selectbox("Which Todo List Would You Like To See?", todo_list_names)
        todolistid = get_id_numb_from_formatted_list_name(assigned_todo_list)
        st.write("---")


    # ---- SECTION ----

    with st.container():

        optioncol1, optioncol2, optioncol3 = st.columns(3)

        with optioncol1:
            st.markdown("##### Select View Type")
            st.radio("View Toggle", options=["Main Task + Subtasks", "Main Tasks Only", "Subtasks Only"]) # might remove child only tasks btw
        
        with optioncol2:
            st.markdown("##### Handy Filter")
            st.radio("Filter Results", options=["All Tasks","Recent Tasks", "Stalled Tasks"])

        with optioncol3:
            st.markdown("##### Tags Filter")
            st.multiselect("Select Tags", options=["Tag1","Tag2"])

    st.write("---")


    # ---- SECTION ----

    basic_tasks_dict_as_list = view_tasks_basic(db_username, todolistid)



    with st.container():
        
        for j, taskd in enumerate(basic_tasks_dict_as_list):
            
            
            st.write("##")
            st.write(f"#### Task {j+1}")

            parents_id = taskd["taskID"]

            basic_subtasks_dict_as_list = db.view_tasks_basic(db_username, parents_id, "all")
 
            for i, subtaskd in enumerate(basic_subtasks_dict_as_list):
                st.write(subtaskd)

                
                    

        st.write("---")



    # css testing
    st.markdown(unsafe_allow_html=True, body=f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
            </style>
        """)



if __name__ == "__main__":
    run()


