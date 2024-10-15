import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import os

db_client = pymongo.MongoClient(os.getenv("MONGO_URL"))

def get_practice_data():
    collection = db_client['writing_king']['practices']
    data = list(collection.find()) # convert cursor to list

def history():
    st.title("History")