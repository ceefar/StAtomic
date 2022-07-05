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
# for pushing to dc via webhook 
import discord_webhook as dc



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
            st.markdown("#### Your Shopping Lists")
            st.write("**To view the items on your shopping list use the dropdown selector below**")
            todo_list_names = create_todo_lists_list()
            shopping_tasks = db.get_shopping_list_tag_tasks_only(db_username)

            # CONSIDER WHAT HAPPENS WHEN THERE ARE NONE (no shop tags) - just try except should be fine tbf? but still need to do! #FIXME
            shop_tasks_dict_list = []
            for task in shopping_tasks:
                shoptask = db.view_tasks_basic(db_username, task, "shop")
                shop_tasks_dict_list.append(shoptask)

            #print(f"{shop_tasks_dict_list = }")

            shop_task_titles = []
            dont_print = [shop_task_titles.append(task[0]["title"]) for task in shop_tasks_dict_list]
            # print(f"{shop_task_titles = }")
            
            # NEED CASE FOR IF NONE BTW!
            amount_of_shop_tasks = len(shop_tasks_dict_list)
            if (amount_of_shop_tasks % 2) != 0:
                cards_one = amount_of_shop_tasks // 2
                cards_two = cards_one + 1

            shop_task_titles.insert(0, "All Shopping Lists")

            assigned_todo_list = st.selectbox("Choose An Existing Shopping List", shop_task_titles)

            st.write("##")


        # ---- NEW CARD SECTION ----
        

        # IF DROPDOWN IS ALL
        if assigned_todo_list == "All Shopping Lists":
          with st.container():
            cardcol1, cardcol2 = st.columns(2)
            with cardcol1:
                temptitlestwo = shop_tasks_dict_list[cards_two:]
                for task in temptitlestwo:
                    if "Toiletries" in task[0]["title"]:
                        img = "https://cdn-icons-png.flaticon.com/512/3419/3419660.png"
                        #shop tags, created date, detail... 
                        task_detail = task[0]["detail"][:40]
                        stc.html(SHOP_CARD_4_HTML_TEMPLATE_TOIL.format(task[0]["title"], img, task[0]["createdDate"], task_detail), height=450)
                    else:
                        img = basket_images[random.randint(0, 2)]
                        stc.html(SHOP_CARD_4_HTML_TEMPLATE.format(task[0]["title"], img, task[0]["createdDate"], task_detail), height=450)
            with cardcol2:
                temptitlesone = shop_tasks_dict_list[:cards_one+1]
                for task in temptitlesone:
                    task_detail = task[0]["detail"][:40]
                    stc.html(SHOP_CARD_4_HTML_TEMPLATE.format(task[0]["title"], basket_images[random.randint(0, 2)], task[0]["createdDate"], task_detail), height=450)
        else:
          for task in shop_tasks_dict_list:
            if task[0]["title"] == assigned_todo_list:
              # defined for easier insert and easier tracking size(len)
              listdetail = str(task[0]["detail"])
              listtitle = task[0]["title"]
              # for the amount of items in the list, displayed at the bottom of the list in the html
              list_items_counter = len(listdetail.split(","))
              # to get the checkbox at the start it has to be done this long way round          
              newlist = listdetail.split(",")
              # after splitting at the comma, create new list that we'll append formatted strings to
              checkboxlist = []
              for item in newlist:
                # create a new formatted string of the item stripped and capitalised with a breakline at the end and checkbox at the start
                checkitem = f"{CHECKBOX_HTML_CODE}&nbsp&nbsp;{item.strip().capitalize()} <br>"
                checkboxlist.append(checkitem)
              # the above list will be full of newline (\n) characters due to the checkbox code having endl's
              finalcheckboxlist = []
              # so replace any \n characters for each item and append them to a final list, is fine since we use breakline to separate each list item
              for item in checkboxlist:
                checkboxitem = item.replace("\n","")
                finalcheckboxlist.append(checkboxitem)
              # finally join that all back into one string so it can be inserted into the html in one go
              checkboxliststring = "".join(str(item) for item in finalcheckboxlist)

              # list_style_details = listdetail.replace(",", f"{CHECKBOX_HTML_CODE} <br>")
             
              # OWN FUNCTION PLS!! #FIXME
              paper_base_height = 720 # idk if this is accurate btw
              paper_height_incremenet = 40 # for every 2 over 11 add x and define x so is easy to change 
              extra_lines = list_items_counter - 11
              extra_height = extra_lines * paper_height_incremenet
              paper_height = paper_base_height + extra_height
              paper_height = 720 if paper_height < 720 else paper_height

              dc_button = st.button(label="Send To Discord")
              if dc_button:
                fordc = listdetail.split(",")
                fordcstripped = []
                dont_print_three = [fordcstripped.append(f"• {item.strip().capitalize()}") for item in fordc]
                fordcstripped.insert(0,f"**{listtitle}**\n- - - - -")
                fordcstripped.append("- - - - -")
                fordc_final = "\n".join(fordcstripped)
                # TODO : ffs need to strip again due to minor spacing issues, ideally just 1 list comprehension strip creates 2 vars then do whatever afterwards
                fordcstrip = []
                dont_print_five = [fordcstrip.append(item.strip().capitalize()) for item in fordc]
                shoplistimg = arty.draw_dynamic_shopping_list(f"{db_username}_{listtitle}", fordcstrip, listtitle)
                dc.push_msg_to_dc(fordc_final)
                dc.push_image_to_dc(shoplistimg, f"Here's your shopping list {db_username}")

              arty_button = st.button(label="Get Downloadable Image")
              if arty_button:
                forarty = listdetail.split(",")
                fordcstripper = []
                dont_print_four = [fordcstripper.append(item.strip().capitalize()) for item in forarty]
                shoplistimg = arty.draw_dynamic_shopping_list(f"{db_username}_{listtitle}", fordcstripper, listtitle)
                st.image(shoplistimg)

              stc.html(TEST_PAPER_HTML_TEMPLATE.format(listtitle, checkboxliststring, list_items_counter), height=paper_height) 
            
    else:
        with st.container():  

            st.markdown("#### New Shopping List")
            st.write("**Use commas to separate items on your shopping list for a truly integrated experience**")
            todo_faux_title = st.text_input("Enter A List Title", value="A simple example", key="td_fauxtitle")
            todo_faux_detail = st.text_area("Enter Items", value="A more thorough example", key="td_fauxdetail")
            st.write("---")

            # THIS HEIGHT DYNAMIC BASED ON AMOUNT OF /N AND CHARS! #FIXME
            stc.html(TEST_PAPER_HTML_TEMPLATE.format("New List","Click to write your message bro"), height=620)
            
    

        # skip to end/quick add button?
    
       
    st.write("---")

    with st.sidebar:
        stc.html("""<iframe src="https://discord.com/widget?id=972790226504282132&theme=dark" width="280" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>""", height=550)
    

    # FIXME 
    # BIG CHANGE MUST N0TE GENERALLY AND FOR REFACTORS! 
    # LEGIT ITS NOT ATOMIC ITS AN ADHD APP NOW LOL (tho not just adhd tbf but best for it so think about shit exclusively for you - yay!)


    # BUG 
    # ALSO HAVE A SMALL WIDGET YANNO! (or atleast like an anchor thats in icon that hops u to the bottom of the page idk)

    # TWO PAPER THINGS QUICKLY FOR HOME PAGE AND ANYWHERE ELSE TBH LOOK SICK AF
    #   - have post it at the top of lots of pages (or which every tbh, with a current reminder!)
    #   - tho for shop list another style could be better tbf but meh
            # stc.html(POST_IT_HTML_TEMPLATE.format(), height=500)
            # stc.html(PAPER_TEMPLATE_NEW.format(), height=500)

    # IMPROVE EXISTING DC WEBHOOK IMPLEMENTATION A TAD FFS!
    # NEW PAGE IDEA (sleep tracker (wake and sleep time) with caffeine (and meds) entry)
    # NEW DC IDEA, SEE BELOW!
    # AFTER THIS ONLY WEB DB IMPLEMENTATION - NEW REPO?
    #   - EITHER WAY FIRST TEST A SUUUPER BASIC VERSION TO BE SURE WORKS (with artist!)


    # TODO FOR DC
    # MORE SEND TO DISCORD THINGS, ALSO THINK ABOUT TIMED SHIT FOR THAT TOO LEGIT!
    # ACTUALLY TO GET BOT TO WORK DO THIS
    #   - when new user lands they idk confirm to the bot they staying or sumnt idk
    #   - once confirmed you get your own (private?) channel, just you and the bot
    #   - this is where you get your notifications and in turn send things to be stored in the db OOOOOOOOO!
    # ALSO THEN REFACTOR LOADS OF SHIT ALREADY DONE BUT FROM ST PAGES TO THEIR OWN RELEVANT - JUST PY - FILE
    # AND USE THESE TO MAKE A BOT DO THE EXACT SAME COMMANDS AS ST (like getting lists n shit! ooooo)


    # TODO 
    # OPTION TO MAKE (& SAVE!) EDITS, ADD NEW ACTUALLY WORKING
    # ENTER HOW MUCH IT COST, LOCATION, ETC? AND SAVE THAT STUFF TOO
    # SAVING ANY EDITS AS CHILDREN AND DISPLAY BACK EDIT VERSIONS (CHILD VERSIONS) OF LISTS IF THEY HAVE THEM THROUGH A DD
    # LEGIT ANY API TO LIKE PRICE UP THE BASKET OR WHATEVER LEGIT ANYTHING JUST TO SAY IMPLEMENTED ONE
    

    # OTHER PAGES (OR THIS PAGE TBF) FULL WEB/DB REFACTOR TEST
    #   - LEGIT ANY PAGE FOR REFACTOR JUST IN ALL SERIOUSNESS GET SUMNT LOOKING TO FINAL AND THEN GET IT A LIVE DB
    #   - SLEEP TRACKER MIGHT BE BEST SINCE STARTING A NEW IS ALWAYS EASIEST IG
    # SLEEP TRACKER VS CAFFEINE / MEDS TING! <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # &/OR TECHNICAL INTERVIEW PREP



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
{}
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}...</h2>
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
{}
<h2 style="color:#151515; font-weight:500; margin-bottom:10px; font-size:1.3rem; font-family: 'Roboto', sans-serif;">{}...</h2>
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


CHECKBOX_HTML_CODE = """
<container>
<input type="checkbox">
<span class="checkmark"></span>
</container>
"""


TEST_PAPER_HTML_TEMPLATE = """
<style>
body {{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px 30px;
  margin-top:-25px;
  margin-left:-30px;
}}
.notepad {{
  width: 80%;
  max-width: 600px;
  box-shadow: 10px 10px 10px 5px rgba(0,0,0,0.10);
  border-radius: 10px 10px 10px 10px;
  border: 1px solid rgba(0,0,0,0.20);
  overflow: hidden;
}}
.top {{
  width: 100%;
  height: 50px;
  background: #333;
  border-radius: 5px 5px 0 0;
}}
.paper {{
  width: 90%;
  height: 100%;
  min-height: 60vh;
  padding: 35px 50px 50px 20px;
  background: repeating-linear-gradient(#F1EDE9, #F1EDE9 31px, #94ACD4 31px, #94ACD4 32px);
  font-family: 'Shadows Into Light', cursive;
  line-height: 32px;
  outline: 0;
  font-size: 22px;
}}
</style>
<div class="notepad">
  <div class="top"></div>
  <div class="paper" contenteditable="true">
    <b>{}</b><br>
    {}<br>{} total list items
  </div>
</div>
"""


PAPER_TEMPLATE_NEW = """"
<style>
:root {{
  --pink: #ecb2ba;
  --pink-dark: #c6939a;
  --tape-gray: #dbd8be;
  --tape-edge-gray: #b7b49d;
  --transparent: rgba(255, 255, 255, 0);
}}

body {{
  background: #ebf4e9;
  padding: 20px;
  display: flex;
  justify-content: center;
  flex-direction: column;
}}

.pink {{
  --paper-color: var(--pink);
  --paper-dark: var(--pink-dark);
  --shadow-size: 1px;
  --transparent: rgba(236, 178, 186, 0);
}}

.blue {{
  --paper-color: #d5e0f9;
  --paper-dark: #c2d0ea;
  --shadow-size: 3px;
  --transparent: rgba(213, 224, 249, 0);
}}

.paper {{
  position: relative;
  background: linear-gradient(
      to bottom right,
      var(--paper-dark),
      20%,
      var(--transparent)
    ),
    var(--paper-color);
  min-width: 250px;
  min-height: 130px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Caveat", cursive;
  font-size: 2rem;
  box-shadow: var(--shadow-size) var(--shadow-size) 2px var(--paper-dark);
  margin: auto;
  margin-top: 50px;
}}

.paper::after {{
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(
      var(--transparent),
      50%,
      var(--paper-dark),
      51%,
      var(--transparent)
    ),
    linear-gradient(
      to right,
      var(--transparent),
      50%,
      var(--paper-dark),
      51%,
      var(--transparent)
    );
}}

.tape-section {{
  position: absolute;
  width: 100%;
}}

.top-tape {{
  position: absolute;
  height: 4vmin;
  top: -5px;
  width: 110%;
  background-color: var(--tape-gray);
  border-right: 1px dotted var(--tape-edge-gray);
  border-left: 1px dotted var(--tape-edge-gray);
  opacity: 0.5;
}}

.tape-section:first-of-type {{
  top: 0;
}}

.tape-section:last-of-type {{
  bottom: 0;
}}

.tape-section::before,
.tape-section::after {{
  content: "";
  width: 10vmin;
  height: 4vmin;
  position: absolute;
  background-color: var(--tape-gray);
  opacity: 0.5;
  border-right: 1px dotted var(--tape-edge-gray);
  border-left: 1px dotted var(--tape-edge-gray);
}}

.tape-section:last-of-type::after {{
  transform: rotate(-45deg);
  right: -4vmin;
  top: -3vmin;
}}

.tape-section:first-of-type::before {{
  transform: rotate(-45deg);
  left: -4vmin;
}}

.tape-section:first-of-type::after {{
  transform: rotate(45deg);
  right: -4vmin;
  top: 0;
}}

.tape-section:last-of-type::before {{
  transform: rotate(45deg);
  left: -4vmin;
  bottom: 0;
}}
</style>


<body>
  <div class="paper pink">
    <div class="tape-section"></div>
    <p>drink more water</p>
    <div class="tape-section"></div>
  </div>
  <div class="paper blue">
    <div class="top-tape"></div>
    <p>code more pens</p>
  </div>
</body>
"""



POST_IT_HTML_TEMPLATE="""
<style>

:root {{
  --papery-shadow: #c9bf8d;
}}

body {{
  display: flex;
  justify-content: center;
  padding: 10vmin;
  background-color: #c3cde8;
  font-family: "Caveat", cursive;
  font-size: 2rem;
}}

.papery {{
  --papery-dark: #e5c93d;
  --papery-color: #ffed87;

  position: relative;
  display: flex;
  justify-content: center;
  min-width: 325px;
  min-height: 175px;
  background: linear-gradient(
    135deg,
    var(--papery-dark),
    30%,
    var(--papery-color)
  );
  box-shadow: 3px 3px 2px var(--papery-shadow);
  transform: rotate(10deg);
  transform-origin: top left;
}}

.papery p {{
  margin: auto;
}}

.pin {{
  --pin-color: #d02627;
  --pin-dark: #9e0608;
  --pin-light: #fc7e7d;

  position: absolute;
  left: 20px;
  width: 60px;
  height: 50px;
}}

.shadowy {{
  position: absolute;
  top: 18px;
  left: -8px;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: radial-gradient(var(--paper-shadow), 20%, rgba(201, 191, 141, 0));
}}

.metal {{
  position: absolute;
  width: 5px;
  height: 20px;
  background: linear-gradient(to right, #808080, 40%, #eae8e8, 50%, #808080);
  border-radius: 0 0 15px 15px
  transform: rotate(50deg);
  transform-origin: bottom left;
  top: 15px;
  border-bottom: 1px solid #808080;
}}

.bottom-circle {{
  position: absolute;
  right: 15px;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background-color: var(--pin-color);
  background: radial-gradient(
    circle at bottom right,
    var(--pin-light),
    25%,
    var(--pin-dark),
    90%,
    var(--pin-color)
  );
}}


.bottom-circle::before {{
  content: "";
  position: absolute;
  top: 0;
  left: -2px;
  width: 20px;
  height: 30px;
  transform: rotate(55deg);
  border-radius: 0 0 20px 20px;
  background: linear-gradient(
    to right,
    var(--pin-dark),
    30%,
    var(--pin-color),
    90%,
    var(--pin-light)
  );
}}

.bottom-circle::after {{
  content: "";
  position: absolute;
  right: -10px;
  top: -5px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: radial-gradient(
    circle at right,
    var(--pin-light),
    30%,
    var(--pin-color),
    var(--pin-dark) 80%
  );
}}

</style>

<div class="papery">
  <div class="pin">
    <div class="shadowy"></div>
    <div class="metal"></div>
    <div class="bottom-circle"></div>
  </div>
  <p>zoom call @ 4pm</p>
</div>

"""


if __name__ == "__main__":
    run()