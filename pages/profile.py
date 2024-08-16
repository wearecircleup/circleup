import streamlit as st

st.set_page_config(
    page_title="Circle Up Community",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from typing import Dict, List, Tuple, Any
import json
import re
from google.cloud import firestore
from dataclasses import asdict

from menu import menu
from utils.body import (
    warning_empty_data, unauthenticate_login,
    warning_profile_changes, succeed_update_profiles,
    html_banner
)
from utils.form_options import skills, how_to_learn,weaknesses,strengths
from classes.firestore_class import Firestore
from classes.utils_class import CategoryUtils
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


def initialize_session_state() -> None:
    """Initialize session state variables."""
    st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
    st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)
    
    if 'page_selected' not in st.session_state:
        st.session_state.page_selected = None
    if 'updates_confirmation' not in st.session_state:
        st.session_state.updates_confirmation = False
        st.session_state.updates_request = True

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password against security criteria."""
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

def update_users_profile() -> None:
    """Display and handle user profile update form."""
    layout = st.columns([2,2])
    layout[0].text_input(label="Nombre", value=st.session_state.user_auth.first_name, key="_first_name", help=st.session_state.form_definitions['_first_name'])
    layout[1].text_input(label="Apellido", value=st.session_state.user_auth.last_name, key="_last_name", help=st.session_state.form_definitions['_last_name'])
    layout[0].text_input(label="Correo Electronico", value=st.session_state.user_auth.email, key="_email", help=st.session_state.form_definitions['_email'])
    
    new_password = layout[1].text_input(label="Contraseña", value="", type="password", key="_new_password", help="Ingrese su contraseña si desea cambiarla. Déjela en blanco para mantener la actual.")
    if new_password:
        is_valid, message = validate_password(new_password)
        if not is_valid:
            layout[1].error(message)
        else:
            layout[1].success(":material/check: " + message)
            st.session_state._password = new_password
    else:
        st.session_state._password = st.session_state.user_auth.password

    layout[0].text_input(label="Direccion", value=st.session_state.user_auth.address, key="_address", help=st.session_state.form_definitions['_address'])
    layout[1].text_input(label="Telefono Celular", value=st.session_state.user_auth.phone_number, key="_phone_number", help=st.session_state.form_definitions['_phone_number'])
    layout[0].selectbox(label="Tipo D.I.", index=st.session_state.id_user_list.index(st.session_state.user_auth.id_user_type), options=st.session_state.id_user_list, key="_id_user_type", help=st.session_state.form_definitions['_id_user_type'], disabled=True) 
    layout[1].text_input(label="Número Documento Identidad", value=st.session_state.user_auth.id_user, key="_id_user", help=st.session_state.form_definitions['_id_user'], disabled=True) 
    layout[0].text_input(label="Cuidad Residencia", value=st.session_state.user_auth.city_residence, key="_city_residence", help=st.session_state.form_definitions['_city_residence'])
    layout[1].text_input(label="Nombre Tutor legal/Emergencia", value=st.session_state.user_auth.guardian_fullname, key="_guardian_fullname", help=st.session_state.form_definitions['_guardian_fullname'])
    layout[0].text_input(label="Parentesco", value=st.session_state.user_auth.guardian_relationship, key="_guardian_relationship", help=st.session_state.form_definitions['_guardian_relationship'])
    layout[1].text_input(label="Telefono Tutor/Emergencia", value=st.session_state.user_auth.emergency_phone, key="_emergency_phone", help=st.session_state.form_definitions['_emergency_phone'])
    layout[0].multiselect(label="¿Cuáles son tus habilidades?", default=st.session_state.user_auth.skills, key="_skills", help=st.session_state.form_definitions['_skills'], options=skills)
    layout[1].multiselect(label="¿Cómo aprendes mejor?", default=st.session_state.user_auth.how_to_learn, key="_how_to_learn", help=st.session_state.form_definitions['_how_to_learn'], options=how_to_learn)
    layout[0].multiselect(label="¿Cuáles son tus debilidades?", default=st.session_state.user_auth.weaknesses, options=weaknesses, placeholder="Choose an option", key="_weaknesses", help=st.session_state.form_definitions['_weaknesses'])
    layout[1].multiselect(label="¿Cuáles son tus fortalezas?", default=st.session_state.user_auth.strengths, options=strengths, placeholder="Choose an option", key="_strengths", help=st.session_state.form_definitions['_strengths'])

def profile_updates() -> None:
    """Validate and process profile updates."""
    profile_attributes = {
        'first_name': st.session_state._first_name, 
        'last_name': st.session_state._last_name,
        'email': st.session_state._email,
        'password': st.session_state._password,
        'address': st.session_state._address,
        'phone_number': st.session_state._phone_number,
        'id_user': st.session_state._id_user,
        'id_user_type': st.session_state._id_user_type,
        'city_residence': st.session_state._city_residence, 
        'guardian_fullname': st.session_state._guardian_fullname,
        'guardian_relationship': st.session_state._guardian_relationship,
        'emergency_phone': st.session_state._emergency_phone,
        'skills': st.session_state._skills,
        'how_to_learn': st.session_state._how_to_learn,
        'weaknesses': st.session_state._weaknesses,
        'strengths': st.session_state._strengths,
    }

    if all(profile_attributes.values()):
        changes = st.session_state.user_auth.catch_profile_updates(**profile_attributes)
        warning_profile_changes(changes)
        if any([value[-1] for value in changes.values()]):
            st.session_state.updates_request = False
    else: 
        warning_empty_data()    

def update_profile_changes() -> None:
    """Update user profile in the database."""
    profile_attributes = {
        'first_name': st.session_state._first_name, 
        'last_name': st.session_state._last_name,
        'email': st.session_state._email,
        'password': st.session_state._password,
        'address': st.session_state._address,
        'phone_number': st.session_state._phone_number,
        'id_user': st.session_state._id_user,
        'id_user_type': st.session_state._id_user_type,
        'city_residence': st.session_state._city_residence, 
        'guardian_fullname': st.session_state._guardian_fullname,
        'guardian_relationship': st.session_state._guardian_relationship,
        'emergency_phone': st.session_state._emergency_phone,
        'skills': st.session_state._skills,
        'how_to_learn': st.session_state._how_to_learn,
        'weaknesses': st.session_state._weaknesses,
        'strengths': st.session_state._strengths,
    }

    st.session_state.user_auth.update_profile(**profile_attributes)
    data = asdict(st.session_state.user_auth)
    cloud_id = st.session_state.user_auth.cloud_id
    connector().update_document('users_collection', cloud_id, data)
    st.session_state.updates_request = True
    succeed_update_profiles(st.session_state.user_auth.first_name.capitalize())

def form_update_profile() -> None:
    """Display profile update form and handle button actions."""
    update_users_profile()
    button_layout = st.columns([3,1,2])
    button_layout[0].button(label='Verificar Cambios', type="primary", on_click=profile_updates, disabled=st.session_state.updates_confirmation, use_container_width=True)
    button_layout[2].button(label='Guardar Cambios', type="primary", on_click=update_profile_changes, disabled=st.session_state.updates_request, use_container_width=True)

def access_granted() -> None:
    """Display profile update page for authenticated users."""
    profile_warning = """
    Actualizar tu información es rápido y sencillo, 
    y asegura que recibas contenido y oportunidades acordes a tus intereses y necesidades actuales. Si tienes alguna pregunta o 
    necesitas asistencia, los **Sentinel** están siempre disponibles para ofrecerte su apoyo. ¡No dudes en actualizar tus datos o contactarnos!
    """
    st.info(f"Mantén tu perfil al día para una experiencia óptima en **Circle Up Community**", icon=":material/done_all:")
    st.markdown(profile_warning)
    st.title(f"Actualización de Información")
    form_update_profile()

def main() -> None:
    """Run the main Streamlit application."""
    initialize_session_state()
    menu()

    try:
        if st.session_state.user_auth is not None and st.session_state.user_auth.user_status == 'Activo':
            st.subheader(f'¡Hola, {st.session_state.user_auth.first_name.capitalize()}!')
            access_granted()

            st.divider()
            if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
                st.switch_page('app.py')
            st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
        else:
            unauthenticate_login(st.session_state.user_auth.user_role)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.switch_page("app.py")

if __name__ == "__main__":
    main()