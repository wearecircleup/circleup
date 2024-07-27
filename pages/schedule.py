import streamlit as st
import pandas as pd
from menu import menu
from utils.body import unauthenticate_login
from google.cloud import firestore
import json
from classes.utils_class import CategoryUtils
from classes.spread_class import Sheets
from classes.firestore_class import Firestore
from datetime import datetime, date
from utils.body import succefull_enrollment
from typing import Dict, List
import time
import numpy as np
import altair as alt
from itertools import chain
from collections import Counter
from utils.form_options import age_range, topics_of_interest
from utils.body import enrollment_warning, warning_unenroll, unenrolled_confirm, html_banner

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

@st.cache_data
def get_course_data():
    Conn = connector()
    course_requests = Conn.query_collection('course_proposal', [('status', '==', 'Approved')])
    courses_data = [doc.data for doc in course_requests]
    dataset = pd.DataFrame(courses_data)
    dataset.rename(columns={'cloud_id':'cloud_id_course'},inplace=True)
    return dataset

@st.cache_data
def get_intake_data():
    Conn = connector()
    course_requests = Conn.query_collection('intake_collection',[('cloud_id_user', '==', st.session_state.user_auth.cloud_id),
                                                                ('status', '==', 'Enrrolled')])
    courses_data = [doc.data for doc in course_requests]
    dataset = pd.DataFrame(courses_data)
    return dataset

def lock_data(field):
    data_courses = get_course_data()
    users_enrollments = get_intake_data()
    enlistment = pd.merge(data_courses, users_enrollments, on=['cloud_id_course'], how='inner')
    
    categories = enlistment[field].str.split(',')
    flattened_categories = chain.from_iterable(categories)
    unique_categories = sorted(set(flattened_categories))

    return unique_categories


def course_description(course):
    st.info(f"¡{st.session_state.user_auth.first_name.capitalize()}! Aquí tienes los detalles del curso.\n :blue[**{course['course_name']}**]", icon=":material/dynamic_form:")
    
    st.write("A continuación, encontrarás toda la información que necesitas para decidir si es el adecuado para ti.")
    
    col1, col2 = st.columns([1,1])
    
    with col1:
        st.info(f":blue[**Objetivos Curso**] \n\n{course['course_objective']}", icon=":material/lightbulb:")

    with col2:
        st.success(f" :blue[**Perfil Voluntario**] \n\n{course['volunteer_profile']}", icon=":material/account_circle:")

    st.info(":blue[**Información General del Curso**] Esta información te ayudará a planificar tu participación y entender la estructura del curso",icon=":material/mitre:")

    general_data = {
        "Característica": ["Fecha de inicio", "Modalidad", "Mín. participantes", "Máx. participantes"],
        "Descripción": [
            course['start_date'],
            course['modality_proposal'],
            course['min_audience'],
            course['max_audience']
        ]
    }
    general_df = pd.DataFrame(general_data)
    st.dataframe(general_df.set_index('Característica'), use_container_width=True)

    st.info(":blue[**Categorías y Edades**] Pefecto cumples con los requisitos de edad. "
    "Echa un vistazo a las categorías para asegurarte de que se alinean con tus intereses", icon=":material/filter_list:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.multiselect('Categorías', options=course['course_categories'].split(','), default=course['course_categories'].split(','), disabled=True)
    with col2:
        st.multiselect('Edades Permitidas', options=course['allowed_age'].split(','), default=course['allowed_age'].split(','), disabled=True)

    st.info(":blue[**Detalles Adicionales**] Revisa estos detalles para asegurarte de que puedes cumplir con los requisitos y aprovechar al máximo esta oportunidad de aprendizaje", icon=":material/list_alt:")
    
    details_data = {
        "Característica": ["Ciudad", "Lugar", "Requisitos", "Recursos", "Conocimientos previos"],
        "Descripción": [
            course['city_proposal'],
            course['place_proposal'],
            course['devices_proposal'],
            course['tech_resources'],
            course['prior_knowledge']
        ]
    }
    details_df = pd.DataFrame(details_data)
    st.dataframe(details_df.set_index('Característica'), use_container_width=True)

    st.info("Esperamos que esta información te ayude a tomar una decisión informada. Si tienes alguna pregunta adicional, no dudes en contactarnos en gocircleup@gmail.com", icon=":material/mountain_flag:")
    st.success(":green[**Invierte en tu comunidad**] Este curso te cuesta :green[**$0.00**], pero su valor se mide en el impacto que generarás.", icon=":material/handshake:")

def get_uniques(df, field):
    return df[field].str.split(',', expand=True).stack().unique().tolist()

@st.cache_data(ttl=3600,show_spinner=False)
def send_to_sheets(data: List[List[str]]):
    try:
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Enrollment')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False
    
@st.cache_data(ttl=3600,show_spinner=False)
def send_to_firebase(data: Dict):
    try:
        intake_data = connector().add_document('intake_collection',data)
        return intake_data.id
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False

def enrollment_notice(data: Dict):
    cloud_id = send_to_firebase(data)
    data['cloud_id'] = cloud_id 
    sheet_entry = [list(data.values())]
    send_to_sheets(sheet_entry)
    st.rerun()

st.title("Explora Nuestros Cursos")
st.write("Bienvenido a nuestra plataforma de aprendizaje. Aquí podrás encontrar cursos diseñados para potenciar tus habilidades y conocimientos.")

data_courses = get_course_data()

lock_categories = lock_data('course_categories')
lock_courses = lock_data('course_name')

user_age = CategoryUtils().age_to_category(st.session_state.user_auth.dob)
all_age_options = get_uniques(data_courses, 'allowed_age')

age_appropriate = data_courses['allowed_age'].apply(lambda x: user_age in x.split(',')).any()

if age_appropriate:
    st.info("**Paso 1** Elige una Categoría",icon=":material/self_improvement:")
    category_options = get_uniques(data_courses, 'course_categories')
    selected_category = st.selectbox(
        "Explora nuestras categorías y elige la que más te interese",
        options=category_options,
        index=None,
        placeholder='Seleccionar Categoría'
    )

    if selected_category:
        st.write("Ahora que has elegido una categoría, explora los cursos disponibles. Cada curso ha sido diseñado para ofrecerte una experiencia de aprendizaje interesante.")
        st.info("**Paso 2** Seleccionar Curso",icon=":material/self_improvement:")
        filtered_courses = data_courses[data_courses['course_categories'].str.contains(selected_category)]
        course_options = filtered_courses['course_name'].tolist()
        selected_course = st.selectbox(
            "Ahora, echa un vistazo a los cursos disponibles en esta categoría:",
            options=course_options,
            index=None,
            placeholder='Seleccionar Curso'
        )

        if selected_course:
            selected_request = filtered_courses[filtered_courses['course_name'] == selected_course].iloc[0]
            if selected_course not in lock_courses:
                if not selected_request.empty:
                    st.write("Aquí tienes toda la información detallada sobre el curso seleccionado. Revisa cuidadosamente los objetivos, el perfil del instructor y los requisitos para asegurarte de que este curso sea el adecuado para ti.")
                    course_description(selected_request)

                    utils = CategoryUtils()

                    reminder = f"""El curso de {selected_request['course_name']} {'será en modalidad ' + selected_request['modality_proposal'].lower() if selected_request['modality_proposal'].lower() == 'virtual' else f'se realizará en {selected_request['place_proposal']}, {selected_request['city_proposal']}'}. Está diseñado para participantes de {selected_request['allowed_age']} años{f' y es recomendable que cuentes con {selected_request['prior_knowledge'].lower()}' if selected_request['prior_knowledge'].lower() != 'no aplica' else ''}. Seremos un grupo de {selected_request['min_audience']} a {selected_request['max_audience']} personas{f', así que no olvides {selected_request['tech_resources'].lower()}' if selected_request['tech_resources'].lower() != 'no aplica' else ''}. Este curso se encuentra dentro de las categorías de {selected_request['course_categories']}."""

                    data_collection = {
                        'enrolled_at':utils.get_current_date(),
                        'week':utils.date_to_day_of_week(),
                        'hour_range':utils.time_to_category(),
                        'cloud_id':None,
                        'cloud_id_user':st.session_state.user_auth.cloud_id,
                        'cloud_id_volunteer':selected_request['cloud_id_volunteer'],
                        'cloud_id_course':selected_request['cloud_id_course'],
                        'first_name':selected_request['first_name'],
                        'last_name':selected_request['last_name'],
                        'email':selected_request['email'],
                        'start_date':selected_request['start_date'],
                        'summary': reminder,
                        'attendance_record':0,
                        'email_notice':'Pending',
                        'email_reminder':0,
                        'status':'Enrrolled',
                        'last_change':utils.get_current_date()
                    }
                    
                    st.write(reminder)
                    cols = st.columns([2,1])
                    with cols[0]:
                        if st.button('Registrarse',use_container_width=True):
                            enrollment_notice(data_collection)
                    with cols[1]:
                        if st.button('Confirmar',type='primary',use_container_width=True):
                            pass
            else:
                st.error(f"Ya estás en el curso :red[**{selected_course}**]. En :red[**Circle Up Community**] hay otras opciones más interesantes para ti.", icon=":material/concierge:")
        else:
            st.info("Selecciona un curso para ver más detalles. Cada curso ha sido cuidadosamente diseñado para ofrecerte una experiencia de aprendizaje enriquecedora.", icon=":material/library_books:")
    else:
        st.info("Explora nuestras categorías para encontrar el tema que más te apasione. Tenemos una amplia gama de opciones para satisfacer diversos intereses y niveles de experiencia.", icon=":material/explore:")
else:
    st.warning("Por el momento no tenemos cursos disponibles para tu rango de edad, pero no te preocupes. Estamos trabajando constantemente para ampliar nuestra oferta. Te avisaremos tan pronto como tengamos opciones adecuadas para ti.", icon=":material/notifications:")


menu()