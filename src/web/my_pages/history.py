import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import os

db_client = pymongo.MongoClient(os.getenv("MONGO_URL"))

def get_practice_data():
    collection = db_client['writing_king']['practices']
    data = list(collection.find()) # convert cursor to list
    return data

@st.dialog("Details", width = "large")
def show_details(practice_data):
    tab_task1, tab_task2 = st.tabs(['Task 1', 'Task 2'])
    with tab_task1:
        st.subheader("Task 1")
        st.write(f"Task 1 Questions: {practice_data['task1_data']['Task 1 Data']['Task 1 Description']}")
        st.write(f"Task 1 Essay: {practice_data['task1_data']['Task 1 Essay']}")
        st.subheader(f"Task 1 Score:")
        st.write(f"Task 1 Coherence and Cohesion: {practice_data['task1_data']['Coherence and Cohesion']}")
        st.write(f"Task 1 Lexical Resource: {practice_data['task1_data']['Lexical Resource']}")
        st.write(f"Task 1 Grammatical Range and Accuracy: {practice_data['task1_data']['Grammatical Range and Accuracy']}")
        st.write(f"Task 1 Task Achievement: {practice_data['task1_data']['Task Achievement']}")
        # st.write(f"Task 1 Feedback: {practice_data['task1_data']['Feedback']}")
        for key in practice_data['task1_data']['Feedback']:
            st.write(f"{key}: {practice_data['task1_data']['Feedback'][key]}")
    with tab_task2:
        st.subheader("Task 2")
        st.write(f"Task 2 Questions: {practice_data['task2_data']['Task 2 Data']['Task 2 Question']}")
        st.write(f"Task 2 Essay: {practice_data['task2_data']['Task 2 Essay']}")
        st.subheader(f"Task 2 Score:")
        st.write(f"Task 2 Coherence and Cohesion: {practice_data['task2_data']['Coherence and Cohesion']}")
        st.write(f"Task 2 Lexical Resource: {practice_data['task2_data']['Lexical Resource']}")
        st.write(f"Task 2 Grammatical Range and Accuracy: {practice_data['task2_data']['Grammatical Range and Accuracy']}")
        st.write(f"Task 2 Task Achievement: {practice_data['task2_data']['Task Achievement']}")
        # st.write(f"Task 2 Feedback: {practice_data['task2_data']['Feedback']}")
        for key in practice_data['task2_data']['Feedback']:
            st.write(f"{key}: {practice_data['task2_data']['Feedback'][key]}")

def history():
    st.title("History")

    if st.button("Refresh"):
        st.rerun()

    practice_data = get_practice_data()

    if practice_data:
        for it,data in enumerate(practice_data):
            with st.container(border=True):
                st.write(f"Datetime: {data['date'][:-7]}")
                st.write(f"Overall Score: {data['overall_score']}")
                # button to see the details
                if st.button("Show Details", key=f"show_details_{it}"):
                    show_details(data)

    else:
        st.write("No practice data found!")