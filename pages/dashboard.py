import streamlit as st

st.set_page_config(
    page_title="Circle Up Community",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import json
from typing import List, Dict, Any, Optional
from google.cloud import firestore
import pandas as pd
import time
import altair as alt
from datetime import datetime, timedelta
import math
import random
import string

from menu import menu
from classes.firestore_class import Firestore
from classes.utils_class import CategoryUtils
from classes.spread_class import Sheets
from classes.blobs_class import GoogleBlobs
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)


if 'page_selected' not in st.session_state:
    st.session_state.page_selected = None

if 'user_auth' not in st.session_state:
    st.session_state.user_auth = None

if 'finalize_course' not in st.session_state:
    st.session_state.finalize_course = ('¿Estás list@ para dar por finalizado el curso?', 'info')

def clear_names():
    column_rename_map = {
        'first_name': 'Nombre',
        'last_name': 'Apellido',
        'gender': 'Género',
        'nationality': 'Nacionalidad',
        'is_ethnic': '¿Etnia?',
        'city_residence': 'Ciudad',
        'guardian_fullname': 'Contacto Emergencia',
        'guardian_relationship': 'Parentesco',
        'emergency_phone': 'Tel. Emergencia',
        'education_level': 'Nivel Educativo',
        'user_role': 'Rol',
        'strengths': 'Fortalezas',
        'weaknesses': 'Áreas de Mejora',
        'disability': 'Div. Funcional',
        'ethnic_affiliation': 'Grupo Étnico',
        'skills': 'Habilidades',
        'how_to_learn': 'Estilo Aprendizaje',
        'email':'Email'
    }
    return column_rename_map

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn


@st.cache_data(ttl=300, show_spinner=False)
def update_sheets_proposal(cloud_id):
    last_update = CategoryUtils().get_current_date()
    updates = {'status': 'Finalized', 'updated_at':last_update,'image_course':st.session_state.sign_document}
    try:
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
        sheet.replace_values(cloud_id, updates)
        return True
    except Exception as e:
        return False

@st.cache_data(ttl=300, show_spinner=False)
def update_firebase_proposal(cloud_id):
    last_update = CategoryUtils().get_current_date()
    updates = {'status': 'Finalized', 'updated_at':last_update}
    try:
        connector().update_document('course_proposal', cloud_id, updates)
        return True
    except Exception as e:
        
        return False

@st.cache_data(ttl=900, show_spinner=False)
def add_firebase(data: Dict):
    try:
        token_collection = connector().add_document('tokens_storage',data,data['cloud_id'])
        return True
    except Exception as e:
        return False

@st.cache_data(ttl=900, show_spinner=False)
def tokens_generator(course_details):

    course_id = course_details['cloud_id']
    if course_id != '':
        utils = CategoryUtils()
        characters = string.ascii_letters + string.digits
        token = ''.join(random.choice(characters) for _ in range(5)).lower()
        token_course = course_id + token +  utils.get_current_date().replace('-','')
        
        firebase_token = {'cloud_id': token_course,'token': token, 'cloud_id_volunteer':course_details['cloud_id_volunteer'],
                    'cloud_id_course': course_details['cloud_id'],'status':[],'created_at':utils.get_current_date()}
        
        return firebase_token
    else:
        return None

# @st.cache_data(ttl=900, show_spinner=False)
def get_course_data():

    try:
        Conn = connector()
        course_requests = Conn.query_collection('course_proposal', [('status', '==','Approved')])
        courses_data = [doc.data for doc in course_requests]
        dataset = pd.DataFrame(courses_data)
        # dataset = dataset[dataset['cloud_id_volunteer'] == auth]
        return dataset
    except Exception as e:
        st.error(f"Error fetching course data: {str(e)}")
        return pd.DataFrame(columns=[
            'created_at', 'cloud_id_volunteer', 'first_name', 'last_name', 'gender', 'email',
            'volunteer_profile', 'cloud_id', 'course_categories', 'course_name', 'course_objective',
            'modality_proposal', 'min_audience', 'max_audience', 'allowed_age', 'city_proposal',
            'place_proposal', 'start_date', 'devices_proposal', 'tech_resources', 'prior_knowledge',
            'status', 'signed_concent', 'updated_at', 'notification'
        ])

@st.cache_data(ttl=900, show_spinner=False)
def get_attendance(cloud_id_course):
    try:
        Conn = connector()
        course_requests = Conn.query_collection('tokens_storage', [('cloud_id_course', '==', cloud_id_course)])
        courses_data = [doc.data for doc in course_requests]
        dataset = pd.DataFrame(courses_data)
        if dataset.empty:
            return []
        else:
            emails_attendance = list({email for item in dataset['status'].values for email in item})
        return emails_attendance
    except Exception as e:
        st.error(f"Error fetching course data: {str(e)}")
        return []

@st.cache_data(ttl=300,show_spinner=False)
def cached_upload_image(google_blobs, file):
    try:
        file_link = google_blobs.upload_image(file)
        return str(file_link) if file_link is not None else ""
    except Exception as e:
        st.error(f"Error al subir el archivo: {str(e)}")
        return ""

# @st.cache_data(ttl=900, show_spinner=False)
def get_intake_data(cloud_id_course) -> pd.DataFrame:
    """
    Fetch and filter intake data for enrolled users.
    
    Returns:
        pd.DataFrame: Filtered user data or empty DataFrame if no data found.
    """
    required_columns = [
        'first_name', 'last_name', 'dob', 'gender', 'nationality', 'is_ethnic','email',
        'city_residence', 'guardian_fullname', 'guardian_relationship', 'emergency_phone', 
        'education_level', 'user_role', 'strengths', 'weaknesses', 'disability', 
        'ethnic_affiliation', 'skills', 'how_to_learn','cloud_id'
    ]

    try:
        Conn = connector()
        course_requests = Conn.query_collection('intake_collection', [
            ('cloud_id_volunteer', '==', st.session_state.user_auth.cloud_id),
            ('status', '==', 'Enrolled')
        ])
        time.sleep(2)
        courses_data = [doc.data for doc in course_requests]
        dataset = pd.DataFrame(courses_data)
        
        if dataset.empty:
            return pd.DataFrame(columns=required_columns)
        
        dataset = dataset[dataset['cloud_id_course'] == cloud_id_course]

        intake_users = set(dataset['cloud_id_user'].values)
        user_data_list: List[Dict[str, Any]] = []
        
        for user_id in intake_users:
            user_data = Conn.get_document('users_collection', user_id)
            user_data_list.append(user_data.data)
            time.sleep(2)
        
        users_df = pd.DataFrame(user_data_list)
        users_df = users_df[required_columns]
        
        for col in required_columns:
            if col not in users_df.columns:
                users_df[col] = None
        
        list_columns = ['strengths', 'weaknesses', 'disability', 'ethnic_affiliation', 'skills', 'how_to_learn']
        for col in list_columns:
            users_df[col] = users_df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        
        users_df.rename(columns=clear_names(),inplace=True)

        return users_df

    except Exception as e:
        st.error(f"Error fetching intake data: {str(e)}")
        return pd.DataFrame(columns=required_columns)

def display_course_summary(course_details: Dict[str, Any]) -> None:
    """Display a summary of the selected course."""
    st.info(
        f"**Resumen:** El programa :blue[**{course_details['modality_proposal']}**] se encuentra "
        f":blue[**{course_details['status']}**]. Se impartirá en la(s) categoría(s) "
        f":blue[**{course_details['course_categories']}**], dirigido a participantes de "
        f":blue[**{course_details['allowed_age']}**] años. La capacidad está establecida entre "
        f":blue[**{course_details['min_audience']}**] y :blue[**{course_details['max_audience']}**] "
        f"asistentes, con una expectativa de asistencia mínima del 85%. El curso se confirmará al "
        f"alcanzar :blue[**{course_details['min_audience']}**] inscripciones.",
        icon=':material/summarize:'
    )
    
    st.success(f"**Objetivo Curso** {course_details['course_objective']}", icon=':material/target:')

def display_course_dates(course_details: Dict[str, Any], utils: CategoryUtils) -> None:
    """Display the course creation and start dates."""
    col1, col2 = st.columns(2)
    with col1:
        st.info(
            f"**Creación Propuesta** :blue[**{utils.format_date(course_details['created_at'], course_details['city_proposal'])}**]",
            icon=':material/today:'
        )
    with col2:
        st.info(
            f"**Fecha Clase** :blue[**{utils.format_date(course_details['start_date'], course_details['place_proposal'])}**]",
            icon=':material/today:'
        )

def display_course_requirements(course_details: Dict[str, Any]) -> None:
    """Display the course participation requirements."""
    devices = course_details['devices_proposal'].lower().strip()
    tech_resources = course_details['tech_resources'].lower().strip()
    prior_knowledge = course_details['prior_knowledge'].lower().strip()

    devices_info = "ningún dispositivo específico" if devices == 'no aplica' else devices
    tech_resources_info = "ningún recurso técnico en particular" if tech_resources == 'no aplica' else tech_resources
    prior_knowledge_info = f"Se recomienda tener conocimientos previos en {prior_knowledge}." if prior_knowledge != 'no aplica' else "No se requieren conocimientos previos específicos."

    st.write(
        f":blue-background[**Requisitos de participación**] Para este curso, los participantes deberán contar con {devices_info}. "
        f"En cuanto a recursos técnicos, se requiere {tech_resources_info}. {prior_knowledge_info}"
    )

def volunteer_dashboard() -> None:
    """Main function to display the volunteer dashboard."""

    utils = CategoryUtils()

    st.title("Gestión de Propuestas Voluntariado Académico")
    st.write(
        "Bienvenido a tu panel de control. Aquí podrás revisar el estado de tus propuestas, "
        "gestionar la asistencia de los participantes y marcar la finalización de tus cursos. "
        "Selecciona una propuesta para ver detalles y estadísticas."
    )

    st.info("""
    Aquí tienes datos confidenciales de tus participantes para mejorar tu experiencia educativa. Recuerda que esta información está protegida por nuestra [Política de Protección de Datos](https://drive.google.com/file/d/18Vu3lsHP0_UszWxSr8uez4W7P3_FWKfe/view). :blue[**Úsala exclusivamente para el desarrollo del curso y no la compartas con terceros.**]
    """, icon=":material/admin_panel_settings:")

    if st.session_state.user_auth is None:
        st.warning(f"No tienes cursos propuestos. :orange[**¿Crees que es un error?**] Escríbenos a wearecircleup@gmail.com", icon=":material/notifications:")
        return 

    proposals = get_course_data()

    if proposals.empty:
        st.warning(f"No tienes cursos propuestos. :orange[**¿Crees que es un error?**] Escríbenos a wearecircleup@gmail.com", icon=":material/notifications:")
        return
    
    proposals = proposals[proposals['cloud_id_volunteer'] == st.session_state.user_auth.cloud_id]

    course_names = set(proposals['course_name'].values)
    selected_course: Optional[str] = st.selectbox("Selecciona un curso para revisar", course_names, index=None)

    if selected_course is None:
        st.info(f"Selecciona uno de los cursos disponibles en tu :blue[**portafolio**] de Circle Up Community", icon=":material/notifications:")
        return

    courses = proposals[proposals['course_name'] == selected_course]

    if courses.empty:
        st.warning(f"No se encontraron cursos como :orange[**{selected_course}**]", icon=":material/notifications:")
        return

    course_details = courses.to_dict(orient='records')[0]

    return course_details

def expand_rows(row):
    estilos = row['Estilo Aprendizaje'].split(',')
    return pd.DataFrame({
        'Estilo Aprendizaje': estilos,
        'Grupo Edad': [row['Grupo Edad']] * len(estilos)
    })

def parse_date(date_string: str) -> datetime:
    """Parse date string to datetime object."""
    return datetime.strptime(date_string, "%d-%m-%Y")

def calculate_metrics(course: Dict[str, int], enrolled: List[int]) -> Dict[str, int]:
    """Calculate course metrics."""
    total = len(enrolled)
    target = max(course['min_audience'] * 1.2, course['min_audience'] * 0.85)
    return {
        'min': course['min_audience'],
        'max': course['max_audience'],
        'total': total,
        'target': int(target),
        'remaining': max(0, int(target) - total)
    }


# start_date = parse_date('15-08-2024')
# days_until_start = (start_date - datetime.now()).days
# st.write(days_until_start)
# st.write(get_course_data())
# st.write(st.session_state.user_auth.cloud_id)


def display_dashboard(course: Dict[str, int], enrolled: List[int], utils: CategoryUtils):
    """Display friendly course enrollment dashboard with highlighted key information."""
    
    metrics = calculate_metrics(course, enrolled)
    start_date = parse_date(course['start_date'])
    days_until_start = int((start_date - datetime.now()).days)
    cancel_date = start_date - timedelta(days=2)
    min_required = math.ceil(metrics['min']*0.85)

    if days_until_start > -1:
        st.info(f"""
            El curso comienza el :blue[**{utils.format_date(start_date.strftime('%d-%m-%Y')).lower()}**].
            Tenemos hasta el :blue[**{utils.format_date(cancel_date.strftime('%d-%m-%Y')).lower()}**], es decir, :blue[**{days_until_start - 2} días**]
            para alcanzar un mínimo de :blue[**{metrics['min']} participantes**] o al menos :blue[**{min_required} personas**], ¡pero seguro lo logramos!
            Ya vamos :blue[**{metrics['total']} inscritos**]. Solo faltarían al menos :blue[**{max(0, min_required - metrics['total'])} personas más**]. ¡Ánimo, estamos cerca!
            Recuerda, si no alcanzamos este número, el curso podría ser cancelado.
        """,icon=":material/battery_charging_50: ")
    elif days_until_start == -1:
        st.success("¡Fantástico! El curso comienza :green[**hoy**]. ¡Esperamos que todos estén listos para esta gran aventura de aprendizaje!")
    else:
        st.info(f"El curso ya está en marcha desde hace :blue[{abs(days_until_start)} días]. ¡Esperamos que estén disfrutando de esta experiencia!")

    progress = min(metrics['total'] / metrics['target'], 1.0)
    st.progress(progress)

    col1, col2, col3 = st.columns(3)
    col1.metric("Inscritos", metrics['total'], f"{metrics['total'] - math.ceil(metrics['min']*0.85)} Requeridos")
    col2.metric("Objetivo Ideal", metrics['target'], 
                f"{metrics['remaining']} Faltantes" if metrics['remaining'] > 0 else "¡Logrado!")
    col3.metric("Capacidad Máxima", metrics['max'], f"{metrics['max'] - metrics['total']} Disponibles")

    if metrics['total'] >= metrics['target']:
        st.success(f"¡Excelente trabajo! Hemos alcanzado y superado nuestro objetivo con :green[**{metrics['total']} participantes inscritos.**]")
    elif metrics['total'] >= metrics['min']:
        st.warning(f"¡Vamos por buen camino! Solo faltan :orange[**{metrics['remaining']} participantes**] para alcanzar nuestro objetivo ideal.")
    else:
        st.error(f"!Seguro lo logramos! faltan :red-background[**{math.ceil(metrics['min']*0.85) - metrics['total']} participantes**] para alcanzar el mínimo requerido.")

def update_attendance():
    get_attendance.clear()
    st.rerun()

def intake_dashboard(course_details,users_enrolled):

    attendace_emails = get_attendance(course_details['cloud_id'])
    
    utils = CategoryUtils()
    
    users_enrolled['Grupo Edad'] = users_enrolled['dob'].apply(utils.age_to_category)
    
    display_dashboard(course_details, users_enrolled,utils)

    col1, col2 = st.columns(2)
    
    with col1:

        st.title("Distribución Edad")
        st.info("Descubre la diversidad de tu grupo y ajusta tu contenido para conectar mejor con todos tus participantes.", icon=":material/fingerprint:")

        age_gender = users_enrolled.groupby(['Grupo Edad', 'Género']).size().reset_index(name='count')
        total_count_ag = age_gender['count'].sum()
        age_gender['Porcentaje (%)'] = (age_gender['count'] / total_count_ag * 100).round(2)

        chart_col1 = alt.Chart(age_gender).mark_bar().encode(
            x='Género:N',
            y='Porcentaje (%):Q',
            color='Grupo Edad:N',
            tooltip=['Grupo Edad', 'Género', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(height=350)

        st.altair_chart(chart_col1, use_container_width=True)

    with col2:
        st.title("Distribución Ciudad")
        st.info("Conoce la diversidad geográfica de tus participantes y ajustalo según las perspectivas de diferentes regiones.", icon=":material/south_america:")
        
        city_gender = users_enrolled.groupby(['Ciudad', 'Género']).size().reset_index(name='count')
        total_count_cg = city_gender['count'].sum()
        city_gender['Porcentaje (%)'] = (city_gender['count'] / total_count_cg * 100).round(2)

        chart_col2 = alt.Chart(city_gender).mark_bar().encode(
            x='Género:N',
            y='Porcentaje (%):Q',
            color='Ciudad:N',
            tooltip=['Ciudad', 'Género', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(height=350)

        st.altair_chart(chart_col2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:

        st.title("Nivel Educativo")
        st.info("Adapta el contenido de tu curso según la formación de tus participantes para un aprendizaje efectivo.", icon=":material/fit_screen:")
        
        edu_gender = users_enrolled.groupby(['Nivel Educativo', 'Género']).size().reset_index(name='count')
        total_count_eg = edu_gender['count'].sum()
        edu_gender['Porcentaje (%)'] = (edu_gender['count'] / total_count_eg * 100).round(2)

        chart_col3 = alt.Chart(edu_gender).mark_bar().encode(
            y='Género:N',
            x='Porcentaje (%):Q',
            color='Nivel Educativo:N',
            tooltip=['Nivel Educativo', 'Género', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(height=300)

        st.altair_chart(chart_col3, use_container_width=True)
    
    with col4:

        st.title("Estilos Aprendizaje")
        st.info("Conoce cómo aprenden tus estudiantes y optimiza tu enseñanza para potenciar el aprendizaje en el curso.", icon=":material/local_library:")
        
        expanded_df = pd.concat([expand_rows(row) for _, row in users_enrolled[['Estilo Aprendizaje', 'Grupo Edad']].iterrows()], ignore_index=True)
        learn_gender = expanded_df.groupby(['Estilo Aprendizaje', 'Grupo Edad']).size().reset_index(name='count')
        total_count_lg = learn_gender['count'].sum()
        learn_gender['Porcentaje (%)'] = (learn_gender['count'] / total_count_lg * 100).round(2)

        chart_col4 = alt.Chart(learn_gender).mark_bar().encode(
            y='Grupo Edad:N',
            x='Porcentaje (%):Q',
            color='Estilo Aprendizaje:N',
            tooltip=['Estilo Aprendizaje', 'Grupo Edad', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(height=300)

        st.altair_chart(chart_col4, use_container_width=True)
    
    st.write("Datos de Emergencia/Registro")
    st.info("Aquí encontrarás los datos de contacto y demográficos para gestionar tu curso de forma eficaz y segura.", icon=":material/dataset:")

    if st.button(":material/deployed_code_update: Actualizar Registro",use_container_width=True,type='primary'):
        update_attendance()

    users_enrolled['Nombre'] = users_enrolled['Nombre'] + ' ' + users_enrolled['Apellido']
    summary = users_enrolled.copy()

    if len(attendace_emails) == 0:
        filter_fields = ['Nombre','Contacto Emergencia','Parentesco','Tel. Emergencia','Div. Funcional','Grupo Étnico']
        summary = summary[filter_fields]
        st.dataframe(summary.dropna(), hide_index=True, use_container_width=True)

    else:
        filter_data = ['Registro','Nombre','Contacto Emergencia','Parentesco','Tel. Emergencia','Div. Funcional','Grupo Étnico']
        summary['Registro'] = summary['Email'].apply(lambda x: 'Registra' if x in attendace_emails else 'No registra')
        summary = summary[filter_data]

        st.dataframe(summary.dropna(), hide_index=True, use_container_width=True)

def token_attendance(course_details):
    
    firebase_token = None

    st.info("""
    Aquí puedes :blue[**registrar la asistencia**] de los participantes. Es crucial hacerlo correctamente, 
    ya que al finalizar el curso enviaremos :blue[**memorias**] y una :blue[**certificación simbólica**] solo a los asistentes reales. 
    Un registro preciso asegura que todos los participantes reciban los materiales correspondientes y evita envíos incorrectos.
    """, icon=":material/contextual_token:")
    
    st.write("""
    1. La :blue[**asistencia**] se registra con un :blue[**token único**] generado 5 minutos antes de iniciar o finalizar la clase. Es crucial crear solo un token por clase cuando todos estén listos, :blue[**sin generarlo anticipadamente**].
    2. Los participantes deben seleccionar la clase correcta en la sección de asistencia e :blue[**ingresar el token en minúsculas**]. Tras confirmar, recibirán una validación inmediata. Sus :blue[**certificados y memorias**] se enviarán en las siguientes 24 horas.
    """)

    
    utils = CategoryUtils()

    if 'token' in st.session_state:
        st.success(st.session_state.token, icon=":material/barcode:")

    if course_details['start_date'] == utils.get_current_date():
    
        if st.button(':material/qr_code_2: Generar Token', type='secondary', use_container_width=True):

            if 'token_code' in st.session_state:
                st.error(f"Token generado :red-background[**{st.session_state.token_code}**], no es necesario generar más tokens para esta sesión.", icon=":material/do_not_disturb_on:")
            else:
                firebase_token = tokens_generator(course_details)
                time.sleep(2)
                st.session_state.token_code = firebase_token['token']
                st.session_state.token = f"""
                Token generado, :green-background[**{firebase_token['token']}**],
                válido solo para el curso :green[**{course_details['course_name']}**],
                presentado el :green[**{utils.format_date(course_details['start_date'],course_details['city_proposal'])}**]
                """
                add_firebase(firebase_token)
                time.sleep(2)

    else:
        st.warning(f"""La generación del token solo estará disponible el :orange[**{utils.format_date(course_details['start_date'])}**], es decir el día que presentarás el curso :orange[**{course_details['course_name']}**]. No es posible generar el token en otra fecha.
        """, icon=":material/event:")

if 'finalize_course' not in st.session_state:
    st.session_state.finalize_course = ('Sestas list@? para dar por finalizado el curso?','info')


def finalize_course(course_details: Dict[str, str]) -> None:
    """
    Manejar el proceso de finalización del curso en Streamlit.
    """
    st.warning(':orange[¿Estás segur@ que quieres finalizar la clase?]',icon=':material/stop_circle:')
    
    ending_class = st.selectbox('¿Finalizar clase?', options=['No', 'Sí'],index=None)
    
    if ending_class == 'Sí':
        st.info("""
        Para :blue[**finalizar la clase, necesitas**] cargar una foto clara del grupo donde aparezcas tú, :blue[**evita contraluz**], confirma la asistencia y acepta las condiciones. Asegúrate de completar estos pasos antes de :material/stop_circle: Finalizar Clase.
        """,icon=':material/quick_reference:')

        with st.form('end_course'):
            uploaded_file = st.file_uploader('Cargar Fotografía del Grupo', type=['jpg', 'png', 'jpeg'])
            
            confirmation_checkbox = st.checkbox("Al aceptar, confirmas que el grupo marcó la asistencia correctamente, la foto cargada es clara y muestra al grupo contigo, y entiendes que este es un voluntariado sin remuneración.")            
            observations = st.text_area('Observaciones Adicionales', 
                        placeholder='Reporta aquí cualquier novedad sobre el espacio o la sesión.')
            
            end_class_button = st.form_submit_button(':material/stop_circle: Finalizar Clase', use_container_width=True)

        if end_class_button:
            missing_fields = []
            if not uploaded_file:
                missing_fields.append("Cargar Fotografía del Grupo")
            if not confirmation_checkbox:
                missing_fields.append("Confirmar las condiciones (marcar el checkbox)")
            
            if missing_fields:
                st.error(f"Por favor, completa todos los campos antes de finalizar.",icon=":material/missing_controller:")
            else:
                with st.spinner('Procesando...'):
                    google_blobs = GoogleBlobs('1yzuSRznAc_H38jw8-PgkrG-O85FS_iMt')
                    new_filename = f"{st.session_state.user_auth.email}-{st.session_state.user_auth.cloud_id}.{uploaded_file.name.split('.')[-1]}"
                    uploaded_file.name = new_filename
                    st.session_state.sign_document = cached_upload_image(google_blobs, uploaded_file)
                    time.sleep(2)
                    update_firebase_proposal(course_details['cloud_id'])
                    time.sleep(1)
                    update_sheets_proposal(course_details['cloud_id'])
                    time.sleep(1)
                    st.session_state.finalize_course = (
                    ":green[**¡Lo lograste! Tu clase ha terminado con éxito.**] "

                    "Tu generosidad al compartir tu experiencia hoy ha sido invaluable. Este curso cuenta como 6 horas de voluntariado, un paso significativo en tu viaje altruista. "
                    "• Hoy sumaste 6 horas a tu cuenta de voluntariado. "
                    "• Al llegar a 12 horas, recibirás un certificado de la Secretaría de Integración Social. "
                    ":green[**Tómate un momento para sentirte orgullos@.**] Tu conocimiento ha plantado semillas que seguirán creciendo en la mente de los participantes. "
                    "Cuando estés list@, nos encantaría verte de nuevo. Tu experiencia es un tesoro para nuestra comunidad. "
                    "Gracias por marcar la diferencia hoy. Tu dedicación no pasa desapercibida.","success")
                
    if 'finalize_course' in st.session_state:
        if isinstance(st.session_state.finalize_course, tuple) and st.session_state.finalize_course[1] == 'info':
            st.info(st.session_state.finalize_course[0],icon=':material/done_all:')
            del st.session_state.finalize_course
        else:
            st.success(st.session_state.finalize_course[0],icon=':material/potted_plant:')


def toggle_view(view_name):
    for view in ['course_details', 'course_dashboard', 'course_token','complete']:
        st.session_state[f'show_{view}'] = (view == view_name)

def main() -> None:
    course_details = volunteer_dashboard()
    if course_details:
        start_date = parse_date(course_details['start_date'])
        days_until_start = int((start_date - datetime.now()).days)
    
    if course_details and days_until_start >=-1:

        st.divider()
        col1, col2, col3 = st.columns(3)
        
        if col1.button(':material/dashboard: Detalles Propuesta', use_container_width=True, type='primary'):
            toggle_view('course_details')
        
        if col2.button(':material/analytics: Analítica Inscritos', use_container_width=True, type='primary'):
            toggle_view('course_dashboard')
        
        if col3.button(':material/token: Generar Tokens', use_container_width=True, type='primary'):
            toggle_view('course_token')
        
        if course_details:
            if st.session_state.get('show_course_details', False):
                display_course_summary(course_details)
                display_course_dates(course_details, CategoryUtils())
                display_course_requirements(course_details)
            
            if st.session_state.get('show_course_dashboard', False):
                users_enrolled = get_intake_data(course_details['cloud_id'])
                if users_enrolled.empty:
                    st.info(f"No te preocupes, aún no tenemos inscritos en :blue[**{course_details['course_name']}**]. Todavía hay tiempo para invitar a más personas. Si es necesario, podríamos considerar reprogramar para asegurar un buen número de participantes.",icon=":material/notifications:")
                else:
                    intake_dashboard(course_details,users_enrolled)
            
            if st.session_state.get('show_course_token', False):
                token_attendance(course_details)
        else:
            st.info("Selecciona un curso para visualizar su :blue[**dashboard analítico**] o los :blue[**detalles generales**].", icon=":material/account_tree:")

        if course_details:
            if st.button(':material/slow_motion_video: Clase Finalizada',use_container_width=True, type='primary'):
                toggle_view('complete')
            if st.session_state.get('show_complete', False):
                finalize_course(course_details)
    else:
        st.info(':blue[**¡Gracias por tu participación!**] Este curso ya ha finalizado. Esperamos que haya sido una experiencia enriquecedora. ¿Listo@ para más? Explora nuestros otros cursos disponibles.',icon=':material/rocket:')

    st.divider()
    if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
        st.switch_page('app.py')

if __name__ == "__main__":
    # try:
    main()
    menu()
    st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
    # except:
    #     st.switch_page('app.py')