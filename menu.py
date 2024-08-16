import streamlit as st
import json
from utils.body import html_home       
from google.cloud import firestore
from dataclasses import asdict
from typing import Dict
from classes.utils_class import CategoryUtils

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

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
        
        st.sidebar.image('./gallery/WebSvg/bear.svg', use_column_width=True)
        
        st.sidebar.info(f":blue[**{st.session_state.role_synonym}** Menu]")

        st.sidebar.page_link("app.py", label="Inicio", icon=":material/home:")
        st.sidebar.page_link("pages/profile.py", label="Perfil", icon=":material/person:")
        st.sidebar.page_link("pages/enroll.py", label="Explora Cursos", icon=":material/calendar_today:")
        st.sidebar.page_link("pages/attendance.py", label="Asistencia", icon=":material/edit_note:")

        if st.session_state.user_auth.user_role == 'Learner':
            st.sidebar.page_link("pages/volunteering.py", label="Ser Voluntario", icon=":material/volunteer_activism:")

        if st.session_state.user_auth.user_role in ['Volunteer','Admin']:
            st.sidebar.info(":blue[**Nomad Side**]")
            st.sidebar.page_link("pages/dashboard.py", label="Propuestas", icon=":material/groups:")

        if st.session_state.user_auth.user_role == 'Admin':
            st.sidebar.info(":blue[**Sentinel Side**]")
            st.sidebar.page_link("pages/make.py", label="Crear Ideas", icon=":material/lightbulb:")
            st.sidebar.page_link("pages/proposal.py", label="Proponer Cursos", icon=":material/rocket:")
            st.sidebar.page_link("pages/orchestrate.py", label="Gestión Voluntarios", icon=":material/group:")
            st.sidebar.page_link("pages/rollout.py", label="Revisar Cursos", icon=":material/menu_book:")
            
def unauthenticated_menu():
    st.sidebar.image('./gallery/WebSvg/bear.svg', use_column_width=True)
    st.sidebar.page_link("app.py", label="Registrarse", icon=":material/ads_click:") 
    st.sidebar.page_link('pages/signup.py',label='Crear Cuenta', icon=":material/app_registration:")
    st.sidebar.page_link("pages/docs.py", label="Investigación", icon=":material/experiment:")
    st.sidebar.page_link("pages/home.py", label="Community", icon=":material/diversity_3:")
    st.sidebar.page_link("pages/cbl.py", label="CBL Hub", icon=":material/hub:")


def menu():
    try:
        if st.session_state.user_auth: 
            if st.session_state.user_auth.user_status == 'Activo':
                authenticated_menu()
        else:
            unauthenticated_menu()
    except:
        st.switch_page('app.py')

