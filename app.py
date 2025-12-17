import streamlit as st
from ui.layout import render_layout

st.set_page_config(
    page_title="AI dazy document sorter",
    page_icon="🗂️",
    layout="wide",
)

render_layout()
