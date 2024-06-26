import json
import streamlit as st
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import pandas as pd
import numpy as np
import time
import datetime
from dataclasses import dataclass
import streamlit.components.v1 as components
from menu import menu
from utils.body import warning_login_failed
from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter
from dataclasses import asdict
from classes.admin_class import Admin
from classes.learner_class import Learner
from classes.volunteer_class import Volunteer

from utils.form_admin import admin_base
from utils.form_learner import learner_base
from utils.form_volunteer import volunteer_base

from utils.form_options import (disabilities,ethnics,skills,
                                how_to_learn,weaknesses,strengths,
                                volunteer_keywords,gender_list,id_user_list,
                                topics_of_interest,education_level)

from utils.form_instructions import form_definitions
from utils.body import tribu_definition,html_banner


st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize Forms Opcions
if 'disabilities' not in st.session_state:
    st.session_state.disabilities = disabilities
    st.session_state.ethnics = ethnics
    st.session_state.skills = skills
    st.session_state.how_to_learn = how_to_learn
    st.session_state.weaknesses = weaknesses
    st.session_state.strengths = strengths
    st.session_state.volunteer_keywords = volunteer_keywords
    st.session_state.gender = gender_list
    st.session_state.form_definitions = form_definitions
    st.session_state.id_user_list = id_user_list
    st.session_state.topics_of_interest = topics_of_interest
    st.session_state.education_level = education_level


if "_email_entered" not in st.session_state:
    st.session_state._email_entered = None
    st.session_state._password_entered = None

# Initialize TTL for Cache Data
if 'ttl_data' not in st.session_state:
    st.session_state.ttl_data = 5
        

# Initialize Roles Translation
if 'role_synonym' not in st.session_state:
        st.session_state.role_synonym = 'Crew'

# Initialize Register Button to use it a Toggle Button
if 'register_button' not in st.session_state:
        st.session_state.register_button = False
        

# Initialize Register Button to use it a Toggle Button
if '_is_ethnic' not in st.session_state:
        st.session_state._is_ethnic = "No"
        st.session_state._is_ethnic_affiliation = True

# Initialize st.session_state.auth to Log In | Circle Up
if "user_auth" not in st.session_state:
    st.session_state.user_auth = None

@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

@st.cache_data(show_spinner=False)
def catch_user(cls_role,email,password,connection):
    intance = cls_role()
    intance.user_authentication(email,password,connection)
    if any(asdict(intance).values()):
        st.toast('¡Validación exitosa!', icon='🎉')
        return intance

def login_setup(cls_role,email,password,connection):
    if email and password:
        st.session_state.user_auth = catch_user(cls_role,email,password,connection)
    else:
        warning_login_failed(st.session_state._email_entered,st.session_state._password_entered)

def login_fetch(email,password):   
    if email is not None and password is not None:
        login_setup(Learner,email,password,firestore_client())
    else:
        warning_login_failed(st.session_state._email_entered,st.session_state._password_entered)

st.html(html_banner)

intro_message = """
Circle Up ⚫ es una plataforma dedicada a la gestión de propuestas e ideas de aquellos que desean compartir su conocimiento con la comunidad. 
Ofrecemos un espacio seguro, fácil de usar, gratuito y sin ánimo de lucro.
"""
container_message = """
Elige :blue[**Crew**] para descubrir y aprender, o :blue[**Nomad/Sentinel**] para crear y guiar. ¿Listo para sumergirte? Haz clic en :blue[**Aprende sobre tribus**] y comienza en Circle Up ⚫.
"""

st.subheader(f"**Log In | Circle Up** ⚫")

st.markdown(intro_message)

with st.container(height=310):

    st.markdown("Por favor, ingresa con tus datos registrados para continuar. Si aún no tienes una cuenta, dirígete al botón de :blue[**Registro/Sign Up**]") 
    st.text_input(label="Correo electrónico",placeholder="mail@mail.com",key="_email_entered")      
    st.text_input(label="Contraseña",placeholder="eMp3r@D0r",key="_password_entered",type="password") 
    st.button(label="Ingresar",type="primary",on_click=login_fetch,args=[st.session_state._email_entered,st.session_state._password_entered],use_container_width=True)


with st.container(height=170):
    st.markdown(container_message)
    cols = st.columns([2,2])
    cols[0].button(f'¡Aprende Sobre Tribus!',type="secondary",on_click=tribu_definition,use_container_width=True)
    cols[1].link_button('¿Qué es Circle Up?',url='https://circleup.com.co/',type="primary",use_container_width=True)


menu() # Render the dynamic menu!

