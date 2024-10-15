import streamlit as st

from my_pages.home import home

pages = {
    "Home":[
        st.Page("Home", home)
    ],

}

if __name__ == "__main__":
    pg = st.navigation(pages)
    pg.run()