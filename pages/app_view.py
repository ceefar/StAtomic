# imports 
# for web app and test components
import streamlit as st
import streamlit.components.v1 as stc
# for db access
import db_integration as atomdb
# for datatime objects
from datetime import datetime



def get_db_data_temp() -> tuple:
    # obvs len considerations duh, paginate with offset based on amount of valid entries you want to display
    base_data = atomdb.get_base_habit_data_v0()
    return(base_data)


def format_dt(dt) -> str:
    """ use paramters to set formatting type """
    formatted_datetime = dt.strftime("%m/%d/%Y, %H:%M:%S")
    return(formatted_datetime)


HABIT_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;
border=5px;box-shadow:0 0 1px 1px #eee; background-color:#31333F;
border-left:5px solid #6c6c6c;color:white;">
<h4>{}</h4>
<h4>{}</h4>
<h4>{}</h4>
</div>
"""

HABIT_DETAILS_TEMPLATE = """
<div>
<h4>{} {}</h4>
</div>
"""


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
        
        stc.html(HABIT_HTML_TEMPLATE.format(id, title, align), )
        #st.markdown(HABIT_DETAILS_TEMPLATE.format(id, title, align), unsafe_allow_html=True)
        with st.expander("Details"):
            stc.html(HABIT_DETAILS_TEMPLATE.format(create_dt, update_dt), scrolling=True)



if __name__ == "__main__":
    run()