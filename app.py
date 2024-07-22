import datetime as dt
from datetime import datetime
import json
import streamlit as st
from google.cloud import firestore
from menu import menu
from google.cloud import firestore
from classes.users_class import Users
from classes.firestore_class import Firestore
from classes.spread_class import Sheets   
from classes.utils_class import CategoryUtils
from typing import List
import gspread
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from dataclasses import asdict
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
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

def show_login_feedback(status: str, email: str = None):
    if status == "success":
        st.toast("Inicio de sesión exitoso", icon="✅")
        st.success("Bienvenido de nuevo a Circle Up")
        st.info("Has iniciado sesión correctamente. Ahora puedes acceder a todas las funcionalidades de la plataforma.")
    elif status == "wrong_password":
        st.toast("Contraseña incorrecta", icon="⚠️")
        st.error("La contraseña ingresada no es correcta")
        st.warning(
            "- Las contraseñas distinguen entre mayúsculas y minúsculas\n"
            "- Verifica que no tengas el bloq mayús activado"
        )
    else:
        st.toast("Error de inicio de sesión", icon="⚠️")
        st.error("No se pudo completar el inicio de sesión")
        st.warning(
            "Por favor, **verifica**\n"
            "- El correo electrónico está escrito correctamente\n"
            "- La contraseña es la correcta\n"
            "- No hay espacios adicionales en los campos"
        )

def prepare_sheets_data(instance_data):
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

@st.cache_data(ttl=3600,show_spinner=False)
def send_to_sheets(data: List[List[str]]):
    try:
        sheet = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM','Log In')
        sheet.create(data)
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False

def login_setup(email, password):
    if not email or not password:
        return "incomplete_fields"

    try:
        query_data = connector().auth_firestore(email, password)
        instance = Users(**query_data)
        instance_data = asdict(instance)
        sheets_data = prepare_sheets_data(instance_data)
        send_to_sheets([sheets_data]) 
    except:
        instance = None
    if instance:
        st.session_state.user_auth = instance
        return "success"
    else:
        return "wrong_password"


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

with st.container():
    st.markdown("Por favor, ingresa con tus datos registrados para continuar. Si aún no tienes una cuenta, dirígete al botón de :blue[**Registro/Sign Up**]") 
    st.text_input(label="Correo electrónico",placeholder="mail@mail.com",key="_email_entered")      
    st.text_input(label="Contraseña",placeholder="eMp3r@D0r",key="_password_entered",type="password") 

    feedback_container = st.empty()

    if st.button(label="Ingresar", type="primary", use_container_width=True):
        login_result = login_setup(st.session_state._email_entered, st.session_state._password_entered)

        with feedback_container:
            show_login_feedback(login_result, st.session_state._email_entered)

with st.container():
    st.markdown(container_message)
    cols = st.columns([1, 1])
    with cols[0]:
        st.button(f'¡Aprende Sobre Tribus!',type="secondary",on_click=tribu_definition,use_container_width=True)
    with cols[1]:
        st.link_button('¿Qué es Circle Up?',url='https://circleup.com.co/',type="primary",use_container_width=True)

menu()