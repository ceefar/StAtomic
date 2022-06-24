# imports 
# for web app and test components
import streamlit as st
import streamlit.components.v1 as stc
# for db access
import db_integration as atomdb
# for datatime objects
from datetime import datetime
# for number to word (yh im a lay-zee-boi, deal with it)
import n2w



def get_db_data_temp() -> tuple:
    # obvs len considerations duh, paginate with offset based on amount of valid entries you want to display
    base_data = atomdb.get_base_habit_data_v0()
    return(base_data)


def format_dt(dt) -> str:
    """ use paramters to set formatting type """
    formatted_datetime = dt.strftime("%m/%d/%Y, %H:%M:%S")
    return(formatted_datetime)


HABIT_HTML_TEMPLATE = """
<div style="padding-left:15px;font-family: 'Roboto', sans-serif; font-weight:600; color:grey;">{}.</div>
<div style="width:95%; height:100%; margin:5px 20px 1px 1px; padding:1px 5px 35px 15px; position:relative; border-radius:5px;
border=5px solid; box-shadow:0 0 1px 1px #eee; background-color:#31333F; font-weight:300;
border-left:10px solid #484848; color:white; font-family: 'Roboto', sans-serif;">
<h2 style="color:#eba538; font-weight:300;">{}</h2>
<span style="width:95%; height:100%; position:absolute; text-align:right;">{}{}</span>
<span style="width:95%; height:100%; position:absolute; text-align:left;">{}</span>
</div>
"""

#003366 <- for dark mode | #d4d4d4 <- for light mode
HABIT_DETAILS_TEMPLATE = """
<div style="width:100%; height:50%; margin:-20px 1px 1px 1px;color:#003366; padding:0px 0px 0px 20px;
font-family: 'Roboto', sans-serif;">
<h4 style="font-weight:400; width:90%; position:absolute; text-align:right;">{}</h4>
<div style="width:90%; position:absolute; margin-top:40px;"><hr style="border-top:1px solid #ddd;"></div>
</div>
"""


MATERIAL_ICON_POSITIVE = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:#AAFF00'>add_circle</i>"
MATERIAL_ICON_NEUTRAL = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:yellow'>do_not_disturb_on</i>"
MATERIAL_ICON_NEGATIVE = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:red'>disabled_by_default</i>"
MATERIAL_ICON_TASK_ALT = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:#AAFF00'>task_alt</i>"
MATERIAL_ICON_ADD_TASK = "<link rel='stylesheet' href='https://fonts.googleapis.com/icon?family=Material+Icons'><i class='material-icons' style='padding-left:10px; color:#AAFF00'>add_task</i>"


def run():
    
    base_data = get_db_data_temp()
    for task in base_data:
        id, title, align, created, updated = task 
        #st.write(str(id))
        #st.write(title)
        #st.write(f"{align}")
        id = str(id)
        create_dt = (format_dt(created))      
        update_dt = (format_dt(updated))   
        #(1, 'work on personal project - st.atomic', 'positive', datetime.datetime(2022, 6, 20, 6, 10, 7), datetime.datetime(2022, 6, 20, 6, 16))
        
        stc.html(HABIT_HTML_TEMPLATE.format((n2w.convert(id)), title, align, MATERIAL_ICON_POSITIVE, create_dt))
        #st.markdown(HABIT_DETAILS_TEMPLATE.format(id, title, align), unsafe_allow_html=True)

        stc.html(HABIT_DETAILS_TEMPLATE.format(update_dt))
        #stc.html(HABIT_DETAILS_TEMPLATE.format(create_dt, update_dt), scrolling=True)


    # css testing
    st.markdown(unsafe_allow_html=True, body=f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
            </style>
        """)


if __name__ == "__main__":
    run()