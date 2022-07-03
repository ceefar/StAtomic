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
# for randomisation
import random
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

        st.write("##### Shopping List Beta")

    # ---- SECTION ----

    # todo task create intro and setup
    with form_intro:

        st.write(f"### Check Out Before The Checkout")
        
        col1A, _ = st.columns([4,1])
        col1A.write("Anytime you use the shopping list tag we'll automatically save and store the list for your here in a handy lorem, simple for now, will expand to proper journal shortly, to be view, save, and create important entries or just document your life one entry at a time lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur \
                    voluptatum laborum ")
        st.write("---")      

    # ---- SECTION ----

    with st.container():
        saved_or_new = st.radio("List Select", options=["View Saved", "Create New"], horizontal=True)
        st.write("---") 

    # ---- SECTION ----

    basket_images = ["https://cdn-icons-png.flaticon.com/512/3724/3724788.png",
                "https://i0.wp.com/img.talkandroid.com/uploads/2015/08/cinnamon-icon.png",
                "https://www.shareicon.net/data/256x256/2016/05/05/760099_food_512x512.png"]


    if saved_or_new == "View Saved":
        with st.container():  
            st.write("**Your Shopping Lists**")
            todo_list_names = create_todo_lists_list()
            shopping_tasks = db.get_shopping_list_tag_tasks_only(db_username)

            shop_tasks_dict_list = []
            for task in shopping_tasks:
                shoptask = db.view_tasks_basic(db_username, task, "shop")
                shop_tasks_dict_list.append(shoptask)

            shop_task_titles = []
            dont_print = [shop_task_titles.append(task[0]["title"]) for task in shop_tasks_dict_list]
            print(f"{shop_task_titles = }")
            
            # NEED CASE FOR IF NONE BTW!
            amount_of_shop_tasks = len(shop_tasks_dict_list)
            if (amount_of_shop_tasks % 2) != 0:
                cards_one = amount_of_shop_tasks // 2
                cards_two = cards_one + 1

            shop_task_titles_for_titles = shop_task_titles.copy()

            shop_task_titles_for_titles.insert(0, "All Shopping Lists")

            assigned_todo_list = st.selectbox("Choose An Existing Shopping List", shop_task_titles_for_titles)
            st.button(label="Go To This List")

        # ---- NEW CARD SECTION ----

        st.write("##") 
 
        cardcol1, cardcol2 = st.columns(2)
        with cardcol1:
            temptitlestwo = shop_task_titles[cards_two:]
            #print(f"{temptitlesone = }")
            for i in range (cards_one):
                # FIXME: do this properly using the tags not the title! 
                if "Toiletries" in temptitlestwo[i]:
                    img = "https://cdn-icons-png.flaticon.com/512/3419/3419660.png"
                    stc.html(SHOP_CARD_4_HTML_TEMPLATE_TOIL.format(temptitlestwo[i], img, "Some Text"), height=420)
                else:
                    img = basket_images[random.randint(0, 2)]
                    stc.html(SHOP_CARD_4_HTML_TEMPLATE.format(temptitlestwo[i], img, "Some Text"), height=420)
        with cardcol2:
            temptitlesone = shop_task_titles[:cards_one+1]
            #print(f"{temptitlestwo = }")
            for i in range (cards_two):
                stc.html(SHOP_CARD_4_HTML_TEMPLATE.format(temptitlesone[i], basket_images[random.randint(0, 2)], "Some Text"), height=420)

    else:
        with st.container():  

            st.write("**Your Journal Entry**")
            todo_faux_title = st.text_input("Enter A Task Title", value="A simple example", key="td_fauxtitle")
            todo_faux_detail = st.text_area("Enter Any Additional Details (Optional)", value="A more thorough example", key="td_fauxdetail")
            st.write("---")

        # skip to end/quick add button?
 


    # ON WAKE - QUICKLY DO THIS PAPER TING THEN DO CV!
    # LEGIT ITS NOT ATOMIC ITS AN ADHD APP NOW LOL (tho not just adhd tbf but best for it so think about shit exclusively for you - yay!)

    # DO CARD INFO SO IS WORKING (NOT JUST DUMMY BS TEXT) 
    # IF SELECT ONE VIA DROPDOWN YOU GET A BIT MORE INFO (slightly larger (maybe full width) card)
    # THEN IF BUTTON IT DOES A PROPER DISPLAY TING WITH PRINT ETC && THIS PAPER IDEA TING!

    # K NOW OBVS GET THE SHIT FORMATTED PROPERLY CARDS (v basic nice and quick)
        # HAVE THOSE IMGS RANDOMISE PLS?!! (or more based on whats in the basket, maybe you set it idk)

    # QUICKLY TRY THE ENTRY WITH THE CSS PAPER THINGS LOOKS SO SICK OMD

    # I THINK FOR THIS MAYBE SHOULD ONLY BE THE PARENT FOR NOW
        # THO DEFO KIDS IN FUTURE WHICH CAN BE LIKE SMALL ITERATIONS 
        # i.e. mexican, obvs shopping list still has the main shit but then sometimes u have a list with a few changes bosh
        # ACTUALLY FUCK IT IMPLEMENT THIS IF IS EASY ENOUGH
    # THEN WHEN YOU TAP A CARD ITS JUST GUNA OPEN IT IN HERE! 
        # button might have to be under the card unless see if can merge st and html?! or even just own html button as trigger/link>!
    # WHEN OPEN ITS GUNA SHOW YOU THE DETAILED LIST
    # PLUS OPTION TO DOWNLOAD AS IMG!
    # OPTION TO TICK OFF AS YOU GO
    # OPTION TO MAKE EDITS, ADD NEW ?????
    # OMG REPLACE ICON THAT SHOWS SIMILAR (not functional but can implement slowly machine learning similar foods)
    # WHEN DONE SAVE EDITS IF HAVING ???? WOULD BE AS CHILD AS NEVER WANNA DELETE (tho you can if you want to)
    # ENTER HOW MUCH IT COST, LOCATION, ETC?

    # ONCE THIS IS DONE EITHER...
    # DC BASIC WEBHOOK SUMNT 
    #   - say like if it was every day at x time for example ooooo DO THIS TBF! SO HAVE BASICS! 
    #   - and send an img via dc of a current task or sumnt ooooo!!!!
    # OTHER PAGES (OR THIS PAGE TBF) FULL WEB/DB REFACTOR TEST
    # &/OR CV



# top div centers card
# 2nd div main top setup with gradient bg
# 3rd div for card structure
# 4th and 5th div for text
# 6th div for img
# 7th div main bottom setup with white bg and text
# 8th h2 for text

#FIXME : format the card img size and could sort better overlay & dimensions on it as img too tbf!

SHOP_CARD_4_HTML_TEMPLATE = """
<div style="display:flex; justify-content:center; align-items:center;">
<div style="width:90%; height:100%; padding:50px 0px 0px 0px; position:relative; border-radius:40px; 
box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
background: url('https://thehardgainerbible.com/wp-content/uploads/2022/07/abstract-blur-defocused-supermarket.jpg');
background-size: cover; background-color:rgba(42,46,63,0.95); background-blend-mode: overlay;>
<div style="width:100%; height:100%; position:relative;">
<div style="font-size:1.7rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:20px; padding-right:100px; padding-bottom:20px;
font-weight:500;">{}</div>
<div style="height:100%; padding:0px 10px 90px 0px;"><img src ="{}" 
style="display: flex; flex-direction: column; justify-content: space-between; position: relative; filter: drop-shadow(5px 5px 10px #0F1620);
min-height: 100px; max-height:120px; float:right">
</div>
<div style="width:auto; height:100%; positiion:relative; background-color:white; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
padding: 20px 0px 50px 15px; border-radius:0px 0px 40px 40px; font-family: 'Roboto', sans-serif;">
Some Text
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}</h2>
</div>
</div>
</div>
</div>
"""


SHOP_CARD_4_HTML_TEMPLATE_TOIL = """
<div style="display:flex; justify-content:center; align-items:center;">
<div style="width:90%; height:100%; padding:50px 0px 0px 0px; position:relative; border-radius:40px; 
box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
background: url('https://www.ayewanderful.com/wp-content/uploads/2018/03/Travel-Toiletry-Bag-Essentials-Carry-On-Luggage-1440x809.jpg');
background-size: auto 100vh; background-color:rgba(42,46,63,0.95); background-blend-mode: overlay; background-repeat: no-repeat;>
<div style="width:100%; height:100%; position:relative;">
<div style="font-size:1.7rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:20px; padding-right:100px; padding-bottom:20px;
font-weight:500;">{}</div>
<div style="height:100%; padding:0px 10px 90px 0px;"><img src ="{}" 
style="display: flex; flex-direction: column; justify-content: space-between; position: relative; filter: drop-shadow(5px 5px 10px #0F1620);
min-height: 100px; max-height:120px; float:right">
</div>
<div style="width:auto; height:100%; positiion:relative; background-color:white; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
padding: 20px 0px 50px 15px; border-radius:0px 0px 40px 40px; font-family: 'Roboto', sans-serif;">
Some Text
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}</h2>
</div>
</div>
</div>
</div>
"""


# https://www.smartertravel.com/wp-content/uploads/2015/01/toiletries-flat-lay-toothbrush-shampoo-brush-towel.jpg

# https://thehardgainerbible.com/wp-content/uploads/2022/07/abstract-blur-defocused-supermarket.jpg
# https://thehardgainerbible.com/wp-content/uploads/2022/07/abstract-blur-supermarket.jpg
# background-position: center;
# background-color:rgba(71,71,71,0.95);
# rgba(52,58,79,0.95)
# 42,46,63


SHOP_CARD_3_HTML_TEMPLATE = """
<div style="display: flex; justify-content: center; align-items: center;">
<div style="width:90%; height:100%; padding:50px 0px 0px 0px; position:relative; border-radius:40px; 
box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); background: linear-gradient(120deg, #343A4F, #483d8b);>
<div style="width:100%; height:100%; position:relative;">
<div style="font-size:1.3rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:15px;">Shopping</div>
<div style="font-size:1.3rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:15px;">List</div>
<div style="height:100%; padding:0px 10px 100px 0px;"><img src ="{}" 
style="display: flex; flex-direction: column; justify-content: space-between; position: relative; filter: drop-shadow(5px 5px 10px #0F1620);
min-height: 100px; max-height:120px; float:right">
</div>
<div style="width:auto; height:100%; positiion:relative; background-color:white; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
padding: 10px 0px 50px 15px; border-radius:0px 0px 40px 40px; font-family: 'Roboto', sans-serif;">
Some Text
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}</h2>
</div>
</div>
</div>
</div>
"""




#stc.html(SHOP_CARD_2_HTML_TEMPLATE.format(db_username), height=550)

SHOP_CARD_2_HTML_TEMPLATE = """
<div style="width:40%; height:100%; padding:50px 0px 0px 0px; position:relative; border-radius:40px; 
box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); background: linear-gradient(120deg,  #343A4F, #0F1620);>
<div style="width:100%; height:100%; position:relative;">
<div style="font-size:1.3rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:15px;">Shopping</div>
<div style="font-size:1.3rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:15px;">List</div>
<div style="height:100%; padding:0px 10px 100px 0px;"><img src ="https://www.shareicon.net/data/256x256/2016/05/05/760099_food_512x512.png" 
style="display: flex; flex-direction: column; justify-content: space-between; position: relative; filter: drop-shadow(5px 5px 10px #0F1620);
min-height: 100px; max-height:120px; float:right">
</div>
<div style="width:auto; height:100%; positiion:relative; background-color:white; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
padding: 10px 0px 50px 15px; border-radius:0px 0px 40px 40px; font-family: 'Roboto', sans-serif;">
Some Text
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}</h2>
</div>
</div>
</div>
"""


# ---- NOT USING RN BUT PLS SAVE AS WILL WANT TO REFERENCE FOR SURE! ----

SHOP_CARD_1_HTML_TEMPLATE = """
<div style="width:40%; height:100%; padding:50px 0px 0px 0px; position:relative; border-radius:40px; 
box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); background: linear-gradient(120deg,  #343A4F, #0F1620);>
<div style="width:100%; height:100%; position:relative;">
<div style="font-size:1.3rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:15px;">Shopping</div>
<div style="font-size:1.3rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:15px;">List</div>
<div style="height:100%; padding:0px 10px 160px 0px"><img src ="https://www.shareicon.net/data/256x256/2016/05/05/760099_food_512x512.png" 
style="display: flex; flex-direction: column; justify-content: space-between; position: relative; filter: drop-shadow(5px 5px 10px #0F1620);
min-height: 100px; max-height:120px; float:right;
box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15);">
</div>
<div style="width:auto; height:100%; positiion:relative; background-color:white; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
padding: 10px 0px 50px 15px; border-radius:0px 0px 40px 40px; font-family: 'Roboto', sans-serif;">
Some Text
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}</h2>
</div>
</div>
</div>
"""


SHOP_CARD_1_HTML_TEMPLATE_OG = """
<div style="padding-left:15px;font-family: 'Roboto', sans-serif; font-weight:600; color:grey;">{}</div>
<div class="card" style="width:90%; height:100%; margin:5px 20px 1px 1px; padding:1px 5px 35px 15px; position:relative; border-radius:5px;
border=5px solid; box-shadow:0 0 1px 1px #eee; 
background: radial-gradient(rgba(255,255,255,0.2)8%,transparent 8%); background-position:0%, 0%; background-size:5vmin 5vmin;
font-weight:300; border-left:10px solid #484848; color:white; font-family: 'Roboto', sans-serif; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15);">
<h2 style="color:#eba538; font-weight:500; margin-bottom:10px; font-size:1.3rem;">{}</h2>
<div style="color:#efefef; font-weight:300; margin-bottom:5px; margin-left:-15px"><span style="background-color:#484848; color:#ffffff; border-radius:2px; padding:2px 5px;">details</span></div>
<div style="color:#efefef; font-weight:300; margin-bottom:25px;">{}</div>
<div style="border-top: 1px dashed #7e7e7e; padding-bottom:10px"></div>
<div style="color:#efefef; font-weight:300; margin-bottom:15px;">Created {} Days Ago <span style="color:#949494;">[{}]</span></div>
{}
<span style="width:95%; height:100%; position:absolute; text-align:right; font-size:0.9rem; color:#949494; margin-left:-10px;">{}</span>
<span style="width:95%; height:100%; position:absolute; text-align:left; color:#949494;">{}</span>
</div>
"""

SHOP_CARD_4_HTML_TEMPLATE_BACKUP = """
<div style="display:flex; justify-content:center; align-items:center;">
<div style="width:90%; height:100%; padding:50px 0px 0px 0px; position:relative; border-radius:40px; 
box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
background: url('https://thehardgainerbible.com/wp-content/uploads/2022/07/abstract-blur-defocused-supermarket.jpg');
background-size: cover; background-color:rgba(42,46,63,0.95); background-blend-mode: overlay;>
<div style="width:100%; height:100%; position:relative;">
<div style="font-size:1.7rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:20px; font-weight:500;">Shopping</div>
<div style="font-size:1.7rem; font-family: 'Roboto', sans-serif; color:#efefef; padding-left:20px; font-weight:500;">List</div>
<div style="height:100%; padding:0px 10px 90px 0px;"><img src ="{}" 
style="display: flex; flex-direction: column; justify-content: space-between; position: relative; filter: drop-shadow(5px 5px 10px #0F1620);
min-height: 100px; max-height:120px; float:right">
</div>
<div style="width:auto; height:100%; positiion:relative; background-color:white; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15); 
padding: 20px 0px 50px 15px; border-radius:0px 0px 40px 40px; font-family: 'Roboto', sans-serif;">
Some Text
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}</h2>
</div>
</div>
</div>
</div>
"""





if __name__ == "__main__":
    run()