import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import os

db_client = pymongo.MongoClient(os.getenv("MONGO_URL"))

def get_practice_data():
    collection = db_client['writing_king']['practice_stats']
    data = collection.find() # only one document
    return_value = {}
    if data:
        return_value['total_practice_times'] = data[0]['total_practice_times']
        return_value['total_task1_practice_times'] = data[0]['total_task1_practice_times']
        return_value['total_task2_practice_times'] = data[0]['total_task2_practice_times']
        return_value['all_task1_practice_scores'] = data[0]['all_task1_practice_scores'] # list of scores
        return_value['all_task2_practice_scores'] = data[0]['all_task2_practice_scores'] # list of scores
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
        st.plotly_chart(fig)
    else:
        st.write("Please practice first to see the scores")

    # show quick links
    col_link1, col_link2 = st.columns(2)
    with col_link1:
        st.write("Go to Practice")
        st.markdown("[Practice](/practice)")
    with col_link2:
        st.write("Go to History")
        st.markdown("[History](/history)")