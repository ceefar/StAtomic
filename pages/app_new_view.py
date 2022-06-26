# ---- imports ---- 
# for web app and test components
from tkinter import PAGES
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

def get_tags_list(username):
    tags_list = db.get_tags_from_db(username)
    return(tags_list)



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


# from create but refactoring (didnt change tbf?)
def get_main_tasks_for_todo_list_from_db(username:str, formatted_list_name:str) -> list:
    """ write me """
    username = username.lower()
    listID = get_id_numb_from_formatted_list_name(formatted_list_name)
    main_tasks_for_todo_list = db.get_main_tasks_for_todo_list_by_id(username, listID)
    return(main_tasks_for_todo_list)


def disable_handy_filter(specific_or_all_tasks):
    """ disables the handy filter unless all tasks selected (not a specific parent/main task) """
    if specific_or_all_tasks != "All Tasks":
        show_handy_filter = True
        st.sidebar.error("Select ALL TASKS to use the Handy Filter")
    else:
        show_handy_filter = False
    return(show_handy_filter)



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

        st.markdown("#### Your Tasks, Your Way")

        todo_lists_main_tasks_listed = get_main_tasks_for_todo_list_from_db(user_name, assigned_todo_list)
        todo_lists_main_tasks_listed.insert(0, "All Tasks")
        specific_or_all_tasks = st.selectbox("All Tasks Or A Specific Main Task?", todo_lists_main_tasks_listed)
        enable_handy = disable_handy_filter(specific_or_all_tasks)

        st.write("##")

        optioncol1, optioncol2, optioncol3 = st.columns(3)

        with optioncol1:
            st.markdown("##### View Type")
            sub_main_or_all = st.radio("View Toggle", options=["Main Task + Subtasks", "Main Tasks Only", "Subtasks Only"]) # might remove child only tasks btw
        
        with optioncol2:
            st.markdown("##### Order By Filter") # previously called handy filter
            handy_filter_selection = st.radio("Filter Results", options=["All Tasks","Recent Tasks", "Oldest Tasks", "Stalled Tasks"], disabled=enable_handy)
            if handy_filter_selection == "Stalled Tasks":
                st.sidebar.warning("Stalled Tasks = longest time between task being created & updated") 

        with optioncol3:
            st.markdown("##### Status Filter")
            status_selection = st.radio("Sort By Status", options=["All Status Tasks", "In Progress Tasks", "Completed Tasks"])

        tags_list = get_tags_list(db_username)

        st.markdown("##### Tags Filter")
        #user_todo_tags = st.multiselect("Select Tags",tags_list, default=tags_list[0])
        user_todo_tags = st.multiselect("Select Tags",tags_list)

        print(f"{user_todo_tags = }")

        # OBVS NEEDS TO BE A LIST OR TUPLE PROBS TBF FOR EASIER UNPACKING, AND OBVS NEED TO UNPACK IT LOL (immutable tho... reruns from start tho... hmmm... should be fine)
        filter_tags = ""
        filter_tags_list = []

        for tag in user_todo_tags:
            tagndx = tag.rfind("[")
            tag_name = tag[:tagndx-1].strip()
            tag_group = tag[tagndx+1:-1]
            user_tagid = db.get_tagid_from_tag_plus_group(db_username, tag_name, tag_group)
            filter_tags = user_tagid
            filter_tags_list.append(user_tagid)
        



            
        # so (and obvs dont do this here but its just easier to sort and test it here without breaking the entire db module)
        # if just one item then this is fine 
        # AND t2.tagID = 2
        # else its + OR t2.tagID = {another_id_from_list}
        # dynamically add that to a new string variables and then just add that final variable and thats it
        # legit dont think theres any other way to do this without explicitly declaring every single thing like if PARAMETER = 2 THEN final_string.append('t2.tagID = 2') 

        # SOME KINDA COUNT HERE FOR TAGS WOULD PROBABLY BE HELLA USEFUL TOO (as not that many tags but tbf should be more tags in future)
        # LEGIT AFTER THIS THE IMG BIT WITH SAVE BUTTON 
        # - N0TE SHOW THE DYNAMIC QUERY IN A DD OR SUMNT AS IS TO SHOW MY WORK ABILITY (maybe even show it broken up too ooo - maybe even as img lol)
        # THEN GET THE TASKS IN DB TO LOOK MORE NORMALISED
        # THEN ONE MINOR THING IN THE OTHER VIEW PAGE
        # THEN DO THAT TUT!



    st.write("---")


    # ---- SECTION ----

    basic_tasks_dict_as_list = view_tasks_basic(db_username, todolistid)

    taskdict_list = db.view_tasks_toggle(db_username, todolistid, sub_main_or_all, specific_or_all_tasks, handy_filter_selection, status_selection, filter_tags_list)
    st.markdown("#### TEMP RESULT")
    #st.write(taskdict_list)

    # SO BEFORE DOING THIS FINAL PRINT NEED TO DO THE MERGE OF DICTS WITH MULTIPLE TAGS, 
    # BASICALLY JUST MATCHING ON todoTaskID and appending to tag & tagtype
    # OR EVEN A JUST A NEW VAR AND STICK IT INTO THE DICT (or even a new dict idk but should be easy enough)

    for taskdict in taskdict_list:
        if len(taskdict) > 10:
            st.write("Print With Tag Info Inherent")
            st.write(taskdict)
        else:
            st.write("No Tag Info Inherent - but can get with a separate query")
            st.write(taskdict)

    st.write("---")



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


