import datetime
import streamlit as st
from menu import menu
import pandas as pd
from dataclasses import dataclass, asdict
from utils.body import (warning_empty_data,unauthenticate_login,
                        warning_profile_changes,succeed_update_profiles,
                        html_banner)
from utils.form_options import skills, how_to_learn
import json
from google.cloud import firestore
import time
import anthropic

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'updates_confirmation' not in st.session_state:
    st.session_state.updates_confirmation = False
    st.session_state.updates_request = True

@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

def update_users_profile():
    if st.session_state.user_auth.user_role == 'Volunteer':
        layout = st.columns([2,2])
        layout[0].text_input(label="Nombre",value=st.session_state.user_auth.first_name,key="_first_name",help=st.session_state.form_definitions['_first_name'])
        layout[1].text_input(label="Apellido",value=st.session_state.user_auth.last_name,key="_last_name",help=st.session_state.form_definitions['_last_name']) 
        layout[0].text_input(label="Correo Electronico",value=st.session_state.user_auth.email,key="_email",help=st.session_state.form_definitions['_email'])
        layout[1].text_input(label="Contraseña",value=st.session_state.user_auth.password,type="password",key="_password",help=st.session_state.form_definitions['_password'])
        layout[0].text_input(label="Direccion",value=st.session_state.user_auth.address,key="_address",help=st.session_state.form_definitions['_address'])
        layout[1].text_input(label="Telefono Celular",value=st.session_state.user_auth.phone_number,key="_phone_number",help=st.session_state.form_definitions['_phone_number'])
        layout[0].selectbox(label="Tipo D.I.", index=st.session_state.id_user_list.index(st.session_state.user_auth.id_user_type),options=st.session_state.id_user_list, key="_id_user_type",help=st.session_state.form_definitions['_id_user_type'],disabled=True) 
        layout[1].text_input(label="Número Documento Identidad",value=st.session_state.user_auth.id_user,key="_id_user",help=st.session_state.form_definitions['_id_user'],disabled=True) 
        layout[0].text_input(label="Cuidad Residencia",value=st.session_state.user_auth.city_residence,key="_city_residence",help=st.session_state.form_definitions['_city_residence'])
        layout[1].text_input(label="Nombre Tutor legal/Emergencia",value=st.session_state.user_auth.guardian_fullname,key="_guardian_fullname",help=st.session_state.form_definitions['_guardian_fullname'])
        layout[0].text_input(label="Parentesco",value=st.session_state.user_auth.guardian_relationship,key="_guardian_relationship",help=st.session_state.form_definitions['_guardian_relationship'])
        layout[1].text_input(label="Telefono Tutor/Emergencia",value=st.session_state.user_auth.emergency_phone,key="_emergency_phone",help=st.session_state.form_definitions['_emergency_phone'])
    else:
        layout = st.columns([2,2])
        layout[0].text_input(label="Nombre",value=st.session_state.user_auth.first_name,key="_first_name",help=st.session_state.form_definitions['_first_name'])
        layout[1].text_input(label="Apellido",value=st.session_state.user_auth.last_name,key="_last_name",help=st.session_state.form_definitions['_last_name']) 
        layout[0].text_input(label="Correo Electronico",value=st.session_state.user_auth.email,key="_email",help=st.session_state.form_definitions['_email'])
        layout[1].text_input(label="Contraseña",value=st.session_state.user_auth.password,type="password",key="_password",help=st.session_state.form_definitions['_password'])
        layout[0].text_input(label="Direccion",value=st.session_state.user_auth.address,key="_address",help=st.session_state.form_definitions['_address'])
        layout[1].text_input(label="Telefono Celular",value=st.session_state.user_auth.phone_number,key="_phone_number",help=st.session_state.form_definitions['_phone_number'])
        layout[0].selectbox(label="Tipo D.I.", index=st.session_state.id_user_list.index(st.session_state.user_auth.id_user_type),options=st.session_state.id_user_list, key="_id_user_type",help=st.session_state.form_definitions['_id_user_type'],disabled=True) 
        layout[1].text_input(label="Número Documento Identidad",value=st.session_state.user_auth.id_user,key="_id_user",help=st.session_state.form_definitions['_id_user'],disabled=True) 
        layout[0].text_input(label="Cuidad Residencia",value=st.session_state.user_auth.city_residence,key="_city_residence",help=st.session_state.form_definitions['_city_residence'])
        layout[1].text_input(label="Nombre Tutor legal/Emergencia",value=st.session_state.user_auth.guardian_fullname,key="_guardian_fullname",help=st.session_state.form_definitions['_guardian_fullname'])
        layout[0].text_input(label="Parentesco",value=st.session_state.user_auth.guardian_relationship,key="_guardian_relationship",help=st.session_state.form_definitions['_guardian_relationship'])
        layout[1].text_input(label="Telefono Tutor/Emergencia",value=st.session_state.user_auth.emergency_phone,key="_emergency_phone",help=st.session_state.form_definitions['_emergency_phone'])
        layout[0].multiselect(label="Selecciona tus habilidades",default=st.session_state.user_auth.skills,key="_skills",help=st.session_state.form_definitions['_skills'],options=skills)
        layout[1].multiselect(label="¿Cómo aprendes mejor?",default=st.session_state.user_auth.how_to_learn,key="_how_to_learn",help=st.session_state.form_definitions['_how_to_learn'],options=how_to_learn)

def profile_updates():
    profile_attributes = {
        'first_name':st.session_state._first_name, 
        'last_name':st.session_state._last_name,
        'email':st.session_state._email,
        'password':st.session_state._password,
        'address':st.session_state._address,
        'phone_number':st.session_state._phone_number,
        'id_user':st.session_state._id_user,
        'id_user_type':st.session_state._id_user_type,
        'city_residence':st.session_state._city_residence, 
        'guardian_fullname':st.session_state._guardian_fullname,
        'guardian_relationship':st.session_state._guardian_relationship,
        'emergency_phone':st.session_state._emergency_phone,
    }

    if st.session_state.user_auth.user_role == 'Learner':
        profile_attributes['skills'] = st.session_state._skills
        profile_attributes['how_to_learn'] = st.session_state._how_to_learn
    else: 
        profile_attributes = profile_attributes

    st.write(profile_attributes)

    if all(profile_attributes.values()):
        changes = st.session_state.user_auth.catch_profile_updates(**profile_attributes)
        warning_profile_changes(changes)
        if any([value[-1] for value in changes.values()]):
            st.session_state.updates_request = False
        
    else: warning_empty_data()    

def update_profile_changes():
    profile_attributes = {
        'first_name':st.session_state._first_name, 
        'last_name':st.session_state._last_name,
        'email':st.session_state._email,
        'password':st.session_state._password,
        'address':st.session_state._address,
        'phone_number':st.session_state._phone_number,
        'id_user':st.session_state._id_user,
        'id_user_type':st.session_state._id_user_type,
        'city_residence':st.session_state._city_residence, 
        'guardian_fullname':st.session_state._guardian_fullname,
        'guardian_relationship':st.session_state._guardian_relationship,
        'emergency_phone':st.session_state._emergency_phone,
    }

    if st.session_state.user_auth.user_role != 'Volunteer':
        profile_attributes = profile_attributes
    else: 
        profile_attributes['skills'] = st.session_state._skills
        profile_attributes['how_to_learn'] = st.session_state._how_to_learn

    st.session_state.user_auth.update_profile(**profile_attributes)
    st.session_state.user_auth.update_firestore_profile(firestore_client())
    st.session_state.updates_request = True
    succeed_update_profiles(st.session_state.user_auth.first_name.capitalize())

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu()

def form_update_profile():
    st.write('**Circle Up ⚫ Participación Activa**')
    update_users_profile()
    button_layout = st.columns([3,1,2])
    button_layout[0].button(label='Verificar Cambios',type="primary",on_click=profile_updates,disabled=st.session_state.updates_confirmation,use_container_width=True)
    button_layout[2].button(label='Guardar Cambios',type="primary",on_click=update_profile_changes,disabled=st.session_state.updates_request,use_container_width=True)

def accesse_granted():
    profile_warning = """
    :blue[**Mantén tu perfil al día para una experiencia óptima en Circle Up ⚫**]. Actualizar tu información es rápido y sencillo, 
    y asegura que recibas contenido y oportunidades acordes a tus intereses y necesidades actuales. Si tienes alguna pregunta o 
    necesitas asistencia, los **Sentinel** están siempre disponibles para ofrecerte su apoyo. ¡No dudes en actualizar tus datos o contactarnos!

    """
    st.markdown(profile_warning)
    st.subheader('Circle Up ⚫ Actualizar Perfil')
    with st.expander(f"**Perfil @{st.session_state.user_auth.first_name.capitalize()}** | Actualización de Información",expanded=True):
        form_update_profile()
    

def authenticated_login_crew():
    st.html(html_banner)
    st.subheader(f'¡Hola, @{st.session_state.user_auth.first_name.capitalize()}!')
    st.markdown(f"¿Sabías que perteneces a la tribu **{st.session_state.role_synonym}**? ¡Es genial tenerte con nosotros! Prepárate para sumergirte en un mundo de aprendizaje. ¡Vamos a aprender un montón juntos!")

    accesse_granted()

def authenticated_login_nomads():
    st.html(html_banner)
    st.subheader(f'¡Hola, @{st.session_state.user_auth.first_name.capitalize()}!')
    st.markdown(f"¿Sabías que perteneces a la tribu **{st.session_state.role_synonym}**? ¡Es genial tenerte con nosotros! Prepárate para sumergirte en un emocionante mundo de enseñanza y aprendizaje. ¡Juntos vamos a explorar y aprender mucho!")

    accesse_granted()

def authenticated_login_sentinel():
    st.html(html_banner)
    st.subheader(f'¡Hola, @{st.session_state.user_auth.first_name.capitalize()}!')
    st.markdown(f"¿Sabías que perteneces a la tribu **{st.session_state.role_synonym}**? ¡Es genial tenerte con nosotros! Prepárate para sumergirte en un emocionante mundo de enseñanza y aprendizaje. ¡Juntos vamos a explorar y aprender mucho!")

    accesse_granted()

try:
    if st.session_state.user_auth is not None and st.session_state.user_auth.user_status == 'Activo':
        if st.session_state.user_auth.user_role == 'Learner':
            authenticated_login_crew()
        elif st.session_state.user_auth.user_role == 'Volunteer':
            authenticated_login_nomads()
        elif st.session_state.user_auth.user_role == 'Admin':
            authenticated_login_sentinel()
    else: 
        unauthenticate_login(st.session_state.user_auth.user_role)
except:
    st.switch_page("app.py")