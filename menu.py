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
        if st.session_state.user_auth.user_role == 'Learner':
            st.sidebar.page_link("pages/be_volunteer.py", label="Volunteer Now")
        if st.session_state.user_auth.user_role in ['Volunteer','Admin']:
            st.sidebar.page_link("pages/pensum-volunteer.py", label=f"Pensum Template")
            st.sidebar.page_link("pages/make_course.py", label=f"Brainstorm Ideas")
            if st.session_state.user_auth.user_role == 'Admin':
                st.sidebar.page_link("pages/pensum-admin.py",label="Pensum Review")
                st.sidebar.page_link("pages/accept_volunteer.py",label="Volunteer Roles")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="**Log In**")
    st.sidebar.page_link('pages/signup.py',label='**Sing Up**')

def menu():
    # try:
    if st.session_state.user_auth: 
        if st.session_state.user_auth.user_status == 'Activo':
            authenticated_menu()
    else:
        unauthenticated_menu()
    # except AttributeError:
    #     st.switch_page('app.py')