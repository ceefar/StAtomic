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
# for dataframes
import pandas as pd


########### IMPORTANT #############
# SO THIS KINDA FUCKIN BREAKS ON SUNDAYS
# FIX WILL BE EASY ENOUGH IG
# IN REFACTOR (which 100 wanna do asap of just this too)
# HAVE GLOBAL OVERRIDE FOR DAY, WEEKNUM, DAYNUMB, ETC SO TESTING IS MUCH MUCH EASIER
# AND PRE FILL A LARGER AMOUNT OF INFO!




# ---- temp globals ----
# for testing/setup

user_name = "Ceefar"
db_username = user_name.lower()

# ---- layout ----
# either use more or remove pls, as barely using rn

topper = st.container()
intro = st.container()


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


# ---- new page functions ----

def print_mood_img(mood):
    """ returns img path based on given mood parameter """
    mood_dict = {'worst':'imgs/mood/angry.png','awful':'imgs/mood/angry-face.png','bad':'imgs/mood/crying.png','below average':'imgs/mood/sad.png',
                'average':'imgs/mood/neutral.png','above average':'imgs/mood/smile.png','good':'imgs/mood/smile.png','great':'imgs/mood/lol.png',
                'amazing':'imgs/mood/lol.png'}
    try:            
        return(mood_dict[mood])
    except KeyError:
        return("imgs/icons/blank.png")

def highlight_current_day(dayname:str) -> str:
    """ returns 'TODAY' if given parameter is the current day of the week, else returns the name of the day of the week e.g. 'Monday' """
    cur_dayname = db.get_current_dayname()
    if cur_dayname == dayname:
        return("imgs/icons/event_available_fill1.png") # enable_fill1
    else:
        return("imgs/icons/blank.png")

def convert_mood_int_to_str(mood_int:int):
    """ write me """
    mood_dict = {1:'worst', 2:'awful', 3:'bad', 4:'below average', 5:'average', 6:'above average', 7:'good', 8:'great', 9:'amazing'}
    if mood_int in mood_dict:
        return(mood_dict[mood_int])
    else:
        return("")

def get_mood_value_from_db_basics(given_day:str):
    """ write me """
    # ideally the result from the db would also be a dict 
    # then you could just pull the relevant values but this is fine tbf since is still only 1 db query
    day_numb_dict = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6,}
    week_mood_basic = db.get_this_weeks_logged_mood_basics(db_username)
    the_day = day_numb_dict[given_day]
    for daymood in week_mood_basic:
        day, mood = daymood
        if the_day == day:
            mood = int(f"{mood:.0f}")
            return(mood)
    return(None)

def get_mood_delta(dayname, week_mood):
    """ write me """
    m_mood, t_mood, w_mood, th_mood, f_mood, sa_mood, su_mood = week_mood
    # get previous sunday mood int
    last_su_mood = db.get_previous_sunday_mood_int(db_username)
    mood_calc_dict = {"Monday":(m_mood - last_su_mood if last_su_mood and m_mood else None), "Tuesday":(t_mood-m_mood if t_mood and m_mood else None),
                    "Wednesday":(w_mood-t_mood if w_mood and t_mood else None), "Thursday":(th_mood-w_mood if th_mood and w_mood else None), 
                    "Friday":(f_mood-th_mood if f_mood and th_mood else None), "Saturday":(sa_mood-f_mood if sa_mood and f_mood else None), 
                    "Sunday":(su_mood-sa_mood if su_mood and sa_mood else None)}
    mood_delta = mood_calc_dict[dayname]
    return(mood_delta)


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

        st.write("##### Mood Monitor")

    # ---- SECTION ----

    # todo task create intro and setup
    with intro:

        st.write(f"### Improve Your Wellness ")

        # LIKE THIS IS GUNA NEED ITS OWN DB TABLE RIGHT BUT KEEP HELLA SIMPLE TO START OBVS!
        
        col1A, _ = st.columns([4,1])
        col1A.write("Improve your wellness and lead a happier life by monitoring your mood by lorem ipsum dolor sit amet consectetur adipisicing elit.\
                    Maxime mollitia, molestiae quas vel sint commodi repudiandae consequuntur \
                    voluptatum laborum ")
        st.write("---")      


    # ---- SECTION ----

    with st.container():
        st.markdown("##### Weekly Mood Snapshot")
        col1B, _ = st.columns([4,1])
        col1B.write("Lorem ipsum week starts on sunday (for now), 1 is the lowest mood score and 9 is the best sit amet dolor etc also be sure to note how the delta works here so it's clear")
        current_date = db.get_current_date()
        current_dayname = db.get_current_dayname()
        st.write("##")
        st.markdown(f"### Your Mood This Week")
        st.markdown(f"##### Current Day is {current_dayname} [{current_date}]")
        st.write("##")

        # ADD THE DELTA HERE TOO 100
        monday_mood = get_mood_value_from_db_basics("Monday")
        tuesday_mood = get_mood_value_from_db_basics("Tuesday")
        wednesday_mood = get_mood_value_from_db_basics("Wednesday")
        thursday_mood = get_mood_value_from_db_basics("Thursday")
        friday_mood = get_mood_value_from_db_basics("Friday")
        saturday_mood = get_mood_value_from_db_basics("Saturday")
        sunday_mood = get_mood_value_from_db_basics("Sunday")

        week_mood = (monday_mood, tuesday_mood, wednesday_mood, thursday_mood, friday_mood, saturday_mood, sunday_mood)

        # could have imgs over the top, just empty but same size, except current day which has a down arrow! #FIXME
        # ALSO THIS SHOULD JUST BE 1 FUNCTION AND CAN JUST FEED IT THE DAYNAME (AND COL? - see if works anyway!) #TODO
        # ALSO TEMPTED TO HAVE DATE AS SHORT STR (15/08/22) OVER THE EMOJIS/BLANK FOR THE SAKE OF FORMATTING BTW
        moncol, tuecol, wedscol, thurcol, fricol, satcol, suncol = st.columns(7)
        # MONDAY
        try:
            moncol.image(print_mood_img(convert_mood_int_to_str(monday_mood)), width=40) 
        except FileNotFoundError:
            moncol.write("")
        moncol.metric(label="Monday", value=monday_mood, delta=get_mood_delta("Monday", week_mood), delta_color="normal")
        moncol.image(highlight_current_day("Monday"), width=30)
        # TUESDAY
        try:
            tuecol.image(print_mood_img(convert_mood_int_to_str(tuesday_mood)), width=40) 
        except FileNotFoundError:
            tuecol.write("")
        tuecol.metric(label="Tuesday", value=tuesday_mood, delta=get_mood_delta("Tuesday", week_mood), delta_color="normal") # tuecol.metric(label=highlight_current_day("Tuesday"), value=tuesday_mood, delta=1, delta_color="normal")   
        tuecol.image(highlight_current_day("Tuesday"), width=30)    
        # WEDNESDAY 
        try:
            wedscol.image(print_mood_img(convert_mood_int_to_str(wednesday_mood)), width=40) 
        except FileNotFoundError:
            wedscol.write("")
        wedscol.metric(label="Wednesday", value=wednesday_mood, delta=get_mood_delta("Wednesday", week_mood), delta_color="normal")
        wedscol.image(highlight_current_day("Wednesday"), width=30) 
        # THURSDAY
        try:
            thurcol.image(print_mood_img(convert_mood_int_to_str(thursday_mood)), width=40)
        except FileNotFoundError:
            thurcol.write("") 
        thurcol.metric(label="Thursday", value=thursday_mood, delta=get_mood_delta("Thursday", week_mood), delta_color="normal")
        thurcol.image(highlight_current_day("Thursday"), width=30)
        # FRIDAY
        try:
            fricol.image(print_mood_img(convert_mood_int_to_str(friday_mood)), width=40) 
        except FileNotFoundError:
            fricol.write("")
        fricol.metric(label="Friday", value=friday_mood, delta=get_mood_delta("Friday", week_mood), delta_color="normal")
        fricol.image(highlight_current_day("Friday"), width=30)
        # SATURDAY
        try:
            satcol.image(print_mood_img(convert_mood_int_to_str(saturday_mood)), width=40)  
        except FileNotFoundError:
            satcol.write("")
        satcol.metric(label="Saturday", value=saturday_mood, delta=get_mood_delta("Saturday", week_mood), delta_color="normal")
        satcol.image(highlight_current_day("Saturday"), width=30)
        # SUNDAY
        try:
            suncol.image(print_mood_img(convert_mood_int_to_str(sunday_mood)), width=40) 
        except FileNotFoundError:
            suncol.write("") 
        suncol.metric(label="Sunday", value=sunday_mood, delta=get_mood_delta("Sunday", week_mood), delta_color="normal")
        suncol.image(highlight_current_day("Sunday"), width=30)

        weeknumb = db.get_current_week_number()
        st.write(f"Week {weeknumb} of 52")

        # ACTUALLY 100 HAVE AN EXPANDER OF NOTES HERE TOO BTW! #FIXME

        # COULD HAVE A LIL BIT OF INFO ABOUT THE WEEK HERE TOO LIKE THE AVG AND AVG COMPARED TO PREVIOUS WEEK
        # AND MAYBE SOME TIPS LIKE JUST SUPER GENERAL IF BAD WEEK OR GOOD WEEK
        # BUT IN FUTURE INSIGHTS WOULD BE BASED ON THINGS YOU HAVE DONE IN GOOD WEEKS UR MISSING OR TO CONTINUE OR WHATEVER LIKE INSIGHTS AF BOSH! #TODO

        st.write("---")

    # ---- SECTION ----

    with st.container():  

        st.markdown("##### Mood Tracking")

        moodinputcol, _, moodimgcol = st.columns([5,1,2])
        with moodinputcol:
            user_mood = st.select_slider('How Is Your Mood Today?', value='average', options=['worst','awful','bad','below average','average','above average','good','great','amazing'])
            mood_notes = st.text_area('Mood Notes (optional)')
        with moodimgcol:
            st.write("##")
            st.write("I'm feeling...", user_mood)
            st.image(print_mood_img(user_mood),width=80)
        
        # DEACTIVATE THIS BUTTON IF HAS AN ENTRY FOR THE DAY AND HAVE A TOGGLE THAT REACTIVATES IT (or whatever)
        if st.button("Log Today's Mood"):
            if mood_notes:
                db.log_user_mood_for_day(db_username, user_mood, mood_notes)
            else:
                db.log_user_mood_for_day(db_username, user_mood)
            st.success(f'Mood Added for {current_dayname} {current_date}')
            # FIXME
            # EITHER HAVE THIS HAPPEN AFTER X TIME OR HAVE SUMNT THAT FORCES IT TO HAPPEN IDK BUT THE FIELDS SHOULD WIPE AND SHIT SO FIGURE IT OUT PLS!
            # DONT HAVE TO HAVE RERUN BTW 
            # LIKE ABOVE COULD EVEN BE A BUTTON, UPDATE WEEK CHARTS! (legit could just be a faux button too, this might be the best idea! test anyway!!)
            st.experimental_rerun()
            
        st.write("---") 



    # ---- SECTION ----

    with st.container():
        st.markdown("##### Mood Timeline")
        st.write("##")

        data = (5, None, 4, 3, None, None, None),(5, None, 4, 3, None, None, None)

        mood_week_data = pd.DataFrame(data, columns=('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'), index=["Week 22","Week 23"])

        # get list of week numbers with logged data for the user from 2022
        weeknumbs = db.get_all_week_numbs_for_user(db_username)
        # create a new list of week numbers formatted with the word week at the start 
        formattedweeknumbs = []
        dont_print = [formattedweeknumbs.append(f"Week {weekn}") for weekn in weeknumbs] 
        #print(f"{formattedweeknumbs = }")

        # get all mood data for each week, always 7 long and ordered, returns none if no data for a given day else returns its mood as int
        all_weeks_mood_list = []
        for weekint in weeknumbs:
            week_tuple = db.get_mood_data_for_given_week_numb(db_username, weekint)
            all_weeks_mood_list.append(week_tuple)
        #print(f"{all_weeks_mood_list = }")

        # convert to tuple of tuples for dataframe
        all_weeks_mood_tuple = tuple(all_weeks_mood_list)
        #print(f"{all_weeks_mood_tuple = }")

        data = all_weeks_mood_tuple
        mood_week_data = pd.DataFrame(data, columns=('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'), index=formattedweeknumbs)
        

        def style_df(val):
            """ write me """
            if val != None:
                if val == 9:
                    return("background-color: #56ce27")
                elif val == 8:
                    return("background-color: #7ec000")
                elif val == 7:
                    return("background-color: #9ab100")
                elif val == 6:
                    return("background-color: #b1a000")
                elif val == 5:
                    return("background-color: #c48e00")
                elif val == 4:
                    return("background-color: #d47a00")
                elif val == 3:
                    return("background-color: #df6400")                                                                                                                        
                elif val == 2:
                    return("background-color: #e64b0f")
                elif val == 1:
                    return("background-color: #e92d2d")
                elif val == 0:
                    return("background-color: #efefef") # bfbfbf efefef 999999
            else:                                       
                return("background-color: #efefef")

        st.write("Some general info and clarify that 0 means no data")

        st.dataframe(mood_week_data.style.applymap(style_df))
        #st.dataframe(mood_week_data.head(2).style.highlight_null(null_color='#efefef')) 

        # website is awesome and everything https://colordesigner.io/gradient-generator so still use to some degree but please god more vibrant colours
        # ability to print this as cool img with artist.py would be awesome! #FIXME
        #   - like u can choose which month and then THERE you could have even more info) #FIXME
        #   - if not must do something with artist.py even if basic af #FIXME
        # AVG FOR WEEK WOULD BE NICE HERE TOO BTW DUH! #FIXME
        # visualisation of weeks left in year would be nice too, could go in below bit tbf #FIXME
        # for real need a way to see previous weeks too! (date selector ig? or week number toggle or sumnt idk) #FIXME
        # 100% need if saving again and exist it overwrites not creates duplicates! #FIXME
        # 100$ need notes somewhere ffs! #FIXME

        # index, userid, day, mood entry (as enum?), notes
        # can metrics be derived entirely from the table, probably so just meh do like that for now
        # things like missed entries and done entries for week month
        # avg mood
        # tasks completed vs mood
        # visualisation of mood over time

        st.write("---")


    # ---- SECTION ----

    MOOD_NOTES_TEMPLATE = """
    <div style="padding-left:15px;font-family: 'Roboto', sans-serif; font-weight:600; color:grey;">{}</div>
    <div style="background-color:#151515; width:90%; height:100%; position:relative; border-radius:5px;
    border=5px solid; box-shadow:0 0 1px 1px #eee;">
    <div style="margin:5px 2px 1px 1px; padding:1px 25px 25px 15px; background: radial-gradient(rgba(255,255,255,0.2)8%,transparent 8%); background-position:0%, 0%; background-size:5vmin 5vmin;
    font-weight:300; border-radius:5px; border-left:10px solid #484848; color:white; font-family: 'Roboto', sans-serif; box-shadow: 5px 5px 5px 5px rgba(0,0,0,0.15);">
    <div style="color:#efefef; font-weight:300; margin-top:20px; margin-bottom:5px; margin-left:-15px"><span style="background-color:#484848; color:#ffffff; border-radius:2px; padding:2px 5px;">notes</span></div>
    <h2 style="color:#efefef; font-weight:300; margin-bottom:10px; font-size:1.3rem;">{}</h2>
    <div style="color:#eba538; font-weight:500; font-size:1.5rem; margin-bottom:5px;">Mood : {}</div>
    </div>
    </div>
    """

    with st.container():
        st.markdown("##### Your Mood Journal")
        col1C, _ = st.columns([4,1])
        col1C.write("Lorem ipsum sit amet dolor etc")
        #st.write("##")

        user_mood_notes = db.get_mood_notes(db_username)
        if user_mood_notes:
            for note in user_mood_notes:
                # amount of lines dictates the needed height btw (easy calc based on amount of chars * a multiplier) #FIXME
                if len(note[0]) < 65:
                    stc.html(MOOD_NOTES_TEMPLATE.format(str(note[3]),note[0],note[2].title()), height=250)
                else:
                    stc.html(MOOD_NOTES_TEMPLATE.format(str(note[3]),note[0],note[2].title()), height=300)











if __name__ == "__main__":
    run()




# FIXME !
# TODO !
# - sunday shit is not working right either on week display bit ffs! (use current sunday now no backlog duh!) (also here try to have it in sun start order too)
# - start dataframe from sunday to saturday so doesnt look dumb
# - wipe notes on add mood
# - improve df colours/general format



        

        # THEN JOURNAL AND DC! 
        #   - note pomdoro too but nah?? - note also timers dont need to be every sec when its not fitness so its easier ig
        #   - basically just never show tbh or you risk fucking the user, maybe only send pomdoro via discord ooo i LOVE that
        # THEN CV, BIO, & TECH PREP?
        # THEN THIS PAGE ONLY BUT REFACTOR WITH USER AND LIVE DB AND MAYBE CLASSES TOO ooooo

