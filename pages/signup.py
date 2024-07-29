import datetime as dt
from datetime import datetime
import streamlit as st
from menu import menu
import pandas as pd
from dataclasses import asdict
from utils.body import disclaimer_data_agreemet,warning_data_sharing,warning_empty_data,warning_signup_failed,succeed_signup,html_banner
import json
from google.cloud import firestore
import time
from classes.users_class import Users
from classes.firestore_class import Firestore
from classes.spread_class import Sheets
from classes.utils_class import CategoryUtils
import gspread
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from typing import List
from google.cloud.firestore_v1.base_query import FieldFilter


st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

def form_reponses():
    form_users_class = {
        'first_name':st.session_state._first_name, 
        'last_name':st.session_state._last_name,
        'email':st.session_state._email,
        'password':st.session_state._password,
        'address':st.session_state._address,
        'phone_number':st.session_state._phone_number,
        'dob':st.session_state._dob.strftime('%d-%m-%Y'),
        'gender':st.session_state._gender,
        'nationality':st.session_state._nationality,
        'id_user':st.session_state._id_user,
        'id_user_type':st.session_state._id_user_type,
        'is_ethnic':st.session_state._is_ethnic,
        'city_residence':st.session_state._city_residence, 
        'guardian_fullname':st.session_state._guardian_fullname,
        'guardian_relationship':st.session_state._guardian_relationship,
        'guardian_id':st.session_state._guardian_id,
        'guardian_id_type':st.session_state._guardian_id_type,
        'emergency_phone':st.session_state._emergency_phone,
        'education_level':st.session_state._education_level,
        'data_sharing':st.session_state._data_sharing,
        'topics_interest':st.session_state._topics_interest,
        'disability':st.session_state._disability,
        'ethnic_affiliation':st.session_state._ethnic_affiliation,
        'skills':st.session_state._skills,
        'how_to_learn':st.session_state._how_to_learn
    }

    return form_users_class

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
        ', '.join(instance_data.get('topics_interest', [])),
        ', '.join(instance_data.get('how_to_learn', [])),
        'signup'
    ]


@st.cache_data(ttl=3600,show_spinner=False)
def send_to_sheets(data: List[List[str]]):
    try:
        sheet = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM','Sign Up')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False


def signup_submition(form):
    instance = Users(**form)
    is_user_auth = connector().signup_preauth(instance.email, instance.id_user, instance.phone_number)

    if is_user_auth['status'] != 'sigup_approved':
        warning_signup_failed(is_user_auth)
    else:
        instance_data = asdict(instance)
        connector().add_document('users_collection',instance_data)
        sheets_data = prepare_sheets_data(instance_data)
        send_to_sheets([sheets_data]) 
        
        st.toast('¡Hip!')
        time.sleep(.5)
        st.toast('¡Hip!')
        time.sleep(.5)
        st.toast('¡Hurra! El registro se realizó correctamente.', icon='🎉')
        succeed_signup(st.session_state.role_synonym)


def signup_firestore():
    user_responces = form_reponses()
    if st.session_state._data_sharing:
        if all(user_responces.values()):
            signup_submition(user_responces)
        else: warning_empty_data()
    else:
        warning_data_sharing()

def register_users():

    st.text_input(label="Nombre",placeholder="Napoleón",key="_first_name",help=st.session_state.form_definitions['_first_name'])
    st.text_input(label="Apellido",placeholder="Bonaparte",key="_last_name",help=st.session_state.form_definitions['_last_name']) 
    st.text_input(label="Correo Electronico",placeholder="napoleon.bonaparte@mail.com",key="_email",help=st.session_state.form_definitions['_email'])
    st.text_input(label="Contraseña",placeholder="eMp3r@D0r",type="password",key="_password",help=st.session_state.form_definitions['_password'])
    st.text_input(label="Direccion",placeholder="Av. Conquista # 1804",key="_address",help=st.session_state.form_definitions['_address'])
    st.text_input(label="Telefono Celular",placeholder="555-888-9999",key="_phone_number",help=st.session_state.form_definitions['_phone_number'])
    st.date_input(label="Fecha Nacimiento", format="DD-MM-YYYY", value=dt.date(2000,1,1), min_value=dt.date(1940,1,1),max_value=dt.date(2020,12,31), key="_dob",help=st.session_state.form_definitions['_dob'])
    st.selectbox(label="Genero",index=0,options=st.session_state.gender,key="_gender",help=st.session_state.form_definitions['_gender'])
    st.text_input(label="Nacionalidad",placeholder="Francesa",key="_nationality",help=st.session_state.form_definitions['_nationality'])
    st.selectbox(label="Tipo D.I.",index=1,options=st.session_state.id_user_list, key="_id_user_type",help=st.session_state.form_definitions['_id_user_type']) 
    st.text_input(label="Número Documento Identidad",placeholder="80000000",key="_id_user",help=st.session_state.form_definitions['_id_user'])
    st.selectbox(label="¿Pertences a alguna Etnia?",index=1,options=["Si","No"],key="_is_ethnic",help=st.session_state.form_definitions['_is_ethnic']) 
    st.selectbox(label="¿Cual Etnia?",index=3,options=st.session_state.ethnics,key="_ethnic_affiliation",help=st.session_state.form_definitions['_ethnic_affiliation']) 
    st.text_input(label="Cuidad Residencia",placeholder="París",key="_city_residence",help=st.session_state.form_definitions['_city_residence'])
    st.text_input(label="Nombre Tutor legal/Emergencia",placeholder="Letizia Ramolino",key="_guardian_fullname",help=st.session_state.form_definitions['_guardian_fullname'])
    st.text_input(label="Parentesco",placeholder="Madre",key="_guardian_relationship",help=st.session_state.form_definitions['_guardian_relationship'])
    st.text_input(label="D.I. Tutor Legal",placeholder="5000000",key="_guardian_id",help=st.session_state.form_definitions['_guardian_id'])
    st.selectbox(label="Tipo D.I. Tutor",index=1,options=st.session_state.id_user_list,key="_guardian_id_type",help=st.session_state.form_definitions['_guardian_id_type'])
    st.text_input(label="Telefono Tutor/Emergencia",placeholder="555-888-4444",key="_emergency_phone",help=st.session_state.form_definitions['_emergency_phone'])
    st.selectbox(label="Nivel Educación",index=0,options=st.session_state.education_level,key="_education_level",help=st.session_state.form_definitions['_education_level'])
    st.multiselect(label="Temas Interes",options=st.session_state.topics_of_interest,placeholder="Choose an option",key="_topics_interest",help=st.session_state.form_definitions['_topics_interest'])
    st.multiselect(label="Discapacidad (PCD)",options=st.session_state.disabilities,placeholder="Choose an option",key="_disability",help=st.session_state.form_definitions['_disability'])
    st.multiselect(label="Selecciona tus habilidades", options=st.session_state.skills, placeholder="Choose an option", key="_skills",help=st.session_state.form_definitions['_skills'])
    st.multiselect(label="¿Cómo aprendes mejor?", options=st.session_state.how_to_learn, placeholder="Choose an option", key="_how_to_learn",help=st.session_state.form_definitions['_how_to_learn'])
    st.multiselect(label="¿Cuáles son tus debilidades?",options=st.session_state.weaknesses, placeholder="Choose an option", key="_weaknesses",help=st.session_state.form_definitions['_weaknesses'])
    st.multiselect(label="¿Cuáles son tus fortalezas?", options=st.session_state.strengths, placeholder="Choose an option", key="_strengths",help=st.session_state.form_definitions['_strengths'])


def sing_up():
    # Fill form for sign up users
    st.html(html_banner)
    st.subheader("**Sign Up | Circle Up ⚫**")

    st.markdown('Si todavía no eres miembro de nuestra comunidad, te invitamos a unirte. ¡Regístrate y comienza a formar parte de la experiencia Circle Up ⚫!')
    roles = {'Admin':'Sentinel','Volunteer':'Nomads','Learner':'Crew','Log In | Circle Up':'Crew'}

    with st.form("register_form",clear_on_submit=False):
        st.write("Bienvenido a la comunidad Crew, donde valoramos cada historia y experiencia única. Para formar parte de nuestra tribu, por favor completa los siguientes datos personales.")
        
        register_users()

        st.checkbox(disclaimer_data_agreemet,key="_data_sharing")
        st.form_submit_button('Regístrate',type="primary",help='Registro | Tribus',on_click=signup_firestore,use_container_width=True)

sing_up()

menu()

if st.button('Ingresar',type="primary",use_container_width=True):
    st.switch_page('app.py')

