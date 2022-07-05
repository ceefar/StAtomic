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
db_username = user_name.lower()

# ---- layout ----
# either use more or remove pls, as barely using rn

topper = st.container()
intro = st.container()


# ---- page functions ----


# ---- session state declarations ----



# ---- main page ----

def run():

    # ---- SECTION ----
    
    # header topper
    with topper:

        st.write("##### Discord")

    # ---- SECTION ----

    # todo task create intro and setup
    with intro:

        stc.html("""
        <widgetbot
        server="972790226504282132"
        channel="972790226504282135"
        width="800"
        height="600"
        ></widgetbot>
        <script src="https://cdn.jsdelivr.net/npm/@widgetbot/html-embed"></script>
        """, height=1000, width=1000)

















if __name__ == "__main__":
    run()