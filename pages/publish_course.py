import streamlit as st
from menu import menu
import pandas as pd
import json
from utils.body import warning_empty_data,succeed_proposal, warning_reupload,html_banner
from utils.form_options import age_range,topics_of_interest, places, cities,modality,agreement_options,duration_options,consent_items

from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter, Or
from dataclasses import dataclass, asdict
from classes.course_class import Course
from classes.utils_class import CategoryUtils
from classes.spread_class import Sheets
from classes.firestore_class import Firestore
from datetime import datetime
from typing import List
import time

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CategoryUtils().markdown_design(), unsafe_allow_html=True)

if 'enable_form' not in st.session_state:
    st.session_state.enable_form = True

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

def prepare_data(instance_data):
    """
    Prepara los datos específicos para enviar a Google Sheets.
    """
    utils = CategoryUtils()

    return [
        utils.get_current_date(),
        utils.date_to_day_of_week(),
        utils.time_to_category(),
        st.session_state.user_auth.first_name,
        st.session_state.user_auth.last_name,
        st.session_state.user_auth.gender,
        utils.age_to_category(st.session_state.user_auth.dob),
        st.session_state.user_auth.email,
        st.session_state.user_auth.id_user_type,
        st.session_state.user_auth.id_user,
        st.session_state.user_auth.gender,
        st.session_state.user_auth.phone_number,
        st.session_state.user_auth.user_role,
        st.session_state.user_auth.city_residence,
        instance_data.get('check_structure_form', False),
        instance_data.get('check_development_form', False),
        instance_data.get('check_material_form', False),
        instance_data.get('check_proposal_form', False),
        instance_data.get('modality_form', ''),
        instance_data.get('min_audience_form', 10),
        ', '.join(instance_data.get('age_range_form', [])),
        instance_data.get('max_audience_form', 10),
        st.session_state.city_form,
        st.session_state.place_form,
        instance_data.get('start_date_form', '').strftime('%d-%m-%Y'),
        instance_data.get('volunteer_consent_form', ''),
        instance_data.get('devices_form', ''),
        instance_data.get('tech_resources_form', ''),
        instance_data.get('prior_knowledge_form', ''),
        ', '.join(instance_data.get('course_categories_form', [])),
        instance_data.get('course_name_form', ''),
        instance_data.get('course_objective_form', ''),
        instance_data.get('presentation_link_form', ''),
        instance_data.get('course_duration_form', ''),
        instance_data.get('volunteer_profile_form', ''),
        instance_data.get('consent_0_form', False),
        instance_data.get('consent_1_form', False),
        instance_data.get('consent_2_form', False),
        instance_data.get('consent_3_form', False),
        instance_data.get('consent_4_form', False),
        instance_data.get('consent_5_form', False),
        instance_data.get('consent_6_form', False),
        instance_data.get('consent_7_form', False),
        instance_data.get('consent_8_form', False),
        instance_data.get('consent_9_form', False),
        instance_data.get('consent_10_form', False),
        instance_data.get('consent_11_form', False),
        instance_data.get('consent_12_form', False)
    ]


def prepare_collection(instance_data):
    """
    Prepara los datos específicos para enviar a Google Sheets.
    """
    utils = CategoryUtils()

    return {
        'publication':utils.get_current_date(),
        'cloud_id_volunteer':st.session_state.user_auth.cloud_id,
        'cloud_id':None,
        'modality':instance_data.get('modality_form', ''),
        'min_audience':instance_data.get('min_audience_form', 10),
        'age_range':', '.join(instance_data.get('age_range_form', [])),
        'max_audience':instance_data.get('max_audience_form', 10),
        'city':st.session_state.city_form,
        'place':st.session_state.place_form,
        'start_date':instance_data.get('start_date_form', '').strftime('%d-%m-%Y'),
        'devices':instance_data.get('devices_form', ''),
        'tech_resources':instance_data.get('tech_resources_form', ''),
        'prior_knowledge':instance_data.get('prior_knowledge_form', ''),
        'course_categories':', '.join(instance_data.get('course_categories_form', [])),
        'course_name':instance_data.get('course_name_form', ''),
        'course_objective':instance_data.get('course_objective_form', ''),
        'volunteer_profile':instance_data.get('volunteer_profile_form', '')
    }

@st.cache_data(ttl=3600,show_spinner=False)
def send_to_sheets(data: List[List[str]]):
    try:
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Agreement Letter')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False


def main():
    st.title("Módulo Final: Preparación para el Lanzamiento del Curso")

    st.write("""
    Bienvenido al módulo final de preparación para el lanzamiento de su curso. 
    En esta etapa crucial, nos aseguraremos de que todos los elementos estén en su lugar 
    para garantizar una experiencia educativa exitosa y enriquecedora.
    """)

    with st.form("curso_form"):
        st.title("1. Confirmación de Circle Up Community")
        st.info("Circle Up Community ha revisado y está de acuerdo con los siguientes elementos")

        col1, col2 = st.columns(2)

        with col1:
            check_structure = st.checkbox("Estructura del Curso Completa", key="check_structure_form")
            check_development = st.checkbox("Contenido General Revisado/Ajustado", key="check_development_form")

        with col2:
            check_material = st.checkbox("Presentación Revisada/Ajustada", key="check_material_form")
            check_proposal = st.checkbox("Carta Propuesta Voluntario", key="check_proposal_form")

        st.title("2 Aspectos Logísticos")
        st.info("Por favor, confirme los siguientes elementos para finalizar la configuración del curso")

        col1, col2 = st.columns(2)
        with col1:
            selected_modality = st.selectbox("Modalidad Curso", modality, index=None, key="modality_form")
            min_audience = st.number_input("Audiencia Mínima", min_value=10, step=1,max_value=10, key="min_audience_form")

        with col2:
            selected_age_ranges = st.multiselect("Perfil Demográfico", age_range, key="age_range_form")
            max_audience = st.number_input("Audiencia Máxima", min_value=10, step=1, max_value=30, key="max_audience_form")

        if selected_modality in ['Presencial']:
            with col1:
                selected_city = st.selectbox("Ciudad Presentación", cities, index=None, key="city_form")
            with col2:
                selected_place = st.selectbox("Espacio Presentación", places, index=None, key="place_form")
        
        with col1:
            start_date = st.date_input("Fecha Inicio", min_value=datetime.now().date(), key="start_date_form", format="DD-MM-YYYY")
        with col2:
            agreement = st.selectbox("Consentimiento Voluntario", options=agreement_options, index=None, key="volunteer_consent_form")

        st.title("3. Requisitos de Participación")
        st.info("Especifique claramente los requisitos mínimos para los participantes")

        devices = st.text_input(
            "Dispositivos necesarios",
            placeholder="Ej: computadora portátil, teléfono inteligente",
            key="devices_form"
        )

        tech_resources = st.text_input(
            "Recursos técnicos requeridos",
            placeholder="Ej: conexión a Internet, datos móviles",
            key="tech_resources_form"
        )

        prior_knowledge = st.text_input(
            "Conocimientos previos o habilidades necesarias (opcionales)",
            placeholder="Ej: nociones básicas de programación",
            key="prior_knowledge_form"
        )

        categories = st.multiselect(
            "Categoría a la que pertenece el curso",
            options=topics_of_interest, 
            key="course_categories_form"
        )

        st.title("4. Información General del Curso")
        st.info("Por favor, complete la siguiente información general sobre el curso")

        course_name = st.text_input(
            "Nombre del Curso",
            placeholder="Ej: Introducción a la Inteligencia Artificial",
            key="course_name_form"
        )

        course_objective = st.text_area(
            "Objetivo Curso",
            placeholder="Describa brevemente el objetivo principal del curso",
            key="course_objective_form"
        )

        presentation_link = st.text_input(
            "Link Presentación",
            placeholder="docs.google.com/presentation/",
            key="presentation_link_form"
        )

        course_duration = st.selectbox(
            "Duración Curso",
            options=duration_options, index=0,
            key="course_duration_form"
        )

        volunteer_profile = st.text_area(
            "Perfil Profesional Anónimo",
            placeholder="Experiencia academica/profesional del voluntari@.",
            key="volunteer_profile_form"
        )

        st.title("5. Consentimiento General")
        st.info("El voluntario debe leer detenidamente y aceptar los siguientes términos y condiciones")

        consent_checks = [st.checkbox(item, key=f"consent_{i}_form") for i, item in enumerate(consent_items)]

        submitted = st.form_submit_button("Finalizar y Guardar",use_container_width=True,type='primary')

    if submitted:
        missing_fields = []

        # Verificar campos de la sección 1
        if not st.session_state.check_structure_form:
            missing_fields.append("Estructura del Curso Completa")
        if not st.session_state.check_development_form:
            missing_fields.append("Contenido General Revisado/Ajustado")
        if not st.session_state.check_material_form:
            missing_fields.append("Presentación Revisada/Ajustada")
        if not st.session_state.check_proposal_form:
            missing_fields.append("Carta Propuesta Voluntario")

        # Verificar campos de la sección 2
        if not st.session_state.modality_form:
            missing_fields.append("Modalidad Curso")
        if not st.session_state.age_range_form:
            missing_fields.append("Perfil Demográfico")
        if st.session_state.modality_form == 'Presencial':
            if not st.session_state.city_form:
                missing_fields.append("Ciudad Presentación")
            if not st.session_state.place_form:
                missing_fields.append("Espacio Presentación")
        if not st.session_state.start_date_form:
            missing_fields.append("Fecha Inicio")
        if not st.session_state.volunteer_consent_form:
            missing_fields.append("Consentimiento Voluntario")

        # Verificar campos de la sección 3
        if not st.session_state.devices_form:
            missing_fields.append("Dispositivos necesarios")
        if not st.session_state.tech_resources_form:
            missing_fields.append("Recursos técnicos requeridos")
        if not st.session_state.course_categories_form:
            missing_fields.append("Categoría a la que pertenece el curso")

        # Verificar campos de la sección 4
        if not st.session_state.course_name_form:
            missing_fields.append("Nombre del Curso")
        if not st.session_state.course_objective_form:
            missing_fields.append("Objetivo Curso")
        if not st.session_state.presentation_link_form:
            missing_fields.append("Link Presentación")
        if not st.session_state.volunteer_profile_form:
            missing_fields.append("Perfil Profesional Anónimo")

        # Verificar consentimientos de la sección 5
        for i in range(len(consent_items)):
            if not st.session_state[f"consent_{i}_form"]:
                missing_fields.append(f"Consentimiento {i+1}")

        if missing_fields:
            st.error(f"Por favor, complete los siguientes campos: {', '.join(missing_fields)}")
        else:
            volunteer_data = {key: value for key, value in st.session_state.items() if key.endswith("_form")}
            st.success("Todos los campos han sido completados correctamente.")

            collection_data = prepare_collection(volunteer_data)
            connector().add_document('course_preapproved',collection_data)

            sheets_data = prepare_data(volunteer_data)
            send_to_sheets([sheets_data])
            
            st.success(
                """
                ¡Felicidades! 🎉

                En Circle Up Community, valoramos tu participación y esfuerzo.
                
                Gracias por ser parte de este emocionante proceso de co-creación.
                Tu contribución es fundamental para nuestro éxito colectivo.
                
                **¡Todos los créditos son tuyos!** 🏆
                
                Continúa así y sigamos construyendo juntos.
                """
            )

            st.balloons()

            time.sleep(3)
            st.session_state.enable_form = False

    return None

if st.session_state.enable_form:
    main()
else:
    st.title("Módulo Final: Preparación para el Lanzamiento del Curso")

    st.write("""
    Bienvenido al módulo final de preparación para el lanzamiento de su curso. 
    En esta etapa crucial, nos aseguraremos de que todos los elementos estén en su lugar 
    para garantizar una experiencia educativa exitosa y enriquecedora.
    """)

    st.title("1. Confirmación de Circle Up Community")
    st.info("Circle Up Community ha revisado y está de acuerdo con los siguientes elementos")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.")

    st.title("2 Aspectos Logísticos")
    st.info("Por favor, confirme los siguientes elementos para finalizar la configuración del curso")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.")
    
    st.title("3. Requisitos de Participación")
    st.info("Especifique claramente los requisitos mínimos para los participantes")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.")

    st.title("4. Información General del Curso")
    st.info("Por favor, complete la siguiente información general sobre el curso")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.")

    st.title("5. Consentimiento General")
    st.info("El voluntario debe leer detenidamente y aceptar los siguientes términos y condiciones")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.")

    st.info("""
    **Último paso: Firma del documento**
    ¡Estamos tan emocionados como tú por la publicación!

    Enviar el documento es súper fácil y rápido. 
    En solo unos clics estarás listo para comenzar. 
    """)
    
    st.success("""
    Gracias por ser parte de este proceso de co-creación.
    Tu contribución es fundamental para nuestro éxito colectivo.
    """)

menu()



