import streamlit as st
from menu import menu
from utils.body import html_banner
from google.cloud import firestore
from classes.firestore_class import Firestore
from utils.form_options import careers, volunteer_level, skills, roles_jerarquicos
from classes.anthropic_agent import brainstorming, generate_presentation
import anthropic
import json
from typing import List
import pandas as pd
import re
import gspread
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

from datetime import datetime


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
    p,ol,ul .stMarkdown {
        font-size: 14px;
    }
    h1,h2,h3,h4 {
        font-size: 22px;
    }
</style>
""", unsafe_allow_html=True)


if 'status_request' not in st.session_state:
    st.session_state.status_request = False
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'markdown_output' not in st.session_state:
    st.session_state.markdown_output = None
if 'profile_summary' not in st.session_state:
    st.session_state.profile_summary = None
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False
if 'presentation_generated' not in st.session_state:
    st.session_state.presentation_generated = False

@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

@st.cache_resource
def anthropic_client():
    key_claude = st.secrets["apikey_anthropic"]
    client = anthropic.Anthropic(api_key=key_claude)
    return client

@st.cache_data(show_spinner=False)
def data_anthropic(profile):
    if profile is not None:    
        claude_review = brainstorming(profile, anthropic_client())
        return claude_review.content.replace('```','')

@st.cache_data(ttl=1800) 
def get_profile_summary(form_data):
    profile_summary = f"""
    Profesional en el área de {form_data['career']}, específicamente con una carrera en {form_data['specific_career']}. 
    Actualmente trabaja como {form_data['current_job']}, desempeñando el rol de {form_data['current_role']}. 
    
    Su nivel educativo es {form_data['education_level']} y cuenta con {form_data['years_experience']} años de experiencia en su campo. 
    Sus habilidades principales incluyen {', '.join(form_data['skills_selected'])}. Le apasionan temas como {form_data['passion_topics']}. 
    {"Tiene experiencia dando clases o talleres" if form_data['teaching_experience'] else "No tiene experiencia previa dando clases o talleres"}, y 
    {"ha participado como voluntario antes" if form_data['volunteer_experience'] else "no ha participado como voluntario anteriormente"}.
    
    En cuanto a sus habilidades de enseñanza, el voluntario muestra un nivel de comodidad de {form_data['public_speaking']}/10 
    hablando en público y una habilidad de {form_data['explaining_complex_concepts']}/10 para explicar conceptos complejos. 
    {"Se considera una persona paciente al enseñar" if form_data['patient_teacher'] else "No se considera especialmente paciente al enseñar"}, 
    y tiene una disposición de {form_data['feedback_willingness']}/10 para recibir feedback y mejorar sus habilidades. 
    Su motivación principal para ser voluntario es {form_data['volunteer_motivation'].lower()}. 
    En cuanto a su actualización profesional, se encuentra en un nivel {form_data['field_update']}/10 en los últimos avances de su campo. 
    """
    st.session_state.profile_summary = profile_summary

    return profile_summary

@st.cache_data(ttl=3600)
def send_to_sheets(data: List[List[str]]):
    """
    Envía los datos a Google Sheets, añadiéndolos al final de la hoja existente.
    :param data: Lista de listas, donde cada lista interna representa una fila de datos
    """
    try:
        key_sheets = json.loads(st.secrets["sheetskey"])
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        creds = service_account.Credentials.from_service_account_info(key_sheets, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key('1FzqJ-hUvIOyALFS7lXyufIF5XfcfNe6Xdvf_WdhFDw8').sheet1

        num_rows = len(sheet.get_all_values())
        
        for row in data:
            num_rows += 1
            sheet.insert_row(row, num_rows)
        
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False
    

@st.cache_data(ttl=3600)
def structured_presentation(topic: str, _client):
    user_data = get_user_data()
    table_data = generate_presentation(topic, user_data, client)
    return table_data

def format_markdown_output(markdown_output):
    markdown_output = re.sub(r'Propuesta \d+:\s*', '', markdown_output)
    sections = re.split(r'^(####\s.*?)(?=\n####|\Z)', markdown_output, flags=re.MULTILINE | re.DOTALL)
    
    output1 = ""
    output2 = ""
    
    for i in range(1, len(sections), 2):
        if i+1 < len(sections):
            title = sections[i].strip()
            content = sections[i+1].strip()
            formatted_section = f"{title}\n\n{content}\n\n"
            if i == 1:  # Primera sección va a output1
                output1 = formatted_section
            elif i == 3:  # Segunda sección va a output2
                output2 = formatted_section
            # Las demás secciones se ignoran
    
    return output1, output2

menu()

def age_to_category(birth_date_str: str) -> str:
    """
    Convierte una fecha de nacimiento a una categoría de edad.
    
    :param birth_date_str: Fecha de nacimiento en formato "DD-MM-YYYY"
    :return: Categoría de edad como string
    """
    birth_date = datetime.strptime(birth_date_str, "%d-%m-%Y")
    today = datetime.now()
    age = today.year - birth_date.year

    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1

    categories = ["0-4", "5-9", "10-14", "15-19", "20-24","25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60+"]
    
    if age >= 60:
        return "60+"
    for category in categories:
        start, end = map(int, category.split("-"))
        if start <= age <= end:
            return category
    
    return "NoT Found"


def get_user_data():
    """
    Obtiene los datos de usuario de Streamlit session state.
    """
    return {
        "first_name": st.session_state.user_auth.first_name,
        "last_name": st.session_state.user_auth.last_name,
        "email": st.session_state.user_auth.email,
        "user_role": st.session_state.user_auth.user_role,
        "phone_number": st.session_state.user_auth.phone_number,
        "dob": age_to_category(st.session_state.user_auth.dob),
        "career": st.session_state.career,
        "specific_career": st.session_state.specific_career,
        "current_job": st.session_state.current_job,
        "education_level": st.session_state.education_level,
        "current_role": st.session_state.current_role,
        "years_experience": st.session_state.years_experience,
        "cloud_id": st.session_state.user_auth.cloud_id,
        "gender": st.session_state.user_auth.gender,
        "profile": st.session_state.profile_summary,
        "brainstorming": st.session_state.markdown_output,
        "idea": st.session_state.idea
    }

st.title("Circle Up - Creación de Propuestas Educativas")

st.write("Uno de los puntos críticos en el desarrollo de propuestas es el tiempo y el acompañamiento. En Circle Up, sabemos que no todos somos expertos en pedagogía o en preparar una clase. Queremos que solo comprometas el 1% de tu tiempo al mes interactuando con la comunidad, no detrás de un computador pensando en cómo arreglar diapositivas. Vamos a crear juntos el diseño de la clase en el menor tiempo posible.")

st.title("Hablemos de tu perfil")

st.write("Aquí empieza el brainstorming. En este formulario, vamos a responder algunas preguntas para entender tu perfil, tus intereses y experiencias. Luego, elegiremos un tema que te apasione y quieras compartir con la comunidad.")


with st.form("volunteer_profile"):
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

    scale_list = [1,2,3,4,5,6,7,8,9,10]
    st.write("En una escala del 1 al 10, evalúa lo siguiente:")
    public_speaking = st.selectbox("¿Qué tan cómodo te sientes hablando en público?", options=scale_list, key="public_speaking")
    explaining_complex_concepts = st.selectbox("¿Qué tan bueno eres explicando conceptos complejos de manera simple?", options=scale_list, key="explaining_complex_concepts")
    feedback_willingness = st.selectbox("¿Qué tan dispuesto estás a recibir feedback y mejorar tus habilidades de enseñanza?", options=scale_list, key="feedback_willingness")
    field_update = st.selectbox("¿Qué tan actualizado estás en los últimos avances de tu campo profesional?", options=scale_list, key="field_update")
    teaching_adaptation = st.selectbox("¿Qué tan cómodo te sientes adaptando tu estilo de enseñanza a diferentes tipos de estudiantes?", options=scale_list, key="teaching_adaptation")

    submit_button = st.form_submit_button("Enviar perfil", type='primary', use_container_width=True, disabled=st.session_state.button_disabled)

if submit_button and not st.session_state.form_submitted:
    required_fields = {
        "Área profesional": career,
        "Carrera específica": specific_career,
        "Trabajo actual": current_job,
        "Rol desempeñado": current_role,
        "Nivel educativo": education_level,
        "Años de experiencia": years_experience,
        "Habilidades": skills_selected,
        "Temas de pasión": passion_topics
    }
    
    missing_fields = [field for field, value in required_fields.items() if not value]
    
    if missing_fields:
        st.error(f"Por favor, completa los siguientes campos obligatorios: {', '.join(missing_fields)}")
    else:
        with st.spinner("Procesando tu perfil..."):
            st.session_state.form_submitted = True
            st.session_state.button_disabled = True
            
            form_data = {
                "career": career,
                "specific_career": specific_career,
                "current_job": current_job,
                "current_role": current_role,
                "education_level": education_level,
                "years_experience": years_experience,
                "skills_selected": skills_selected,
                "passion_topics": passion_topics,
                "teaching_experience": teaching_experience,
                "volunteer_experience": volunteer_experience,
                "public_speaking": public_speaking,
                "explaining_complex_concepts": explaining_complex_concepts,
                "patient_teacher": patient_teacher,
                "feedback_willingness": feedback_willingness,
                "volunteer_motivation": volunteer_motivation,
                "field_update": field_update
            }
            
            client = anthropic_client()
            st.session_state.profile_summary = get_profile_summary(form_data)
            st.session_state.markdown_output = data_anthropic(st.session_state.profile_summary)
        
        st.success("¡Perfil enviado con éxito!")
        st.rerun()

if st.session_state.form_submitted and st.session_state.markdown_output is not None:
    st.title("Brainstorming Personalizado")
    st.write("Las respuestas que se muestran a continuación son creadas para ti. Ahora vamos a leer cada una detalladamente, y es importante que estés muy atento para que podamos identificar lo que consideras que vale la pena enseñar a tu comunidad. Este contenido es creado con un modelo llamado Claude Sonnet 3.5 de Anthropic, y creemos que es bastante profesional, así que seguro será de utilidad.")
    
    idea1, idea2 = format_markdown_output(st.session_state.markdown_output)
    st.info(idea1)
    st.success(idea2)

    st.title("Selección de Propuesta")
    st.write("Ahora que ya tenemos un tema para presentarle a la comunidad, vamos a trabajar en el material de apoyo. Este material debe ser lo más estructurado posible y manejar un estándar para que todas las presentaciones de CircleUp tengan una identidad propia. En este punto, le entregaremos a Claude Sonnet 3.5 la idea para posteriormente evaluar el contenido.")
    st.title("Generador de Presentaciones Comunitarias")
    topic = st.text_area("Ingrese el tema de la presentación", key='idea')

    if st.button("Generar Presentación", use_container_width=True, type='primary', disabled=st.session_state.presentation_generated) and topic:
        with st.spinner("Generando presentación..."):
            client = anthropic_client()
            table_data = structured_presentation(st.session_state.idea, client)
            st.session_state.table_data = table_data
            st.session_state.presentation_generated = True
        
        st.success("¡Presentación generada con éxito!")
        st.rerun()
    else:
        st.info('Por favor, ingresa el tema de la presentación. Verifica antes de enviar.')

    if st.session_state.presentation_generated:
        # st.table(st.session_state.table_data)
        # st.write([values for table in st.session_state.table_data for key, values in table.items() if key =='name'])
        st.success("Presentación generada. Preparando envío a Google Sheets.")
        if st.button("Enviar/Ejecutar Google Sheets/AppScript", use_container_width=True):
            with st.spinner("Enviando datos a Google Sheets..."):
                sheet_data = [[row['description'] for row in st.session_state.table_data]]
                success = send_to_sheets(sheet_data)
            
            if success:
                st.success("¡Los datos de la presentación han sido enviados correctamente a Google Sheets!")
            else:
                st.error("Hubo un problema al enviar los datos a Google Sheets. Por favor, inténtalo de nuevo más tarde.")

if not st.session_state.form_submitted:
    st.info("Por favor, completa el formulario y haz clic en 'Enviar perfil' para ver los resultados.")


