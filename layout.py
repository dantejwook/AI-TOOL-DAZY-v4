import streamlit as st
from ui.sidebar import sidebar_controls
from ui.main_panel import main_panel

def render_layout():
    options = sidebar_controls()
    main_panel(options)
