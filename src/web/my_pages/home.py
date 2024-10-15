import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import os

db_client = pymongo.MongoClient(os.getenv("MONGO_URL"))

def get_practice_data():
    collection = db_client['writing_king']['practice_stats']
    data = list(collection.find()) # convert cursor to list
    return_value = {}
    if data:
        return_value['total_practice_times'] = data[0]['total_practice_times']
        return_value['total_task1_practice_times'] = data[0]['total_task1_practice_times']
        return_value['total_task2_practice_times'] = data[0]['total_task2_practice_times']
        return_value['all_task1_practice_scores'] = data[0]['all_task1_practice_scores'][-10:] # list of scores
        return_value['all_task2_practice_scores'] = data[0]['all_task2_practice_scores'][-10:] # list of scores
    else:
        return_value['total_practice_times'] = 0
        return_value['total_task1_practice_times'] = 0
        return_value['total_task2_practice_times'] = 0
        return_value['all_task1_practice_scores'] = []
        return_value['all_task2_practice_scores'] = []

    return return_value


def home():
    st.title("Home")
    st.write("Welcome to my app!")

    practice_data = get_practice_data()

    # use metric card to display the data
    st.subheader("Practice Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Practice Times", practice_data['total_practice_times'])
    with col2:
        st.metric("Total Task 1 Practice Times", practice_data['total_task1_practice_times'])
    with col3:
        st.metric("Total Task 2 Practice Times", practice_data['total_task2_practice_times'])

    # plot the scores (line chart)
    if practice_data['all_task1_practice_scores'] and practice_data['all_task2_practice_scores']:
        df = pd.DataFrame({
            'Task 1': practice_data['all_task1_practice_scores'],
            'Task 2': practice_data['all_task2_practice_scores']
        })
        fig = px.line(df)
        fig.update_layout(title="Practice History", xaxis_title="Practice Times", yaxis_title="Scores")
        st.subheader("Practice History")
        st.plotly_chart(fig)
    else:
        _ = 1+1

    # show quick links
    st.subheader("Quick Links")
    col_link1, col_link2 = st.columns(2)
    with col_link1:
        st.write("Go to Practice")
        st.markdown("[Practice](/practice)")
    with col_link2:
        st.write("Go to History")
        st.markdown("[History](/history)")

    # FAQ (expandable text)
    st.subheader("FAQ")
    with st.expander("What is IELTS?"):
        st.markdown("IELTS is the **International English Language Testing System**. It measures ability to communicate in English across all four language skills – listening, reading, writing and speaking – for people who intend to study or work where English is the language of communication.")

    with st.expander("How to prepare for IELTS Writing?"):
        st.markdown("You can practice writing essays on various topics. You can also analyze the essays written by others to understand the structure and vocabulary used. Make sure to practice regularly to improve your writing skills.")

    with st.expander("How to improve IELTS Writing score?"):
        st.write("You can improve your IELTS Writing score by practicing regularly, expanding your vocabulary, and paying attention to grammar and punctuation. You can also get feedback on your essays from teachers or peers to identify areas for improvement.")

    with st.expander("What is the format of IELTS Writing test?"):
        st.write("The IELTS Writing test consists of two tasks. Task 1 requires you to describe visual information in your own words. Task 2 requires you to write an essay on a given topic. You have 60 minutes to complete both tasks.")

    with st.expander("How to manage time in IELTS Writing test?"):
        st.write("To manage time in the IELTS Writing test, you can allocate around 20 minutes for Task 1 and 40 minutes for Task 2. Make sure to plan your essays before writing and leave some time for proofreading at the end.")

    with st.expander("What is the scoring criteria for IELTS Writing?"):
        st.write("The IELTS Writing test is scored based on four criteria: Task Achievement, Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy. Each criterion is scored on a scale of 0-9, and the scores are averaged to give the final Writing score.")

    with st.expander("Who developed This App?"):
        st.write("This app was developed by [hibana2077](https://hibana2077.com). If you have any questions or feedback, feel free to create an issue on the [GitHub repository](https://github.com/hibana2077/writing_king).")