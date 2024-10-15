import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
import os

def practice():
    st.title("IELTS Writing Practice")

    with st.form(key='ielts_form'):
        tab1, tab2 = st.tabs(["Task 1", "Task 2"])

        with tab1:
            st.write("Task 1: Describe the information in the chart below.")
            # Placeholder for Task 1 plot
            # Example: fig = px.bar(...)
            # st.plotly_chart(fig)
            t1_essay = st.text_area("Enter your IELTS Task 1 essay here:")

        with tab2:
            st.write("Task 2: Write an essay on the given topic.")
            t2_essay = st.text_area("Enter your IELTS Task 2 essay here:")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.write("Submitted!")
        st.write("Task 1 Essay:")
        st.write(t1_essay)
        st.write("Task 2 Essay:")
        st.write(t2_essay)