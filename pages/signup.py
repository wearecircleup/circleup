import datetime as dt
from datetime import datetime
import streamlit as st
from menu import menu
from dataclasses import asdict
from utils.body import disclaimer_data_agreemet, html_banner
from utils.form_options import municipios
import json
from google.cloud import firestore
import time
from classes.users_class import Users
from classes.firestore_class import Firestore
from classes.spread_class import Sheets
from classes.utils_class import CategoryUtils
from typing import List
import re
import pandas as pd
from utils.form_instructions import form_definitions
from utils.form_options import (disabilities,ethnics,skills,
                                how_to_learn,weaknesses,strengths,
                                volunteer_keywords,gender_list,id_user_list,
                                topics_of_interest,education_level)

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.session_state.page_selected = None

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

def form_reponses():
    utils = CategoryUtils()

    form_users_class = {
        'first_name':st.session_state._first_name, 
        'last_name':st.session_state._last_name,
        'email':st.session_state._email.lower().strip(),
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
        'how_to_learn':st.session_state._how_to_learn,
        'weaknesses':st.session_state._weaknesses,
        'strengths':st.session_state._strengths,
        'parental_consent':utils.parental_review(st.session_state._dob.strftime('%d-%m-%Y'))
    }
    return form_users_class

FIELD_LABELS = {
    "_first_name": "Nombre",
    "_last_name": "Apellido",
    "_email": "Correo Electrónico",
    "_password": "Contraseña",
    "_address": "Dirección",
    "_phone_number": "Teléfono Celular",
    "_dob": "Fecha Nacimiento",
    "_gender": "Género",
    "_nationality": "Nacionalidad",
    "_id_user": "Número Documento Identidad",
    "_id_user_type": "Tipo D.I.",
    "_is_ethnic": "¿Perteneces a alguna Etnia?",
    "_city_residence": "Ciudad Residencia",
    "_guardian_fullname": "Nombre Tutor legal/Emergencia",
    "_guardian_relationship": "Parentesco",
    "_guardian_id": "D.I. Tutor Legal",
    "_guardian_id_type": "Tipo D.I. Tutor",
    "_emergency_phone": "Teléfono Tutor/Emergencia",
    "_education_level": "Nivel Educación",
    "_topics_interest": "Temas Interés",
    "_disability": "Discapacidad (PCD)",
    "_ethnic_affiliation": "¿Cuál Etnia?",
    "_skills": "Selecciona tus habilidades",
    "_how_to_learn": "¿Cómo aprendes mejor?",
    "_weaknesses": "¿Cuáles son tus debilidades?",
    "_strengths": "¿Cuáles son tus fortalezas?",
    "_data_sharing":disclaimer_data_agreemet
}


def prepare_sheets_data(instance_data):
    utils = CategoryUtils()
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

@st.cache_data(ttl=900,show_spinner=False)
def send_to_sheets(data: List[List[str]]):
    try:
        sheet = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM','Sign Up')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos :orange-background[8 caracteres.]")
    if not re.search(r"[A-Z]", password):
        errors.append("La contraseña debe contener al menos :orange-background[una letra mayúscula.]")
    if not re.search(r"[a-z]", password):
        errors.append("La contraseña debe contener al menos :orange-background[una letra minúscula.]")
    if not re.search(r"\d", password):
        errors.append("La contraseña debe contener al menos :orange-background[un número.]")
    if not re.search(r"[!\_\-@#$%^&*(),.?\":{}|<>]", password):
        errors.append("La contraseña debe contener al menos :orange-background[un carácter especial.]")
    
    is_valid = len(errors) == 0
    
    if not is_valid:
        funny_example = "N@pol3on!"
        message = "\n".join(f":material/password_2_off: {error}" for error in errors)
        message += f"\n\n¿Qué tal si pruebas con algo como :orange[**Ejemplo**] :orange-background[{funny_example}]? :material/vpn_lock:"
    else:
        message = "La contraseña cumple con todos los requisitos."
    
    return is_valid, message

def warning_signup(hidden_data):
    st.info('Ya tienes una :blue-background[cuenta registrada] en nuestro sistema debido a que tu :blue-background[documento de identidad, correo electrónico o teléfono] ya está asociado a un usuario. :blue[**Aquí están los datos que encontramos**]', icon=":material/action_key:")

    del hidden_data['status']
    user_data = pd.DataFrame([hidden_data])
    st.dataframe(user_data,hide_index=True,use_container_width=True)
    st.warning("Por favor, :orange-background[verifica] si reconoces estos datos. Si necesitas ayuda, escribe a wearecircleup@gmail.com",icon=":material/conditions:")

def signup_submition(form):
    instance = Users(**form)
    is_user_auth = connector().signup_preauth(instance.email, instance.id_user, instance.phone_number)

    if is_user_auth['status'] != 'sigup_approved':
        warning_signup(is_user_auth)
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
        
        st.success(":material/handshake: **¡Bienvenido a Circle Up Community!**\n\n¡Registro exitoso! Se ha enviado un correo electrónico de confirmación a tu dirección. A partir de ahora puedes acceder e inscribirte a los cursos disponibles en nuestra plataforma. ¡Esperamos que disfrutes de esta experiencia de aprendizaje!")


def signup_firestore():
    user_responses = form_reponses()
    messages = []
    
    empty_fields = [field for field, value in user_responses.items() if not value]
    if empty_fields:
        messages.append(":material/pending: **Campos pendientes**")
        for field in empty_fields:
            field_label = FIELD_LABELS.get(f"_{field}", field.replace('_', ' ').title())
            if field == 'data_sharing':
                messages.append(f"Por favor, marca el campo :blue[{field_label}].")
            else:
                messages.append(f"Por favor, complete el campo :blue[**{field_label}**].")

    if not validate_email(user_responses['email']):
        messages.append(":material/unsubscribe: **Correo electrónico inválido**\n\nPor favor, ingrese una dirección de correo electrónico válida.")

    is_valid, password_message = validate_password(user_responses['password'])
    if not is_valid:
        messages.append(f":material/unsubscribe: **Contraseña inválida**\n\n{password_message}")
    
    return messages

def register_users():

    st.info("""
    :blue[**Importante**]
    • Todos los datos deben corresponder al participante.
    • Si es menor de edad, incluya los datos de su tutor legal al final del formulario.
    • De lo contrario, esa información se usará como contacto de emergencia.
    • Al completar este formulario, declaras que la información proporcionada es verdadera y precisa.
    """, icon=":material/fingerprint:")
    

    st.text_input(label="Nombre",placeholder="Napoleón",key="_first_name",help=st.session_state.form_definitions['_first_name'])
    st.text_input(label="Apellido",placeholder="Bonaparte",key="_last_name",help=st.session_state.form_definitions['_last_name']) 
    
    st.warning(":orange[**¡Doble check Email!**] Es tu llave para estar al día.", icon=":material/attach_email:")
    st.text_input(label="Correo Electronico",placeholder="napoleon.bonaparte@mail.com",key="_email",help=st.session_state.form_definitions['_email'])

    st.text_input(label="Contraseña",placeholder="eMp3r@D0r",type="password",key="_password",help=st.session_state.form_definitions['_password'])
    st.text_input(label="Direccion",placeholder="Av. Conquista # 1804",key="_address",help=st.session_state.form_definitions['_address'])
    
    st.warning(":orange[**¡Doble check!**] Un número correcto nos mantiene conectados", icon=":material/security_update_good:")
    st.text_input(label="Telefono Celular",placeholder="555-888-9999",key="_phone_number",help=st.session_state.form_definitions['_phone_number'])

    st.warning(":orange[**¡Doble check!**] Tu fecha de nacimiento nos ayuda a personalizar tu experiencia.", icon=":material/event:")
    st.date_input(label="Fecha Nacimiento", format="DD-MM-YYYY", value=dt.date(2000,1,1), min_value=dt.date(1940,1,1),max_value=dt.date(2020,12,31), key="_dob",help=st.session_state.form_definitions['_dob'])
    
    st.selectbox(label="Genero",index=0,options=st.session_state.gender,key="_gender",help=st.session_state.form_definitions['_gender'])
    st.selectbox(label="Nacionalidad",options=["Colombia","Otro país"],index=None,key="_nationality",help=st.session_state.form_definitions['_nationality'])
    st.selectbox(label="Tipo D.I.",index=1,options=st.session_state.id_user_list, key="_id_user_type",help=st.session_state.form_definitions['_id_user_type']) 
    st.text_input(label="Número Documento Identidad",placeholder="80000000",key="_id_user",help=st.session_state.form_definitions['_id_user'])
    st.selectbox(label="Nivel Educación",index=0,options=st.session_state.education_level,key="_education_level",help=st.session_state.form_definitions['_education_level'])
    st.multiselect(label="Temas Interes",options=st.session_state.topics_of_interest,placeholder="Choose an option",key="_topics_interest",help=st.session_state.form_definitions['_topics_interest'])
    st.multiselect(label="Discapacidad (PCD)",options=st.session_state.disabilities,placeholder="Choose an option",default='No Aplica',key="_disability",help=st.session_state.form_definitions['_disability'])
    st.multiselect(label="Selecciona tus habilidades", options=st.session_state.skills, placeholder="Choose an option", key="_skills",help=st.session_state.form_definitions['_skills'])
    st.multiselect(label="¿Cómo aprendes mejor?", options=st.session_state.how_to_learn, placeholder="Choose an option", key="_how_to_learn",help=st.session_state.form_definitions['_how_to_learn'])
    st.multiselect(label="¿Cuáles son tus debilidades?",options=st.session_state.weaknesses, placeholder="Choose an option", key="_weaknesses",help=st.session_state.form_definitions['_weaknesses'])
    st.multiselect(label="¿Cuáles son tus fortalezas?", options=st.session_state.strengths, placeholder="Choose an option", key="_strengths",help=st.session_state.form_definitions['_strengths'])
    st.selectbox(label="¿Pertences a alguna Etnia?",index=1,options=["Si","No"],key="_is_ethnic",help=st.session_state.form_definitions['_is_ethnic']) 
    st.selectbox(label="¿Cual Etnia?",index=3,options=st.session_state.ethnics,key="_ethnic_affiliation",help=st.session_state.form_definitions['_ethnic_affiliation']) 
    st.selectbox(label="Cuidad Residencia",options=municipios,index=None,key="_city_residence",help=st.session_state.form_definitions['_city_residence'])
    st.text_input(label="Nombre Contacto Emergencia/Tutor Legal",placeholder="Letizia Ramolino",key="_guardian_fullname",help=st.session_state.form_definitions['_guardian_fullname'])
    st.text_input(label="Parentesco",placeholder="Madre",key="_guardian_relationship",help=st.session_state.form_definitions['_guardian_relationship'])
    st.text_input(label="Telefono Emergencia/Tutor",placeholder="555-888-4444",key="_emergency_phone",help=st.session_state.form_definitions['_emergency_phone'])
    st.selectbox(label="Tipo D.I. Tutor",index=1,options=st.session_state.id_user_list,key="_guardian_id_type",help=st.session_state.form_definitions['_guardian_id_type'])
    st.text_input(label="D.I. Tutor Legal",placeholder="5000000",key="_guardian_id",help=st.session_state.form_definitions['_guardian_id'])
    st.checkbox(label=disclaimer_data_agreemet, key="_data_sharing")


def sing_up():
    st.html(html_banner)
    st.title(":material/touch_app: **Sign Up | Circle Up Community**")

    st.markdown('Si todavía no eres miembro de nuestra comunidad, te invitamos a unirte. ¡Regístrate y comienza a formar parte de la experiencia Circle Up Community!')
    roles = {'Admin':'Sentinel','Volunteer':'Nomads','Learner':'Crew','Log In | Circle Up':'Crew'}

    with st.form("register_form", clear_on_submit=False):
        st.write("Bienvenido a la comunidad, donde valoramos cada historia y experiencia única. Para formar parte de nuestra tribu, por favor completa los siguientes datos personales.")
        
        register_users()

        submitted = st.form_submit_button(':material/touch_app: Regístrate', type="primary", help='Registro | Tribus', use_container_width=True)

    if submitted:
        messages = signup_firestore()
        if messages:
            for message in messages:
                if message.startswith("Por favor"):
                    st.info(message,icon=":material/pending_actions:")
                elif message.startswith(":material/unsubscribe:") or message.startswith(":material/unsubscribe:"):
                    st.warning(message)
                else:
                    st.error(message)
        else:
            user_responces = form_reponses()
            if all(user_responces.values()):
                signup_submition(user_responces)

sing_up()
st.divider()
if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
    st.switch_page('app.py')

menu()
