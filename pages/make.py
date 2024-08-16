import streamlit as st

st.set_page_config(
    page_title="Circle Up Community",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from typing import Dict, Any, List, Optional, Tuple, TypedDict
import logging
import time
import json
import anthropic
import pandas as pd
from google.cloud import firestore
import re
from menu import menu
from utils.body import html_banner
from classes.spread_class import Sheets
from classes.utils_class import CategoryUtils
from classes.firestore_class import Firestore
from classes.users_class import Users
from utils.form_options import careers, volunteer_level, skills, roles_jerarquicos
from classes.anthropic_agent import brainstorming, generate_presentation
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

# Constants
SHEET_ID = '1FzqJ-hUvIOyALFS7lXyufIF5XfcfNe6Xdvf_WdhFDw8'
SHEET_NAME = 'Anthropic'

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)

# Initialize session state variables
def init_session_state():
    if 'brainstorm_output' not in st.session_state:
        st.session_state.brainstorm_output = None
    if 'profile_summary' not in st.session_state:
        st.session_state.profile_summary = None
    if 'button_disabled' not in st.session_state:
        st.session_state.button_disabled = False
    if 'presentation_generated' not in st.session_state:
        st.session_state.presentation_generated = False
    if 'data_volunteer' not in st.session_state:
        st.session_state.data_volunteer = {}
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

init_session_state()

@st.cache_resource
def get_firestore_client():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
    return firestore.Client.from_service_account_info(key_firestore)

@st.cache_resource
def get_anthropic_client():
    key_claude = st.secrets["ANTHROPIC_KEY"]
    return anthropic.Anthropic(api_key=key_claude)

# Cached data functions
@st.cache_data(ttl=900, show_spinner=False)
def get_anthropic_data(profile: Optional[str]) -> Optional[str]:
    if profile is not None:    
        claude_review: anthropic.Completion = brainstorming(profile, get_anthropic_client())
        return claude_review.content.replace('```', '')
    return None

@st.cache_data(ttl=900, show_spinner=False)
def get_volunteer_id():
    try:
        Conn = get_firestore_connector()
        volunteer_requests = Conn.query_collection('volunteer_request', [('status', '==', 'Approved')])
        volunteer_data = [doc.data for doc in volunteer_requests]
        dataset = pd.DataFrame(volunteer_data)
        cloud_volunteer = list(dataset['cloud_id_user'].values)
        email_volunteer = list(dataset['email'].values)
        return dict(zip(email_volunteer, cloud_volunteer))
    except Exception:
        return {'': ''}

@st.cache_data(ttl=900, show_spinner=False)
def get_volunteer_data(cloud_id_user):
    try:
        Conn = get_firestore_connector()
        volunteer_info = Conn.get_document('users_collection', cloud_id_user)
        return volunteer_info.data
    except Exception:
        return {}

@st.cache_data(ttl=900, show_spinner=False)
def structured_presentation(topic: str, _client, user_data):
    return generate_presentation(topic, user_data, _client)

# Helper functions
def get_profile_summary(form_data: Dict[str, Any]) -> str:
    return f"""
    Profesional en el área de {form_data['career']}, específicamente con una carrera en {form_data['specific_career']}. 
    Actualmente trabajo como {form_data['current_job']}, desempeñando el rol de {form_data['current_role']}. 
    
    Nivel educativo es {form_data['education_level']} y cuento con {form_data['years_experience']} años de experiencia en el campo. 
    Habilidades principales incluyen {', '.join(form_data['skills_selected'])}. Me apasionan temas como {form_data['passion_topics']}. 
    {"Tengo experiencia dando clases o talleres" if form_data['teaching_experience'] else "No tengo experiencia previa dando clases o talleres"}, y 
    {"he participado como voluntari@ antes" if form_data['volunteer_experience'] else "no he participado como voluntari@ anteriormente"}.
    
    En cuanto a habilidades de enseñanza, el(a) voluntari@ muestra un nivel de comodidad de {form_data['public_speaking']}/10 
    hablando en público y una habilidad de {form_data['explaining_complex_concepts']}/10 para explicar conceptos complejos. 
    {"Se considera una persona paciente al enseñar" if form_data['patient_teacher'] else "No se considera especialmente paciente al enseñar"}, 
    y tiene una disposición de {form_data['feedback_willingness']}/10 para recibir feedback y mejorar sus habilidades. 
    Su motivación principal para ser voluntario es {form_data['volunteer_motivation'].lower()}. 
    En cuanto a su actualización profesional, se encuentra en un nivel {form_data['field_update']}/10 en los últimos avances de su campo. 
    """

def format_brainstorm_output(brainstorming: str) -> Tuple[str, str]:
    cleaned_output: str = re.sub(r'Propuesta \d+:\s*', '', brainstorming)
    sections: list = re.split(r'^(####\s.*?)(?=\n####|\Z)', cleaned_output, flags=re.MULTILINE | re.DOTALL)
    
    output1: str = ""
    output2: str = ""
    
    for i in range(1, len(sections), 2):
        if i+1 < len(sections):
            title: str = sections[i].strip()
            content: str = sections[i+1].strip()
            formatted_section: str = f"{title}\n\n{content}\n\n"
            if i == 1: 
                output1 = formatted_section
            elif i == 3:
                output2 = formatted_section
    
    return output1, output2

def get_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        volunteer_info: Users = Users(**user_data)
        utils: CategoryUtils = CategoryUtils()
        
        return {
            "date": utils.get_current_date(),
            "week": utils.date_to_day_of_week(),
            "hour_range": utils.time_to_category(),
            "first_name": volunteer_info.first_name,
            "last_name": volunteer_info.last_name,
            "email": volunteer_info.email,
            "user_role": volunteer_info.user_role,
            "phone_number": volunteer_info.phone_number,
            "dob": utils.age_to_category(volunteer_info.dob),
            "career": st.session_state.career,
            "specific_career": st.session_state.specific_career,
            "current_job": st.session_state.current_job,
            "education_level": st.session_state.education_level,
            "current_role": st.session_state.current_role,
            "years_experience": st.session_state.years_experience,
            "cloud_id": volunteer_info.cloud_id,
            "gender": volunteer_info.gender,
            "profile": st.session_state.profile_summary,
            "brainstorming": st.session_state.brainstorm_output,
            "idea": st.session_state.idea,
        }
    except AttributeError as e:
        logging.error(f"AttributeError in get_user_data: {e}. This may be due to missing attributes in user_data or session_state.")
        st.error("Error al procesar los datos del usuario. Por favor, verifica que todos los campos estén completos.")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in get_user_data: {e}")
        st.error("Ocurrió un error inesperado al procesar los datos del usuario. Por favor, intenta nuevamente.")
        return None

def send_to_sheets(data: List[List[str]]) -> bool:
    try:
        sheet = Sheets(SHEET_ID, SHEET_NAME)
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False


@st.cache_resource
def get_firestore_connector():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn


def update_volunteer_data():
    get_volunteer_id.clear()
    get_volunteer_data.clear()
    st.rerun()

def update_brainstorm():
    get_anthropic_data.clear()

def main():
    st.title("Creación de Propuestas Educativas")
    st.write("Uno de los puntos críticos en el desarrollo de propuestas es el tiempo y el acompañamiento. En Circle Up Community, sabemos que no todos somos expertos en pedagogía o en preparar una clase. Queremos que solo comprometas el 1% de tu tiempo al mes interactuando con la comunidad, no detrás de un computador pensando en cómo arreglar diapositivas. Vamos a crear juntos el diseño de la clase en el menor tiempo posible.")
    
    st.title("Hablemos de tu perfil")
    st.write("Aquí empieza el brainstorming. En este formulario, vamos a responder algunas preguntas para entender tu perfil, tus intereses y experiencias. Luego, elegiremos un tema que te apasione y quieras compartir con la comunidad.")

    if st.button(":material/database: Actualizar Voluntarios", use_container_width=True):
        update_volunteer_data()
        st.rerun()

    create_volunteer_profile_form()

    if st.session_state.brainstorm_output is not None and st.session_state.data_volunteer is not None:
        display_brainstorming_results()
        create_presentation_form()

def create_volunteer_profile_form():
    with st.form("volunteer_profile"):
        volunteers = get_volunteer_id()
        volunteer_emails = volunteers.keys()
        
        volunteer_mail = st.selectbox("¿Cuál es tu email?", volunteer_emails, index=None, key="volunteer_mail")        
        career = st.selectbox("¿Cuál es tu área profesional?", careers, index=None, key="career")
        specific_career = st.text_input("¿Cuál es el nombre exacto de la carrera que estudiaste?", key="specific_career")
        
        col1, col2 = st.columns(2)
        with col1:
            current_job = st.text_input("¿Cuál es tu trabajo actual?", key="current_job")
            education_level = st.selectbox("¿Cuál es tu nivel educativo?", volunteer_level, index=None, key="education_level")
        with col2:
            current_role = st.selectbox("¿Qué rol desempeñas?", options=roles_jerarquicos, index=None, key="current_role")
            years_experience = st.number_input("¿Experiencia en tu campo?", min_value=0, max_value=50, key="years_experience")
        
        skills_selected = st.multiselect("Selecciona tus habilidades principales", skills, key="skills")
        passion_topics = st.text_area("¿Qué temas de tu profesión te apasionan más?", key="passion_topics")

        col3, col4 = st.columns(2)
        with col3:
            teaching_experience = st.checkbox("¿Tienes experiencia dando clases o talleres?", key="teaching_experience")
            patient_teacher = st.checkbox("Me considero una persona paciente cuando se trata de enseñar a otros.", key="patient_teacher")
        with col4:
            volunteer_experience = st.checkbox("¿Has participado como voluntario antes?", key="volunteer_experience")
            created_training_materials = st.checkbox("He creado materiales de formación o educativos en el pasado.", key="created_training_materials")

        learning_style = st.selectbox(
            "¿Cuál es tu estilo de aprendizaje preferido?",
            ["Visual", "Auditivo", "Kinestésico", "Lectura/Escritura"],
            key="learning_style"
        )
        volunteer_motivation = st.radio(
            "¿Cuál de las siguientes afirmaciones describe mejor tu motivación para ser voluntario?",
            ["Quiero compartir mis conocimientos", "Busco desarrollar mis habilidades de comunicación", "Deseo contribuir a mi comunidad", "Necesito experiencia para mi CV"],
            key="volunteer_motivation"
        )

        scale_list = list(range(1, 11))
        st.write("En una escala del 1 al 10, evalúa lo siguiente:")
        public_speaking = st.selectbox("¿Qué tan cómodo te sientes hablando en público?", options=scale_list, key="public_speaking")
        explaining_complex_concepts = st.selectbox("¿Qué tan bueno eres explicando conceptos complejos de manera simple?", options=scale_list, key="explaining_complex_concepts")
        feedback_willingness = st.selectbox("¿Qué tan dispuesto estás a recibir feedback y mejorar tus habilidades de enseñanza?", options=scale_list, key="feedback_willingness")
        field_update = st.selectbox("¿Qué tan actualizado estás en los últimos avances de tu campo profesional?", options=scale_list, key="field_update")
        teaching_adaptation = st.selectbox("¿Qué tan cómodo te sientes adaptando tu estilo de enseñanza a diferentes tipos de estudiantes?", options=scale_list, key="teaching_adaptation")

        submit_button_profile = st.form_submit_button(":material/local_shipping: Enviar perfil", type='primary', use_container_width=True)

    if submit_button_profile:
        process_volunteer_profile(volunteers)

def process_volunteer_profile(volunteers):
    required_fields = {
        "Email Volunteer": st.session_state.volunteer_mail,
        "Área profesional": st.session_state.career,
        "Carrera específica": st.session_state.specific_career,
        "Trabajo actual": st.session_state.current_job,
        "Rol desempeñado": st.session_state.current_role,
        "Nivel educativo": st.session_state.education_level,
        "Años de experiencia": st.session_state.years_experience,
        "Habilidades": st.session_state.skills,
        "Temas de pasión": st.session_state.passion_topics
    }

    missing_fields = [field for field, value in required_fields.items() if not value]
    
    if missing_fields:
        st.error(f"Por favor, completa los siguientes campos obligatorios: {', '.join(missing_fields)}")
    else:
        with st.spinner(":material/online_prediction: Procesando tu perfil..."):
            update_brainstorm()
            time.sleep(2)
            volunteers = get_volunteer_id()
            time.sleep(2)
            st.session_state.data_volunteer = get_volunteer_data(volunteers[st.session_state.volunteer_mail])
            time.sleep(2)

            form_data = {
                "volunteer_mail": st.session_state.volunteer_mail,
                "career": st.session_state.career,
                "specific_career": st.session_state.specific_career,
                "current_job": st.session_state.current_job,
                "current_role": st.session_state.current_role,
                "education_level": st.session_state.education_level,
                "years_experience": st.session_state.years_experience,
                "skills_selected": st.session_state.skills,
                "passion_topics": st.session_state.passion_topics,
                "teaching_experience": st.session_state.teaching_experience,
                "volunteer_experience": st.session_state.volunteer_experience,
                "public_speaking": st.session_state.public_speaking,
                "explaining_complex_concepts": st.session_state.explaining_complex_concepts,
                "patient_teacher": st.session_state.patient_teacher,
                "feedback_willingness": st.session_state.feedback_willingness,
                "volunteer_motivation": st.session_state.volunteer_motivation,
                "field_update": st.session_state.field_update
            }
            
            with st.spinner(':material/online_prediction: Generando ideas únicas para tu perfil...'):
                client = get_anthropic_client()
                st.session_state.profile_summary = get_profile_summary(form_data)
                st.session_state.brainstorm_output = get_anthropic_data(st.session_state.profile_summary)
                time.sleep(3)
            
        st.success("¡Perfil creado con éxito!", icon=":material/check_circle:")

def display_brainstorming_results():
    st.title("Brainstorming Personalizado")
    st.write("Las respuestas que se muestran a continuación son creadas para ti. Ahora vamos a leer cada una detalladamente, y es importante que estés muy atento para que podamos identificar lo que consideras que vale la pena enseñar a tu comunidad. Este contenido es creado con un modelo llamado Claude Sonnet 3.5 de Anthropic, y creemos que es bastante profesional, así que seguro será de utilidad.")
    
    idea1, idea2 = format_brainstorm_output(st.session_state.brainstorm_output)
    st.info(idea1.replace('#','').strip(), icon=":material/lightbulb:")
    st.success(idea2.replace('#','').strip(), icon=":material/rocket:")

def create_presentation_form():
    st.title(":material/bolt: Ideas a Diapositivas Sonnet 3.5")
    st.write("""
    Ahora que tenemos un tema para presentar a la comunidad, vamos a trabajar en el material de apoyo. 
    Este material será estructurado y seguirá un estándar para que todas las presentaciones de CircleUp tengan una identidad propia. 
    Claude 3.5 Sonnet evaluará el contenido basado en la idea proporcionada.
    """)
    with st.form(key='presentation_form', clear_on_submit=False):
        topic = st.text_area("Ingrese el tema de la presentación", key='idea')
        submit_button_slides = st.form_submit_button(
            "Generar Presentación", 
            use_container_width=True, 
            type='primary'
        )
    
    st.session_state.user_data = get_user_data(st.session_state.data_volunteer)

    if submit_button_slides and topic and st.session_state.data_volunteer:
        generate_presentation_slides(topic)
    elif submit_button_slides:
        st.warning('Por favor, ingresa el tema de la presentación.', icon=":material/edit_note:")

def generate_presentation_slides(topic):
    with st.spinner(":material/self_improvement: Creando una presentación única..."):
        client = get_anthropic_client()
        table_data = structured_presentation(topic, client, st.session_state.user_data)
        time.sleep(2)
        st.session_state.table_data = table_data
        st.session_state.presentation_generated = True
    
    with st.spinner(":material/self_improvement: Dando vida a tu presentación... ~5 min y listo."):
        st.info(":blue-background[Recordatorio] Para participar como voluntario en :blue[**Circle Up Community**], necesitarás proporcionar un PDF con tu cédula y el acuerdo de voluntario firmado. Te informaremos sobre esto en detalle más adelante.")
        sheet_data = [[row['description'] for row in st.session_state.table_data]]
        success = send_to_sheets(sheet_data)
        time.sleep(5)

    st.success("¡Tu presentación está lista! Revisa tu correo en ~5min para ver el resultado de nuestra colaboración.", icon=":material/document_scanner:")


if __name__ == "__main__":
    # try:
    main()
    menu()
    st.divider()
    st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
    if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
        st.switch_page('app.py')
    # except:
    #     st.switch_page('app.py')
