import streamlit as st

def login():
    password = st.text_input("Enter the admin password", type="password")
    if password == "renotitan@h2":
        st.session_state['logged_in'] = True
    else:
        st.warning("Incorrect password")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    login()
else:
    st.success("Welcome to the Admin Panel")
