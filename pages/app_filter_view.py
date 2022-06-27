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



# PLEASE GOD REFACTOR THIS, AND IF CANT REFACTOR MUCH THEN SPLIT STUFF INTO SMALLER FUNCTIONS!
# (tbf even if can refactor a lot still worth spitting up a bit)
def merge_dicts_for_repeat_tags(taskdict_list:list[dict]) -> list[dict]: 
    """ 
    (likely longwinded) func for merging tags for repeated tasks (due to relational table setup) and removing any duplicates
    created a new key called tagsList for valid tasks (with multiple tags that need to be merged into one task, then excess tasks removed)
    """
    # IF MOVING THIS FUNCTION SHOULD ONLY NEED TO PASS taskdict_list AS PARAMETER
    print("")
    # creates dict of repeating taskIDs + count that happens due to tag selection (own funct when done pls?)
    taskdict_idindex_countdict = {}
    for taskdict_forid in taskdict_list:
        if taskdict_forid['taskID'] not in taskdict_idindex_countdict:
            taskdict_idindex_countdict[taskdict_forid['taskID']] = 1
        elif taskdict_forid['taskID'] in taskdict_idindex_countdict:
            taskdict_idindex_countdict[taskdict_forid['taskID']] += 1

    # creates a list of just the counts    
    print(f"{taskdict_idindex_countdict = }")
    reapeatchecker = taskdict_idindex_countdict.values()
    print(f"{reapeatchecker = }")

    # check if those counts are > 1 (so repeats), if is greater than 1 add its index to new list
    repeatindexes = []
    dontprint = [repeatindexes.append(i) if repeater > 1 else 0 for i, repeater in enumerate(reapeatchecker)]
    print(f"{repeatindexes = }")

    # finally get whats needed, a list of task ids which repeat in the search query because they have multiple tags
    repeatids = []
    ids_fromkeys = taskdict_idindex_countdict.keys()
    ids_fromkeys_list = list(ids_fromkeys)
    print(f"{ids_fromkeys_list = }")
    for rpt_ndx in repeatindexes:
        repeatids.append(ids_fromkeys_list[rpt_ndx])
    print(f"{repeatids = }")

    # creates a dicctionary with key = taskid (with repeats), and value = list of tags (formatted tho, can obvs change easily)
    print("")
    repeating_tags_dict = {}
    for an_id in repeatids:
        for taskdict in taskdict_list:
            if taskdict['taskID'] == an_id:
                if taskdict['taskID'] not in repeating_tags_dict:
                    # created an array to store the multiple tags if doesnt already exist and add first tag+tagtype pair (formatted)
                    repeating_tags_dict[taskdict['taskID']] = [f"{taskdict['tag']} [{taskdict['tagtype']}]"]
                else:
                    # if array does already exist then append the remaining tag+tagtype pairs (formatted)
                    repeating_tags_dict[taskdict['taskID']].append(f"{taskdict['tag']} [{taskdict['tagtype']}]")
    print(f"{repeating_tags_dict = }")

    # from here you just add them to the first, pop the others off, then do formating and img
    # then do group project stuff tbf?

    print("")
    print(f"{taskdict_list}")
    print("")

    idindex_in_taskdict_list_listed = []
    for task_dict in taskdict_list:
        # listed the task ids in order so that their index in this list will be the same as their index in the other
        idindex_in_taskdict_list_listed.append(task_dict["taskID"])
        for a_task_id in repeatids:
            if task_dict["taskID"] == a_task_id:
                task_dict["tagsList"] = repeating_tags_dict[a_task_id] 
                print(f"{task_dict['tagsList']}")
            else:
                # this else case is for non repeating entries (say just 1 valid tag and thats it) to still get the tagsList key in their dictionary
                task_dict["tagsList"] = [f"{taskdict['tag']} [{taskdict['tagtype']}]"]
    
    first_entries = []
    for repeated in repeatids:
        first_entries.append(idindex_in_taskdict_list_listed.index(repeated))

    print(f"{first_entries = }")

    pop_indexes = []
    for i, anid in enumerate(idindex_in_taskdict_list_listed):
        if i not in first_entries and anid in repeatids:
            pop_indexes.append(i)
            print(f"POP INDEX {i}")

    pop_indexes.reverse()
    for popoff in pop_indexes:
        taskdict_list.pop(popoff)
            
    
    print("")
    print(f"{pop_indexes = }")
    print("")
    print(f"{idindex_in_taskdict_list_listed = }")
    print("")
    print(f"{taskdict_list = }")

    return(taskdict_list)

# END FUNCTION



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
    st.markdown("#### RESULT [temp]")
    st.write("##")


    print(f"{user_todo_tags = }")

    
    if user_todo_tags:
        tags_taskdict_list = merge_dicts_for_repeat_tags(taskdict_list)

        # print(f"{tags_taskdict_list = }")
        # print("")

        # BIG N0TE THAT THESE KINDA IMGS WILL BE FOR MAINTASK OR SUBTASK ONLY, NOT PARENT CHILD
        # NEED TO SORT THE VIEW FOR THAT ASAP AS IS RELATED TO THE IMGS!
        # - consider the use of dropdowns for each sub task, note whatever you do just keep it simple ffs! (so probably not dds then lmao)

        for tagstaskdict in tags_taskdict_list:

            taskinfocol, taskimgcol = st.columns(2)

            with taskinfocol:
                # st.markdown(f"##### {tagstaskdict['todoTaskID']}. {tagstaskdict['title']}")
                st.markdown(f"##### {tagstaskdict['title']}")
                st.markdown(f"{tagstaskdict['detail']}")

                st.markdown(f"{tagstaskdict['tagsList']}")         

                st.markdown(f"{tagstaskdict['taskStatus']}")    

                days_since_created = db.get_days_between_a_days_and_today(tagstaskdict['createdDate'])
                st.markdown(f"Created : {tagstaskdict['createdDate']} - {days_since_created} Days Ago")
                if tagstaskdict['updatedDate']:
                    days_since_updated = db.get_days_between_a_days_and_today(tagstaskdict['updatedDate'])
                    st.markdown(f"Last Updated : {tagstaskdict['updatedDate']} - {days_since_updated} Days Ago")

            with taskimgcol:
                imgpath = arty.draw_task_snapshot_test_af(tagstaskdict['todoTaskID'], tagstaskdict['tagsList'], tagstaskdict['title'], tagstaskdict['detail'])
                st.image(imgpath)

                with open(imgpath, "rb") as file:
                    btn = st.download_button(
                            label="Download image",
                            data=file,
                            file_name=f"task_{tagstaskdict['todoTaskID']}.png",
                            mime="image/png",
                            key=tagstaskdict['todoTaskID']
                        )

            st.write("---")

            # todoTaskID, title, detail, tagsList, taskStatus, createdDate, days_since_created, IF VALID : updatedDate, days_since_updated
    
    else:
        # else isnt a tags based query result so is slightly different display (as the dictionary as less keys)
        # means dont have to do len(taskdict) > 10 as before
        # note will likely still want tag info (maybe not rn tho) but will require a separate query to get it for this section
        
        # print(f"{taskdict_list = }")

        for taskdict in taskdict_list:    

            st.markdown(f"##### {taskdict['taskID']}. {taskdict['title']}")      
            st.markdown(f"{taskdict['detail']}")

            st.write("---")


    # BIG N0TE THAT IMG HERE WILL NEED A REPEATING KEY SINCE DONT WANT A JILLION IMGS

    






    # can delete this btw?
    with st.container():
        
        for j, taskd in enumerate(basic_tasks_dict_as_list):
            
            
            st.write("##")
            #st.write(f"#### Task {j+1}")

            parents_id = taskd["taskID"]

            basic_subtasks_dict_as_list = db.view_tasks_basic(db_username, parents_id, "all")
 
            for i, subtaskd in enumerate(basic_subtasks_dict_as_list):
                #st.write(subtaskd)
                pass

                
                    

        st.write("---")



    # css testing
    st.markdown(unsafe_allow_html=True, body=f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
            </style>
        """)



if __name__ == "__main__":
    run()


