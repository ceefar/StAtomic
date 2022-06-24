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
user_tags = ["fitness - cardio","fitness - trim","fitness - bulk","conditions - adhd","conditions - anxiety","skills - mysql","skills - portfolio","skills - programming","software - streamlit","lifestyle - wellness"]
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
        

@st.cache
def get_parent_subtask_count(username:str, task_title:str):
    username = username.lower()
    subtask_count = db.get_count_of_subtasks_for_parent(username, task_title)
    return(subtask_count)


def add_basic_task_to_db(username:str, todoListID:int, taskTitle:str, taskDetail:str = "", taskParentID:int = ""):
    """ write me pls """
    db.add_todo_task_to_db_basic(username, todoListID, taskTitle, taskDetail, taskParentID)


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


@st.cache
def create_task_subtask_img_basic(imgname:str, userSubTasksList:list, usertitle:str):
    """ write me pls """
    imgpath = arty.draw_dynamic_task_subtask_snapshot(imgname, userSubTasksList, usertitle)
    return(imgpath)




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

        st.write("##### Create Task")

    # ---- SECTION ----

    # todo task create intro and setup
    with form_intro:

        st.write(f"### So {user_name}, what are we planning?")
        
        col1A, _ = st.columns([4,1])
        col1A.write("Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur \
                    voluptatum laborum ")
        st.write("---")      

    # ---- SECTION ----

    with st.container():  

        st.write("**Your New Task**")
        todo_faux_title = st.text_input("Enter A Task Title", value="A simple example", key="td_fauxtitle")
        todo_faux_detail = st.text_area("Enter Any Additional Details (Optional)", value="A more thorough example", key="td_fauxdetail")
        st.write("---")

        # skip to end/quick add button?


    # ---- SECTION ----

    with st.container():  
        
        st.header("Setup Essentials")
        #st.write("**Setup Essentials**")
        todo_list_names = create_todo_lists_list()
        assigned_todo_list = st.selectbox("Which Todo List Should We Add This To?", todo_list_names)
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

        if is_datesensitive:
            st.write("---")
            timesenscol1, timesenscol2 = st.columns(2)
            with timesenscol1:
                task_end_date = st.date_input("End Date", datetime.date(2022, 7, 6))
            with timesenscol2:
                if is_timesensitive:
                    task_end_time = st.time_input('End Time', datetime.time(16, 00))
        
        st.write("---")
        st.write("##")

    with st.container():  
        
    # ---- SECTION ----

        st.write("**Advanced Setup**") 
        # st.write("Use these optional enhancements to make getting stuff done easier by taking 30 seconds to quickly configure...") # not configure its not a techy app its a todo list ffs
        with st.expander("Task Tags", expanded=True):
            st.write("What Areas Does This Relate To?")
            habit_tags = st.multiselect("Add Tags",user_tags, default=user_tags[7])
            st.write("You can update tags later blah... by adding tags St.Atomic can help you form connections between similar habits lorem")
        
        with st.expander("Task Difficulty"): #, expanded=True
            col1A,col3A = st.columns([2,3])
            col1A.write("How Difficulty")
            col3A.write("What Is Difficulty")

            ##### DUH FORMS DONT UPDATE EVERY RUN THROUGH!

            col1D,_,col3D = st.columns([1,1,3])
            with col1D:
                todo_type = st.radio("Set The Difficulty",
                ('complicated', 'complex', 'average', 'simple'))
            with col3D:
                st.write("critical - Describe me daddy")

        with st.expander("Task Impact"):
            col1E,col3E = st.columns([2,3])
            col1E.write("How Impact")
            col3E.write("What Is Imapct")

            col1E,_,col3E = st.columns([1,1,3])
            with col1E:
                todo_type = st.radio("Set The Impact",
                ('massive', 'significant', 'limited', 'minor'))
            with col3E:
                st.write("critical - Describe me daddy")

        with st.expander("Task Urgency"):
            col1F,col3F = st.columns([2,3])
            col1F.write("How Urgent Is This Task?")
            col3F.write("What Is Urgency")

            col1F,_,col3F = st.columns([1,1,3])
            with col1F:
                todo_urgency = st.radio("Set The Urgency",
                ('critical', 'urgent', 'moderate', 'low', 'none'))
            with col3F:
                st.write("critical - Describe me daddy")

        st.write("---")        
        st.write("##")


    # ---- MAIN FORM ----
    st.write("**Confirm & Add**")
    with st.form(key="todo_task_creator", clear_on_submit=True):

        # SERIOUSLY THINK ABOUT THIS (AND MAYBE ACTUALLY TRY BOTH WAYS - DOES THIS EVEN NEED TO BE A FORM THO?)

        todo_title = st.text_input("Here Is Your Task Title", value=todo_faux_title, key="td_title")

        todo_detail = st.text_area("Here Are The Task Details", value=todo_faux_detail, key="td_detail")

        # status indicators - need more of these
        st.write("##")
        
        if is_subtask:
            #FIXME
            tempcol1, tempcol2 = st.columns(2)
            parent_subtasks = get_subtasks_for_parent(db_username, taskparentName, todolistid)   
            imgpath = create_task_subtask_img_basic(f"{db_username}_temp_subtasks", parent_subtasks, taskparentName)     
            tempcol2.image(imgpath)
            tempcol1.write(f"##### Will Be Added To...")
            tempcol1.write(f"Todo List - **{assigned_todo_list}**")
            tempcol1.write(f"A Sub Task Of - **{taskparentName}**")
            # print(f"{taskparentName = }")
            # print(f"{todolistid = }")
            parent_subtasks = get_subtasks_for_parent(db_username, taskparentName, todolistid)
            for i, tasks in enumerate(parent_subtasks):
                #_ ,temptaskcol = st.columns([1,6])
                tempcol1.markdown(f" *-* {i+1}. **{tasks}**")
            tempcol1.markdown("<sup>[Update Task](#setup-essentials)</sup>", unsafe_allow_html=True)
        else:
            st.write("Put Some Info Here")


        # SUBMIT BUTTON
        submit_habit_form = st.form_submit_button(label="Add Task")


        if is_subtask:
            #FIXME: OWN FUNCTION! 
            parentID = db.get_parent_id_from_title(db_username, taskparentName, todolistid)
        else:
            parentID = ""

        taskStatus = 1 # << ADD DISSSS!

        if submit_habit_form:
            try:
                if parentID == "":
                    add_basic_task_to_db(db_username, todolistid, todo_title, todo_detail)
                    st.success(f"**{todo_title}**\nadded to -> **{assigned_todo_list}**\nsuccessfully ")
                elif parentID and is_subtask:
                    add_basic_task_to_db(db_username, todolistid, todo_title, todo_detail, parentID)
                    st.success(f"**{todo_title}**\nadded to -> **{assigned_todo_list}**\npaired to -> **{taskparentName}**\nsuccessfully ")
                    parent_subtasks = get_subtasks_for_parent(db_username, taskparentName, todolistid)   
                    imgpath = create_task_subtask_img_basic(f"{db_username}_temp_subtasks", parent_subtasks, taskparentName)                 
                    print(f"{parent_subtasks = }")
                    print(f"{taskparentName = }")
                    st.write(imgpath)
                    st.image(imgpath)

            # try except test
            except pymysql.err.OperationalError as pymyerr:
                # OperationalError ProgrammingError
                st.exception(f"OpErr : {pymyerr}")

            




        # SO NEED ADD STANDARD, THEN ADD IF IS PARENT CHILD WITH PROPER RELATIONSHIP
        # WOULD ALSO LIKE TO DISPLAY IF A THING DOES HAVE PARENT CHILD RELATIONSHIP WHEN U SELECT SUBTASK? 
        #   - FOR THE SPECIFIC ONE RIGHT SO YOU CAN SEE IT



if __name__ == "__main__":
    run()