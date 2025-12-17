import streamlit as st

def progress_ui():
    bar = st.progress(0)
    text = st.empty()
    return bar, text

def log_ui():
    box = st.empty()
    logs = []
    def log(msg):
        logs.append(msg)
        box.markdown("<br>".join(logs[-10:]), unsafe_allow_html=True)
    return log
