# ---- imports ---- 
# for web app and test components
import streamlit as st
import streamlit.components.v1 as stc # < unused at present
# for db access
import db_integration as db
# for datetime object
import datetime
# for regular expressions
import re


# ---- temp globals ----
# for testing/setup

user_name = "Ceefar"
user_tags = ["fitness - cardio","fitness - trim","fitness - bulk","conditions - adhd","conditions - anxiety","skills - mysql","skills - portfolio","skills - programming","software - streamlit","lifestyle - wellness"]


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
def get_main_tasks_for_todo_list_from_db(username:str, formatted_list_name:str) -> tuple:
    """ write me """
    username = username.lower()
    listID = get_id_numb_from_formatted_list_name(formatted_list_name)
    main_tasks_for_todo_list = db.get_main_tasks_for_todo_list_by_id(username, listID)
    return(main_tasks_for_todo_list)
        

def add_basic_task_to_db(username:str, todoListID:int, taskTitle:str, taskDetail:str = "", taskParentID:int = ""):
    """ write me pls """
    db.add_todo_task_to_db_basic(username, todoListID, taskTitle, taskDetail, taskParentID)


def create_todo_lists_list():
    """ write me pls """
    todo_lists = st.session_state["todo_lists"]
    todo_list_names = []
    for a_list in todo_lists.items():
        todo_list_names.append(f"{a_list[0]}. {a_list[1].replace('_',' ')}")
    # legit prints the list comprehension which is super annoying as its clean af
    # [todo_list_names.append(f"{a_list[0]}. {a_list[1].replace('_',' ')}") for a_list in todo_lists.items()] 
    return(todo_list_names)


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

        st.write("**Setup Essentials**")
        todo_list_names = create_todo_lists_list()
        assigned_todo_list = st.selectbox("Which Todo List Should We Add This To?", todo_list_names)

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
                todo_lists_main_tasks_listed = get_main_tasks_for_todo_list_from_db(user_name, assigned_todo_list)
                taskparentID = st.selectbox("Choose A Main Task To Assign To",todo_lists_main_tasks_listed)        
                # print(f"{taskparentID = }")
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
    with st.form(key="todo_task_creator"):

        # SERIOUSLY THINK ABOUT THIS (AND MAYBE ACTUALLY TRY BOTH WAYS - DOES THIS EVEN NEED TO BE A FORM THO?)

        todo_title = st.text_input("Here Is Your Task Title", value=todo_faux_title, key="td_title")

        todo_detail = st.text_area("Here Are The Task Details", value=todo_faux_detail, key="td_detail")
        
        submit_habit_form = st.form_submit_button(label="Add Task")

        todolistid = get_id_numb_from_formatted_list_name(assigned_todo_list)

        db_username = user_name.lower()

        if is_subtask:
            parentID = db.get_parent_id_from_title(db_username, taskparentID, todolistid)
        else:
            parentID = ""

        taskStatus = 1 # << ADD DISSSS!

        if submit_habit_form:
            if parentID == "":
                add_basic_task_to_db(db_username, todolistid, todo_title, todo_detail)
            else:
                add_basic_task_to_db(db_username, todolistid, todo_title, todo_detail, parentID)
            
            # FIRST CONFIRMATION AND CLEAR FOR - MAYBE A QUERY FOR CONFIRMATION BTW!
            # ALSO BOTTOM PAGE BIT NEEDS INDICATOR FOR THE CURRENT TD LIST AND PARENT ETC
            # CAN LEGIT BE TEXT NOT DDS, BUT THEN INCLUDE AN ACHOR OR SKIP TO TOP BUTTON!
            #
            # THEN GET THE TOGGLE ACTUALLY MAKING ADD AS A PARENT THEN GET THE DISPLAY FOR THAT
            # MAYBE ACTUALLY JUST IN PRINT PAGE THO DUH AND FFS FORGET ANY FORMATTING RN!


        # SO NEED ADD STANDARD, THEN ADD IF IS PARENT CHILD WITH PROPER RELATIONSHIP
        # WOULD ALSO LIKE TO DISPLAY IF A THING DOES HAVE PARENT CHILD RELATIONSHIP WHEN U SELECT SUBTASK? 
        #   - FOR THE SPECIFIC ONE RIGHT SO YOU CAN SEE IT



if __name__ == "__main__":
    run()