# imports 
# for web app and test components
import streamlit as st
import streamlit.components.v1 as stc # < unused at present
# for db access
import db_integration


# temp globals for testing/setup
actual_name = "Ceefar"
user_tags = ["fitness - cardio","fitness - trim","fitness - bulk","conditions - adhd","conditions - anxiety","skills - mysql","skills - portfolio","skills - programming","software - streamlit","lifestyle - wellness"]

# these will just be db names, so do check if none exist already then show default else show existing.
# some kinda option for premade or like preset would be cool but not rn ffs lol
tasks_lists = ["My List"]

# layout - maybe temp since barely using tbf
topper = st.container()


# page functions

def add_todo_task_to_db():
    pass


def run():

    # header topper
    with topper:

        st.title(f"St.Atomic")
        st.subheader(f"Add Tasks")
        st.write("---")


    with st.container():

        st.subheader(f"So {actual_name} what are we planning?")
        col1A, _ = st.columns([4,1])
        col1A.write("Information lorem")
        st.write("##")
        



        with st.form(key="todo_task_creator"):


            st.write("**What Do You Want To Do?**")
            todo_title = st.text_input("Enter Task Title", value="a basic example", key="td_title")

            todo_detail = st.text_area("Enter Task Details", value="a more thorough example", key="td_detail")

            st.write("---")

            col1B,col3B = st.columns([2,3])
            col1B.write("What Is The Task's Alignment?")
            col3B.write("What Are Alignments?")

            col1C,_,col3C = st.columns([1,1,3])
            with col1C:
                habit_alignment = st.radio("Choose 1",
                ('Positive', 'Neutral', 'Negative'))
            with col3C:
                if habit_alignment == "Positive":
                    st.write(":white_check_mark: Positive habits are ones that you **want** to develop, these are things that will improve your life in some way or another, however small or big. Think things like 'Read More', 'Meditate', 'Practice Coding', 'Work Out'.")

            st.write("---")
            st.write("**Optional Enhancements**")
            st.write("Make getting stuff done easier by taking 30 seconds to quickly configure...") # not configure its not a techy app its a todo list ffs

            st.write("What Areas Does This Relate To?")
            habit_tags = st.multiselect("Add Tags",user_tags)
            st.write("You can update tags later blah... by adding tags St.Atomic can help you form connections between similar habits lorem")

            st.write("---")

            base_preset = st.selectbox("Choose A Preset Type", ("Work - Programmer", "Exercise - Bulk up", "Exercise - Lose Weight", "Conditions - Adhd", "Lifestyle - Inner Peace"))
            
            submit_habit_form = st.form_submit_button(label="Coming Soon")

            task_type = st.selectbox("Your Tasks Lists", ('Habit', 'Preset Habit', 'Classic Todo'))


            if submit_habit_form:
                add_todo_task_to_db()







if __name__ == "__main__":
    run()