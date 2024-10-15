import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px

# Pages
from my_pages.home import home

pages = {
    "Home":[
        st.Page("Home", home, icon=":material/home")
    ],

}

if __name__ == "__main__":
    pg = st.navigation(pages)
    pg.run()