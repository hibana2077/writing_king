import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import os

db_client = pymongo.MongoClient(os.getenv("MONGO_URI"))

def get_practice_data():
    collection = db_client['writing_king']['practice_stats']
    data = collection.find() # only one document
    return_value = {}
    if data:
        return_value['total_practice_times'] = data[0]['total_practice_times']
        return_value['total_task1_practice_times'] = data[0]['total_task1_practice_times']
        return_value['total_task2_practice_times'] = data[0]['total_task2_practice_times']
    else:
        return_value['total_practice_times'] = 0
        return_value['total_task1_practice_times'] = 0
        return_value['total_task2_practice_times'] = 0

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