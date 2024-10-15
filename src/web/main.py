import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px

# Pages
from my_pages.home import home
from my_pages.practice import practice
from my_pages.history import history

pages = {
    "Home":[
        st.Page(home, title="Home", icon="🏠"),
    ],
    "Practice":[
        st.Page(practice, title="Practice", icon="📝"),
    ],
    "History":[
        st.Page(history, title="History", icon="📜"),
    ]
}

pg = st.navigation(pages)
pg.run()