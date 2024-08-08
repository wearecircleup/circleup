import json
from typing import List, Dict, Any, Optional
import streamlit as st
from google.cloud import firestore
import pandas as pd
import time
import altair as alt
import re
from datetime import datetime, timedelta

from menu import menu
from classes.firestore_class import Firestore
from classes.utils_class import CategoryUtils

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

if 'user_auth' not in st.session_state:
    st.session_state.user_auth = None

auth = st.session_state.user_auth

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

def extract_course_name(text):
    pattern = r"El curso de (.*?)(?=\s(?:se realizará|será))"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

@st.cache_data(ttl=900, show_spinner=False)
def get_intake_data():
    try:
        cloud_id = str(st.session_state.user_auth.cloud_id)
        Conn = connector()
        course_requests = Conn.query_collection('intake_collection', [
            ('cloud_id_user', '==', cloud_id),
            ('status', '==', 'Enrolled')
        ])
        courses_data = [doc.data for doc in course_requests]
        dataset = pd.DataFrame(courses_data)
        dataset = dataset[dataset['cloud_id_volunteer'] != cloud_id]
        dataset['course_name'] = dataset['summary'].apply(extract_course_name)
        return dataset
    except Exception as e:
        return pd.DataFrame(columns=[
            'enrolled_at', 'week', 'hour_range', 'cloud_id', 'cloud_id_user', 'cloud_id_volunteer',
            'cloud_id_course', 'first_name', 'last_name', 'email', 'start_date', 'summary',
            'attendance_record', 'email_notice', 'email_reminder', 'status', 'last_change'
        ])

@st.cache_data(ttl=900, show_spinner=False)
def update_intake_collection(cloud_id):
    last_update = CategoryUtils().get_current_date()
    updates = {'attendance_record': 1,'last_change':last_update}
    try:
        connector().update_document('intake_collection', cloud_id, updates)
        return True
    except Exception as e:
        return False
    
@st.cache_data(ttl=900, show_spinner=False)
def update_tokens_storage(cloud_id):
    try:
        document = connector().get_document('tokens_storage',cloud_id)
        tokens_data = document.data
        emails_register = tokens_data['status']
        if st.session_state.user_auth.email not in emails_register:
            emails_register.append(st.session_state.user_auth.email)
        
        updates = {'status':emails_register}
        connector().update_document('tokens_storage', cloud_id, updates)
        return True
    except Exception as e:
        return False

# @st.cache_data(ttl=900, show_spinner=False)
def authenticate_token(firebase_token):
    default = {'cloud_id':'','cloud_id_course':'','cloud_id_volunteer':'','created_at':'','token':'','status': ''}
    try:
        Conn = connector()
        course_requests = Conn.get_document('tokens_storage',firebase_token)
        token_document = course_requests.data
        return token_document
    except Exception as e:
        return default

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

def display_attendance_instructions() -> None:
    """Display instructions for attendance marking."""
    st.title("Registro de Asistencia")
    st.write("Para recibir tu certificado y las memorias del curso, es necesario que marques tu asistencia.")
    st.info("Recuerda que este proceso es esencial para validar tu participación en el curso."
            ":blue[**Para más información sobre nuestras políticas de asistencia y certificación, consulta los [Términos y Condiciones](https://drive.google.com/file/d/1rZOLZRXzT4uIU9w23lVCTQpFlZWOHGRA/view).**]", icon=':material/action_key:')

def select_course(intakes: pd.DataFrame) -> Optional[Dict]:
    
    """Allow user to select a course and return course details."""
    
    utils = CategoryUtils()
    st.info("**Paso 1.** Selecciona el curso al que estás asistiendo.", icon=':material/self_improvement:')
    course_names = set(intakes['course_name'].values)
    selected_course: Optional[str] = st.selectbox("Seleccionar Curso", course_names, index=None)
    
    if not selected_course:
        st.info("Por favor, elige uno de los cursos en los que te has inscrito para continuar.", icon=":material/notifications:")
        return None
    
    courses = intakes[intakes['course_name'] == selected_course]
    if courses.empty:
        st.warning(f"No se encontraron cursos como :orange[**{selected_course}**]", icon=":material/notifications:")
        return None
    
    course_details = courses.to_dict(orient='records')[0]
    st.success(f"{course_details['summary']} :green[**{utils.format_date(course_details['start_date'])}**]", icon=":material/summarize:")
    
    return course_details

def get_attendance_token() -> str:
    """Prompt user for attendance token."""
    st.info("**Paso 2.** :blue-background[**Ingresar token**] de asistencia. Este es un código de 5 caracteres en minúscula que se proporcionará 5 minutos antes del inicio de la clase o antes de finalizar. :blue[**Si no lo recibes, por favor solicítalo.**]", icon=':material/self_improvement:')
    return st.text_input("Ingresar Token", max_chars=5, placeholder='kyj7r')

def validate_and_mark_attendance(course_details: Dict, token: str) -> None:
    """Validate token and mark attendance."""
    utils = CategoryUtils()
    firebase_token = course_details['cloud_id_course'] + token.lower().strip() + utils.get_current_date().replace('-', '')
    auth_token = authenticate_token(firebase_token)

    if st.session_state.user_auth.email in auth_token['status']:
        st.success(
            f"¡Excelente! Tu asistencia al curso :green[**{course_details['course_name']}**] ya está registrada con el token :green-background[**{token}**]. "
            f"No es necesario registrarlo nuevamente. En las próximas 24 horas, recibirás las memorias de la clase y tu certificado de asistencia.",
            icon=":material/approval_delegation:"
        )
        return None
    
    if auth_token['token'] == token.lower().strip():
        st.success(f"Tu asistencia ha sido registrada correctamente. El token :green-background[**{token}**] ingresado es válido.", icon=":material/approval_delegation:")
        
        update_intake_collection(course_details['cloud_id'])
        update_tokens_storage(auth_token['cloud_id'])

        time.sleep(2)
    elif len(token.strip()) != 5:
        st.warning(f"El token :orange-background[**{token}**] debe tener :orange[**5**] caracteres no :orange[**{len(token.strip())}**]. Revísalo e intenta de nuevo.", icon=":material/pending:")
    else:
        st.warning(f"El token :orange-background[**{token}**] ingresado no es válido. Por favor, intenta con otro token.", icon=":material/pending:")

def parse_date(date_string: str) -> datetime:
    """Parse date string to datetime object."""
    return datetime.strptime(date_string, "%d-%m-%Y")

def intake_attendance() -> Optional[Dict]:

    """Main function to handle attendance intake process."""

    utils = CategoryUtils()

    intakes = get_intake_data()
    if intakes.empty:
        st.warning("No hay cursos disponibles. :orange[**Inscríbete o espera ~15min si ya lo hiciste.**]", icon=":material/notifications:")
        return None

    display_attendance_instructions()
    course_details = select_course(intakes)
    if not course_details:
        return None

    start_date = parse_date(course_details['start_date'])
    days_until_start = (start_date - datetime.now()).days
    today = datetime.now().strftime('%d-%m-%Y')
    today_format = utils.format_date(today)
    course_date = utils.format_date(course_details['start_date'])

    if days_until_start > 0:
            st.warning(f'Recuerda que solo puedes marcar asistencia el :orange[**{course_date}**]. Hoy, :orange[**{today_format}**], no es un día válido. Asegúrate de registrarte en la fecha correcta.',icon=":material/event:")
            return None

    token = get_attendance_token()
    st.info("**Paso 3.** Haz clic en :blue[**Marcar Asistencia**].", icon=':material/self_improvement:')

    if st.button(":material/ads_click: Marcar Asistencia", use_container_width=True, type='primary'):
        if course_details and token:
            validate_and_mark_attendance(course_details, token)
        else:
            st.error("Selecciona un curso e ingresa el token de asistencia. Puede que falte uno o ambos.", icon=":material/pending:")

    return course_details

def main() -> None:
    intake_attendance()
    st.divider()

    if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
        st.switch_page('app.py')

if __name__ == "__main__":
    try:
        main()
        menu()
    except AttributeError:
        st.switch_page('app.py')

