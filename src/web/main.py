import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px

# Pages
from my_pages.home import home

pages = {
    "Home":[
        st.Page(home, title="Home", icon="🏠"),
    ],

}

pg = st.navigation(pages)
pg.run()