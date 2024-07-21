import json
import streamlit as st
from menu import menu
import pandas as pd
from utils.body import (html_banner)
from google.cloud import firestore
from classes.firestore_class import Firestore
from utils.form_options import careers, volunteer_level
from typing import Dict, Any, List, Optional

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .stTextInput, .stSelectbox {
        max-width: 100%;
    }
    p, .stMarkdown {
        font-size: 14px;
    }
    h1 {
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

@st.cache_data
def status_user():
    firestore = Firestore(firestore_client())
    doc_id = st.session_state.user_auth.cloud_id
    if firestore.document_exists("volunteer_request", doc_id):
        return True
    
if 'status_request' not in st.session_state:
    st.session_state.status_request = False or status_user()

menu()

if status_user():
    st.session_state.status_request = True
    st.warning("Ya has enviado una solicitud de voluntariado. Tu solicitud está pendiente de validación. Por favor, está atento a tu email para más información.")


st.title("¿Te interesaría participar como voluntario?")

st.markdown("""
En CircleUp creemos que con tu experiencia académica o profesional puedes aportar a la sociedad. 
Sabemos que como experto en lo que haces no siempre hay suficiente tiempo, así que solo tienes que donar el 1% 
, equivalente a 4 horas mensuales :blue[cuando quieras, sin compromisos].

Además, si bien quieres enseñar algo que te apasiona, entendemos que es difícil contar con tiempo para crear 
material de apoyo. Tú solo nos dices qué quieres enseñar y nosotros te ayudamos a construir el material.

El pensamiento crítico, resolución de problemas y liderazgo son 
exactamente lo que queremos transmitir a la comunidad. No se trata solo de explicar conceptos, sino de compartir cómo, a través de tu experiencia profesional, 
has logrado resolver problemas complejos. Es sobre cómo el pensamiento crítico y el liderazgo, 
habilidades que quizás no tenías antes, han transformado tu perspectiva.

Desconocemos los desafíos que enfrentaremos en 5 años, pero podemos preparar a las próximas generaciones 
para que sean expertos en adaptarse y resolver problemas. Si la próxima generación no quiere resolver problemas entonces, todo el conocimiento acumulado solo habrá beneficiado a unos pocos.

Únete a nosotros para construir un futuro donde la adaptabilidad y el pensamiento crítico sean la 
norma. Tu aporte hoy puede ser la solución que alguien necesite mañana. ¿Listo para ser parte del cambio?            
""")

st.title("Formulario de Voluntarios")

st.markdown("""
Este formulario es el primer paso como voluntario en Circle Up. 
Está diseñado para profesionales de **25 años** en adelante que deseen compartir su experiencia.
""")

def validate_form():
    for key in st.session_state:
        if key.startswith('volunteer_') and not st.session_state[key]:
            return False
    return True

def validate_user_status():
    return (st.session_state.user_auth.user_status != 'Inactive' and 
            st.session_state.user_auth.user_role == "Learner")

with st.form("volunteer_form"):
    age = st.selectbox("Edad",options=[
        "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60+"
    ], key="volunteer_age",index=None)
    
    education = st.selectbox("Nivel educativo completado",options=volunteer_level, key="volunteer_education",index=None)
    profession_category = st.selectbox("Categoría profesional",options=careers, key="volunteer_profession_category",index=None)
    experience = st.number_input("Años de experiencia profesional", min_value=1, max_value=50, key="volunteer_experience")
    
    availability = st.multiselect("Tipo de voluntariado", ["Virtual", "Presencial", "Ambos"], key="volunteer_availability")
    
    time_availability = st.selectbox("Disponibilidad de tiempo", options=[
        "Inmediata",
        "En 1-2 semanas",
        "En 3-4 semanas"
    ], key="volunteer_time_availability",index=None)
    
    commitment = st.slider("Horas que puedes donar al mes", min_value=4, max_value=8, step=1, key="volunteer_commitment",value=4)
    motivation = st.text_area("¿Por qué quieres ser parte de Circle Up?", key="volunteer_motivation", max_chars=300)
    
    submit_button = st.form_submit_button("Enviar Aplicación",use_container_width=True,type='primary',disabled=st.session_state.status_request)

if submit_button:
    if validate_form() and validate_user_status():
        volunteer_data = {
            "age": st.session_state.volunteer_age,
            "education": st.session_state.volunteer_education,
            "profession_category": st.session_state.volunteer_profession_category,
            "experience": st.session_state.volunteer_experience,
            "availability": st.session_state.volunteer_availability,
            "time_availability": st.session_state.volunteer_time_availability,
            "commitment": st.session_state.volunteer_commitment,
            "motivation": st.session_state.volunteer_motivation,
            "first_name": st.session_state.user_auth.first_name,
            "last_name": st.session_state.user_auth.last_name,
            "email": st.session_state.user_auth.email,
            "cloud_id": st.session_state.user_auth.cloud_id,
            "user_status": st.session_state.user_auth.user_status,
            "user_role": st.session_state.user_auth.user_role,
            "status":'Pending',
            "notification":"Pending"
        }

        try:
            firestore = Firestore(firestore_client())
            doc_id = st.session_state.user_auth.cloud_id
            
            if firestore.document_exists("volunteer_request", doc_id):
                st.session_state.status_request = True
                st.warning("Ya has enviado una solicitud de voluntariado. Tu solicitud está pendiente de validación. Por favor, está atento a tu email para más información.")
            else:
                doc = firestore.add_document("volunteer_request", volunteer_data, doc_id)
                st.success("¡Gracias por tu aplicación! Hemos recibido tu información y la evaluaremos pronto.")
                st.info("Si tu aplicación es aprobada, recibirás un email con los siguientes pasos.")
        except ValueError as ve:
            st.warning(str(ve))
        except Exception as e:
            st.error(f"Hubo un error al procesar tu solicitud: {str(e)}")
    else:
        if not validate_user_status():
            st.error("Lo sentimos, solo los usuarios activos con rol de Learner pueden enviar este formulario.")
        else:
            st.error("Por favor, completa todos los campos del formulario antes de enviar.")

