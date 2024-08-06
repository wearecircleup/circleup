import json
from typing import List, Dict, Any, Optional
import streamlit as st
from google.cloud import firestore
import pandas as pd
import time
import altair as alt


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
if 'page_selected' not in st.session_state:
    st.session_state.page_selected = None

if 'user_auth' not in st.session_state:
    st.session_state.user_auth = None

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
    }
    return column_rename_map

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

@st.cache_data(ttl=900, show_spinner=False)
def get_course_data():
    auth = st.session_state.user_auth.cloud_id
    try:
        Conn = connector()
        course_requests = Conn.query_collection('course_proposal', [('cloud_id_volunteer', '==', st.session_state.user_auth.cloud_id)])
        courses_data = [doc.data for doc in course_requests]
        dataset = pd.DataFrame(courses_data)
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
def get_intake_data() -> pd.DataFrame:
    """
    Fetch and filter intake data for enrolled users.
    
    Returns:
        pd.DataFrame: Filtered user data or empty DataFrame if no data found.
    """
    required_columns = [
        'first_name', 'last_name', 'dob', 'gender', 'nationality', 'is_ethnic', 
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
        f"asistentes, con una expectativa de asistencia mínima del 50%. El curso se confirmará al "
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
        f"En cuanto a recursos técnicos, se requiere {tech_resources_info}. {prior_knowledge_info}",
        icon=':material/clipboard-list:'
    )

def volunteer_dashboard() -> None:
    """Main function to display the volunteer dashboard."""

    st.title("Gestión de Propuestas de Voluntariado Académico")
    st.info(
        "Bienvenido a tu panel de control. Aquí podrás revisar el estado de tus propuestas, "
        "gestionar la asistencia de los participantes y marcar la finalización de tus cursos. "
        "Selecciona una propuesta para ver detalles y estadísticas.",
        icon=":material/stadia_controller:"
    )

    status_options: List[str] = ["Approved", "Denied", "Pending"]
    selected_status: Optional[str] = st.selectbox("Selecciona el estado de la propuesta:", status_options, index=None)
    
    if selected_status is None:
        st.info("Selecciona alguno de los estados :blue-background[**Approved, Denied, Pending**]", icon=":material/notifications:")
        return

    volunteer_proposals = get_course_data()
    proposals = volunteer_proposals[volunteer_proposals['status'] == selected_status]

    if proposals.empty:
        st.warning(f"No hay solicitudes con estado :orange[**{selected_status}.**]", icon=":material/notifications:")
        return

    course_names = set(proposals['course_name'].values)
    selected_course: Optional[str] = st.selectbox("Seleccione una solicitud para revisar:", course_names, index=None)

    if selected_course is None:
        st.info(f"Selecciona alguno de los cursos disponibles en el estado :blue-background[**{selected_status}.**]", icon=":material/notifications:")
        return

    courses = proposals[proposals['course_name'] == selected_course]

    if courses.empty:
        st.warning(f"No hay cursos como :orange[**{selected_course}.**]", icon=":material/notifications:")
        return

    course_details = courses.to_dict(orient='records')[0]
    # display_course_summary(course_details)
    # display_course_dates(course_details, utils)
    # display_course_requirements(course_details)

    return course_details

def expand_rows(row):
    estilos = row['Estilo Aprendizaje'].split(',')
    return pd.DataFrame({
        'Estilo Aprendizaje': estilos,
        'Género': [row['Género']] * len(estilos)
    })

def intake_dashboard(course_details):
    users_enrolled = get_intake_data()
    utils = CategoryUtils()
    
    users_enrolled['Grupo Edad'] = users_enrolled['dob'].apply(utils.age_to_category)
    
    st.title("Dashboard de Inscripción al Curso")
    
    st.info("""
    Este dashboard presenta información agregada sobre los participantes inscritos en el curso. 
    Estos datos son confidenciales y están protegidos por la Política de Protección de Datos de Circle Up Community. 
    Su uso está estrictamente limitado al desarrollo y mejora de la experiencia educativa. 
    No comparta esta información con terceros.
    """)
    
    total_enrolled = len(users_enrolled)
    min_audience = course_details['min_audience']
    max_audience = course_details['max_audience']
    progress = (total_enrolled - min_audience) / (max_audience - min_audience)

    st.info(f":blue[**Inscritos**] {total_enrolled}/{max_audience} ({progress:.1%} del objetivo)")
    
    col1, col2 = st.columns(2)
    
    with col1:

        st.title("Distribución por Edad y Género")
        st.info("Este gráfico muestra la composición demográfica del grupo por edad y género.")

        age_gender = users_enrolled.groupby(['Grupo Edad', 'Género']).size().reset_index(name='count')
        total_count_ag = age_gender['count'].sum()
        age_gender['Porcentaje (%)'] = (age_gender['count'] / total_count_ag * 100).round(2)

        chart_col1 = alt.Chart(age_gender).mark_bar().encode(
            x='Género:N',
            y='Porcentaje (%):Q',
            color='Grupo Edad:N',
            tooltip=['Grupo Edad', 'Género', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(title='Distribución de Edades/Género',height=350)

        st.altair_chart(chart_col1, use_container_width=True)

    with col2:
        st.title("Distribución por Nacionalidad")
        st.info("Este gráfico presenta la diversidad de proveniencia de los participantes.")

        city_gender = users_enrolled.groupby(['Ciudad', 'Género']).size().reset_index(name='count')
        total_count_cg = city_gender['count'].sum()
        city_gender['Porcentaje (%)'] = (city_gender['count'] / total_count_cg * 100).round(2)

        chart_col2 = alt.Chart(city_gender).mark_rect().encode(
            x='Género:N',
            y='Porcentaje (%):Q',
            color='Ciudad:N',
            tooltip=['Ciudad', 'Género', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(title='Distribución de Género/Ciudad',height=350)

        st.altair_chart(chart_col2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:

        st.title("Distribución por Nivel Educativo")
        st.info("Este gráfico presenta la diversidad de nivel educativo de los participantes.")

        edu_gender = users_enrolled.groupby(['Nivel Educativo', 'Género']).size().reset_index(name='count')
        total_count_eg = edu_gender['count'].sum()
        edu_gender['Porcentaje (%)'] = (edu_gender['count'] / total_count_eg * 100).round(2)

        chart_col3 = alt.Chart(edu_gender).mark_rect().encode(
            x='Género:N',
            y='Porcentaje (%):Q',
            color='Nivel Educativo:N',
            tooltip=['Nivel Educativo', 'Género', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(title='Distribución de Nivel Educativo / Género',height=300)

        st.altair_chart(chart_col3, use_container_width=True)
    
    with col4:
        
        st.title("Distribución por Estilo Aprendizaje")
        st.info("Este gráfico presenta la diversidad de Estilo Aprendizaje de los participantes.")

        expanded_df = pd.concat([expand_rows(row) for _, row in users_enrolled[['Estilo Aprendizaje', 'Género']].iterrows()], ignore_index=True)
        learn_gender = expanded_df.groupby(['Estilo Aprendizaje', 'Género']).size().reset_index(name='count')
        total_count_lg = learn_gender['count'].sum()
        learn_gender['Porcentaje (%)'] = (learn_gender['count'] / total_count_lg * 100).round(2)

        chart_col4 = alt.Chart(learn_gender).mark_bar().encode(
            x='Género:N',
            y='Porcentaje (%):Q',
            color='Estilo Aprendizaje:N',
            tooltip=['Estilo Aprendizaje', 'Género', alt.Tooltip('Porcentaje (%):Q', format='.1f')]
        ).properties(title='Distribución de Edades / Género',height=300)

        st.altair_chart(chart_col4, use_container_width=True)
    
    st.title("Resumen de Participantes")
    st.info("Esta tabla proporciona información detallada sobre cada participante.")
    users_enrolled['Nombre'] = users_enrolled['Nombre'] + ' ' + users_enrolled['Apellido']
    summary = users_enrolled[['Nombre','Rol','Contacto Emergencia','Parentesco','Tel. Emergencia','Div. Funcional','Grupo Étnico']]
    st.dataframe(summary.dropna(), hide_index=True, use_container_width=True)

def main() -> None:
    course_details = volunteer_dashboard()
    if course_details:
        intake_dashboard(course_details)
    menu()

    st.divider()
    if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
        st.switch_page('app.py')

if __name__ == "__main__":
    main()
