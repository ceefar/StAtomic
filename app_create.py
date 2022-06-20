# imports 
# for web app and test components
import streamlit as st
import streamlit.components.v1 as stc # < unused at present


# temp globals for testing/setup
actual_name = "Ceefar"
user_tags = ["fitness - cardio","fitness - trim","fitness - bulk","conditions - adhd","conditions - anxiety","skills - mysql","skills - portfolio","skills - programming","software - streamlit","lifestyle - wellness"]


# layout - maybe temp since barely using tbf
topper = st.container()


# page functions

def add_habit_to_db_v0():
    pass


def run():

    # header topper
    with topper:

        st.title(f"St.Atomic - The Atomic Todo App")
        st.subheader(f"Create A New Habit")
        st.write("---")


    with st.container():

        st.subheader(f"So {actual_name} What Do You Want To Start Improving?")
        col1A, _ = st.columns([4,1])
        col1A.write("Choose **Habit** or **Preset Habit** for short habits to develop, or if you have a classic style todo task you want to remember, choose **Classic Todo**")
        st.write("##")
        
        task_type = st.selectbox(
        "Habit Type",
        ('Habit', 'Preset Habit', 'Classic Todo'))

        st.write("##")

        with st.form(key="habit_task_form_v0"):

            if task_type == "Habit":
                st.write("**Use This For Developing Atomic Habits - It's What St.Atomic Is Made For!**")
                base_habit = st.text_input("What Habit Do You Want To Grow?")
                st.write("give a basic example duh (maybe inside the box double duh")

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

                st.write("What Areas Does This Relate To?")
                habit_tags = st.multiselect("Add Tags",user_tags)
                st.write("You can update tags later blah... by adding tags St.Atomic can help you form connections between similar habits lorem")

                st.write("---")

                submit_habit_form = st.form_submit_button(label="Start This Habit")



            elif task_type == "Classic Todo":
                st.write("Use This For Longer, Classic Style Todo Tasks, For Atomic Habits Choose **Habit** Instead")
                base_todo = st.text_area("Add Your Todo Task Here")
                submit_habit_form = st.form_submit_button(label="Add To My Todo List")


            elif task_type == "Preset Habit":
                st.write("Full Functionality Coming Soon - Watch This Space!")
                base_preset = st.selectbox("Choose A Preset Type",("Work - Programmer", "Exercise - Bulk up", "Exercise - Lose Weight", "Conditions - Adhd", "Lifestyle - Inner Peace"))
                
                submit_habit_form = st.form_submit_button(label="Coming Soon")


            if submit_habit_form:
                if task_type == "Habit":
                    add_habit_to_db_v0(base_habit, habit_alignment, habit_tags)







if __name__ == "__main__":
    run()