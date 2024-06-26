import streamlit as st
import datetime
import time
import json
from classes.learner_class import Learner
from classes.volunteer_class import Volunteer
from classes.admin_class import Admin
from utils.body import (disclaimer_data_agreemet,html_home,
                        warning_data_sharing,succeed_signup,
                        warning_signup_failed,warning_empty_data
                        )       
from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter
from dataclasses import asdict
from typing import Dict


def register_button_func():
    st.session_state.register_button = not st.session_state.register_button

@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

def authenticated_menu():
    tribes_synonyms = {'Admin':'Sentinel','Volunteer':'Nomads','Learner':'Crew'}
    st.session_state.role_synonym = tribes_synonyms[st.session_state.user_auth.user_role]
    if st.session_state.user_auth is not None and st.session_state.user_auth.user_status == 'Activo':
        
        st.sidebar.page_link("app.py", label=f"Session @**{st.session_state.role_synonym}**")
        st.sidebar.page_link("pages/profile.py", label=f"User Profile")
        st.sidebar.page_link("pages/schedule.py", label=f"Enrollments")
        if st.session_state.user_auth.user_role == 'Volunteer':
            st.sidebar.page_link("pages/pensum-course.py", label=f"Building Pensum")

            # if st.session_state.role in ["Sentinel"] and st.session_state.user_auth in ['Admin']:
            #     st.sidebar.page_link(
            #         "pages/super-admin.py",
            #         label="Manage admin access",
            #         disabled=st.session_state.role != "Sentinel",
            #     )


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    # st.sidebar.html(html_home)
    st.sidebar.page_link("app.py", label="**Log In**")
    st.sidebar.page_link('pages/signup.py',label='**Sing Up**')
    

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    # try:
    if st.session_state.user_auth: 
        if st.session_state.user_auth.user_status == 'Activo':
            authenticated_menu()
    else:
        unauthenticated_menu()
    # except:
    #     st.switch_page('app.py')