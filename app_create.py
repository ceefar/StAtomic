# imports 
# for web app and test components
import streamlit as st




topper = st.container()
creator = st.container()


def run():

    # header topper
    with topper:

        st.title(f"St.Atomic - The Atomic Todo App")
        st.subheader(f"Create A New Habit")
        st.write("##")


    with creator:
        col1, col2 = st.columns(2)

        st.subheader(f"So [NAME] What Do You Want To Start Improving?")
        st.write("Choose **Habit** or **Preset Habit** for short habits to develop")
        st.write("Or if you have a classic style todo task you want to remember, choose **Classic Todo**")
        st.write("##")

        with col2:

            # just a v0.1 concept for now, maybe remove or update shortly

            task_type = st.selectbox(
            "What Kind of Habit or Task Do You Want To Add",
            ('Habit', 'Preset Habit', 'Classic Todo'))

            
            task_type_radio = st.radio(
            "What Kind of Habit or Task Do You Want To Add",
            ('Habit', 'Preset Habit', 'Classic Todo'))


        with col1:

            # yeah legit dropdown better for other stuff radio is fine here

            if task_type == "Classic Todo":
                st.write("Use This For Longer, Classic Style Todo Tasks, If You Want To Develop A Proper Habit Over Time, Choose **Habit** Instead")
                base_task = st.text_area("Add Your Todo Task Here")

            elif task_type == "Habit":
                st.write("Use This For Longer, Classic Style Todo Tasks, If You Want To Develop A Proper Habit Over Time, Choose **Habit** Instead")
                base_task = st.text_input("Add Your Todo Task Here")



if __name__ == "__main__":
    run()