from datetime import datetime
import time
import json
import streamlit as st
from google.cloud import firestore
from menu import menu
from classes.users_class import Users
from classes.firestore_class import Firestore
from classes.spread_class import Sheets   
from classes.utils_class import CategoryUtils
from typing import List, Dict, Optional
from dataclasses import asdict
from utils.form_options import (disabilities,ethnics,skills,
                                how_to_learn,weaknesses,strengths,
                                volunteer_keywords,gender_list,id_user_list,
                                topics_of_interest,education_level)

from utils.form_instructions import form_definitions
from utils.body import html_banner

def user_to_json(user: Users) -> str:
    return json.dumps(asdict(user))

# Función para deserializar JSON a Users
def json_to_user(json_str: str) -> Users:
    return Users(**json.loads(json_str))

# Función para cargar usuario desde st.session_state
def load_user_from_session() -> Optional[Users]:
    if 'user_data' in st.session_state:
        return json_to_user(st.session_state.user_data)
    return None

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize disabilities
if 'disabilities' not in st.session_state:
    st.session_state.disabilities = disabilities

# Initialize ethnics
if 'ethnics' not in st.session_state:
    st.session_state.ethnics = ethnics

# Initialize skills
if 'skills' not in st.session_state:
    st.session_state.skills = skills

# Initialize how to learn
if 'how_to_learn' not in st.session_state:
    st.session_state.how_to_learn = how_to_learn

# Initialize weaknesses
if 'weaknesses' not in st.session_state:
    st.session_state.weaknesses = weaknesses

# Initialize strengths
if 'strengths' not in st.session_state:
    st.session_state.strengths = strengths

# Initialize volunteer keywords
if 'volunteer_keywords' not in st.session_state:
    st.session_state.volunteer_keywords = volunteer_keywords

# Initialize gender list
if 'gender' not in st.session_state:
    st.session_state.gender = gender_list

# Initialize form definitions
if 'form_definitions' not in st.session_state:
    st.session_state.form_definitions = form_definitions

# Initialize id user list
if 'id_user_list' not in st.session_state:
    st.session_state.id_user_list = id_user_list

# Initialize topics of interest
if 'topics_of_interest' not in st.session_state:
    st.session_state.topics_of_interest = topics_of_interest

# Initialize education level
if 'education_level' not in st.session_state:
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
    st.session_state.user_auth = load_user_from_session()

if 'page_selected' not in st.session_state:
    st.session_state.page_selected = None

if 'page_msm' not in st.session_state:
    st.session_state.page_msm = 'status'

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

def show_navigation():
    pages = {
        "Perfil": "pages/profile.py",
        "Explora Cursos": "pages/enroll.py",
        "Asistencia": "pages/attendance.py"
    }

    if st.session_state.user_auth.user_role == 'Learner':
        pages["Ser Voluntario"] = "pages/volunteering.py"

    
    if st.session_state.user_auth.user_role in ['Volunteer', 'Admin']:
        pages["Propuestas"] = "pages/dashboard.py"

    if st.session_state.user_auth.user_role == 'Admin':
        pages["Proponer Curso"] = "pages/proposal.py"
        pages["Crear Ideas"] = "pages/make.py"
        pages["Gestión Voluntarios"] = "pages/orchestrate.py"
        pages["Revisar Cursos"] = "pages/rollout.py"

    return pages

def prepare_sheets_data(instance_data: dict) -> list[str]:
    """
    Prepara los datos específicos para enviar a Google Sheets.
    """
    utils = CategoryUtils()
    now = datetime.now()
    return [
        utils.get_current_date(),
        utils.date_to_day_of_week(),
        utils.time_to_category(),
        instance_data.get('first_name', ''),
        instance_data.get('last_name', ''),
        instance_data.get('gender', ''),
        utils.age_to_category(instance_data.get('dob', '')),
        instance_data.get('email', ''),
        instance_data.get('user_role', ''),
        instance_data.get('city_residence', ''),
        'login'
    ]

@st.cache_data(ttl=900,show_spinner=False)
def send_to_sheets(data: List[List[str]]) -> bool:
    try:
        sheet: Sheets = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM','Log In')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False

def login_setup(email: str, password: str) -> str:
    if not email or not password:
        return "incomplete_fields"
    try:
        with st.spinner(f'Preparando tu espacio personal...'):
            query_data = connector().auth_firestore(email, password)
            time.sleep(2)
            instance = Users(**query_data)
            instance_data = asdict(instance)
            sheets_data = prepare_sheets_data(instance_data)
            send_to_sheets([sheets_data])
            time.sleep(2)
        st.session_state.user_auth = instance
        st.session_state.user_data = user_to_json(instance)
        st.session_state.login_status = 'logged_in'
        return "success"
    except:
        st.session_state.user_auth = None
        return "wrong_password"

st.html(html_banner)

user_agent = st.context.headers.get('User-Agent', 'Desconocido')

intro_message = """
Circle Up Community ⚫ es una plataforma dedicada a la :blue-background[gestión de propuestas e ideas] para la comunidad. 
"""

st.title(f":material/ads_click: **Log In | Circle Up Community**")

with st.container():

    st.markdown("Ingresa con tus datos para continuar. Si aún no tienes una cuenta, dirígete a :blue-background[**Únete/Regístrate**]") 
    
    with st.form(key='login_form', clear_on_submit=False):

        email = st.text_input(label="Correo electrónico", placeholder="mail@mail.com", key="_email_entered")      
        password = st.text_input(label="Contraseña", placeholder="eMp3r@D0r", key="_password_entered", type="password")
        
        submit_button = st.form_submit_button(label=":material/ads_click: Ingresar", type="secondary", use_container_width=True)

    if submit_button:
        st.session_state.user_auth = None
        status = login_setup(email, password)
        st.session_state.page_msm = 'success' if status == 'success' else 'fail'
        # st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(':material/touch_app: Únete/Regístrate', type="primary", help='Registro', use_container_width=True):
            st.switch_page('pages/signup.py')
    with col2:
        st.link_button(':material/person_raised_hand: ¿Qué es Circle Up?', url='https://circleup.com.co/', type="secondary", use_container_width=True)
    
    if st.session_state.page_msm == 'success':
        st.success("Tu cuenta ha sido :green-background[autenticada]. Explora las funcionalidades disponibles para ti. Usa el :green-background[Quick Menu]", icon=":material/passkey:")
    elif st.session_state.page_msm == 'fail':
        st.error(":red-background[No pudimos iniciar sesión]. Por favor, revisa tu :red-background[correo electrónico o contraseña.]", icon=":material/password:")
    else:
        pass

    if st.session_state.user_auth is not None:
        pages = show_navigation()
        selected_page = st.selectbox("Quick Menu", options=list(pages.keys()),key='page_selected')
        if selected_page:
            st.switch_page(pages[selected_page])
    
    st.info(":blue[**¿Necesitas ayuda?**] Escribe a :blue-background[wearecircleup@gmail.com]", icon=":material/sos:")

menu()