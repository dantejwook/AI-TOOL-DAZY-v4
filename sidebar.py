import streamlit as st

def sidebar_controls():
    with st.sidebar:
        st.title("⚙️ 설정")
        return {
            "use_expand": st.toggle("GPT 의미 확장 사용", True),
            "make_zip": st.toggle("ZIP 생성", True),
        }
