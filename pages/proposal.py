import streamlit as st
from menu import menu
import pandas as pd
import json
from utils.form_options import age_range,topics_of_interest, places, cities,modality,duration_options,consent_items

from google.cloud import firestore
from classes.utils_class import CategoryUtils
from classes.spread_class import Sheets
from classes.firestore_class import Firestore
from classes.users_class import Users
from datetime import datetime
from typing import List
import time

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(CategoryUtils().markdown_design(), unsafe_allow_html=True)
st.session_state.page_selected = None

if 'enable_form' not in st.session_state:
    st.session_state.enable_form = True

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

@st.cache_data(ttl=900, show_spinner=False)
def get_volunteer_id():
    try:
        Conn = connector()
        volunteer_requests = Conn.query_collection('volunteer_request', [('status', '==', 'Approved')])
        volunteer_data = [doc.data for doc in volunteer_requests]
        dataset = pd.DataFrame(volunteer_data)
        cloud_volunteer = list(dataset['cloud_id_user'].values)
        email_volunteer = list(dataset['email'].values)
        volunteers = dict(zip(email_volunteer,cloud_volunteer))
        return volunteers
    
    except Exception as e:
        return {'':''}
    
@st.cache_data(ttl=900, show_spinner=False)
def get_volunteer_data(cloud_id_user):
    try:
        Conn = connector()
        volunteer_info = Conn.get_document('users_collection',cloud_id_user)
        return volunteer_info.data
    except Exception as e:
        return {}

def prepare_data(instance_data):
    """
    Prepara los datos específicos para enviar a Google Sheets.
    """
    utils = CategoryUtils()
    volunteer_info = Users(**st.session_state.data_volunteer)

    return [
        utils.get_current_date(),
        utils.date_to_day_of_week(),
        utils.time_to_category(),
        volunteer_info.first_name,
        volunteer_info.last_name,
        volunteer_info.gender,
        utils.age_to_category(volunteer_info.dob),
        volunteer_info.email,
        volunteer_info.id_user_type,
        volunteer_info.id_user,
        volunteer_info.gender,
        volunteer_info.phone_number,
        volunteer_info.user_role,
        volunteer_info.city_residence,
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
    volunteer_info = Users(**st.session_state.data_volunteer)

    return {
        'created_at':utils.get_current_date(),
        'cloud_id_volunteer':volunteer_info.cloud_id,
        'first_name':volunteer_info.first_name,
        'last_name':volunteer_info.last_name,
        'gender':volunteer_info.gender,
        'email':volunteer_info.email,
        'volunteer_profile':instance_data.get('volunteer_profile_form', ''),
        'cloud_id':None,
        'course_categories':', '.join(instance_data.get('course_categories_form', [])),
        'course_name':instance_data.get('course_name_form', ''),
        'course_objective':instance_data.get('course_objective_form', ''),
        'modality_proposal':instance_data.get('modality_form', ''),
        'min_audience':instance_data.get('min_audience_form', 10),
        'max_audience':instance_data.get('max_audience_form', 10),
        'allowed_age':', '.join(instance_data.get('age_range_form', [])),
        'city_proposal':st.session_state.city_form,
        'place_proposal':st.session_state.place_form,
        'start_date':instance_data.get('start_date_form', '').strftime('%d-%m-%Y'),
        'devices_proposal':instance_data.get('devices_form', ''),
        'tech_resources':instance_data.get('tech_resources_form', ''),
        'prior_knowledge':instance_data.get('prior_knowledge_form', ''),
        'status':'Pending',
        'signed_concent':'Pending',
        'approved_at':'Pending',
        'notification':'Pending'
    }

@st.cache_data(ttl=900,show_spinner=False)
def sheets_agreement(data: List[List[str]]):
    try:
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Agreement Letter')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False

@st.cache_data(ttl=900,show_spinner=False)
def sheets_proposal(data: List[List[str]]):
    try:
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False

def main():
    st.title("Acuerdo de Voluntariado Circle Up Community")

    st.write("""
    Bienvenido al paso final para lanzar tu curso con Circle Up Community.
    Aquí formalizarás tu propuesta de curso de 2 horas para un sábado y aceptarás nuestro acuerdo de voluntariado.
    Al completar este formulario, recibirás el acuerdo de voluntariado por correo electrónico en aproximadamente 2 minutos.
    """)

    with st.form("curso_form"):

        volunteers = get_volunteer_id()
        volunteer_emails = volunteers.keys()
        volunteer_mail = st.selectbox("¿Cuál es tu email?", volunteer_emails, index=None, key="volunteer_mail")       

        st.title("1. Confirmación de Circle Up Community")
        st.info("Circle Up Community ha revisado y está de acuerdo con los siguientes elementos", icon=":material/thumb_up:")

        col1, col2 = st.columns(2)

        with col1:
            check_structure = st.checkbox("Estructura del Curso Completa", key="check_structure_form")
            check_development = st.checkbox("Contenido General Revisado/Ajustado", key="check_development_form")

        with col2:
            check_material = st.checkbox("Presentación Revisada/Ajustada", key="check_material_form")
            check_proposal = st.checkbox("Carta Propuesta Voluntario", key="check_proposal_form")

        st.title("2 Aspectos Logísticos")
        st.info("Por favor, confirme los siguientes elementos para finalizar la configuración del curso", icon=":material/format_list_bulleted:")

        col1, col2 = st.columns(2)
        with col1:
            selected_city = st.selectbox("Ciudad Presentación", cities, index=None, key="city_form")
        with col2:
            selected_place = st.selectbox("Espacio Presentación", places, index=None, key="place_form")
        
        with col1:
            selected_modality = st.selectbox("Modalidad Curso", modality, index=None, key="modality_form")
            min_audience = st.number_input("Audiencia Mínima", min_value=10, step=1,max_value=10, key="min_audience_form")

        with col2:
            selected_age_ranges = st.multiselect("Perfil Demográfico", age_range, key="age_range_form")
            max_audience = st.number_input("Audiencia Máxima", min_value=10, step=1, max_value=30, key="max_audience_form")

        
        start_date = st.date_input("Fecha Inicio", min_value=datetime.now().date(), key="start_date_form", format="DD-MM-YYYY")


        st.title("3. Requisitos de Participación")
        st.info("Especifique claramente los requisitos mínimos para los participantes", icon=":material/format_list_bulleted:")

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
        st.info("Por favor, complete la siguiente información general sobre el curso", icon=":material/school:")

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
        st.info("El voluntario debe leer detenidamente y aceptar los siguientes términos y condiciones", icon=":material/gavel:")

        consent_checks = [st.checkbox(item, key=f"consent_{i}_form") for i, item in enumerate(consent_items)]

        submitted = st.form_submit_button("Finalizar y Guardar",use_container_width=True,type='primary')

    if submitted:
        missing_fields = []

        volunteers = get_volunteer_id()
        st.session_state.data_volunteer = get_volunteer_data(volunteers[st.session_state.volunteer_mail])

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
            st.error(f"Por favor, complete los siguientes campos: {', '.join(missing_fields)}", icon=":material/notifications:")
        else:
            volunteer_data = {key: value for key, value in st.session_state.items() if key.endswith("_form")}
            st.success("Todos los campos han sido completados correctamente.", icon=":material/check_circle:")

            collection_data = prepare_collection(volunteer_data)
            doc_ref = connector().add_document('course_proposal',collection_data)
            collection_data['cloud_id'] = doc_ref.id
            sheets_proposal([list(collection_data.values())])

            sheets_data = prepare_data(volunteer_data)
            sheets_agreement([sheets_data])
            
            st.success(
                """
                El Acuerdo de Voluntariado ha sido enviado a tu correo electrónico.

                :green[**Pasos a seguir**]
                1. Firma la carta de :green-background[Acuerdo de Voluntariado Circle Up Community.]
                2. Adjunta una :green-background[fotocopia de tu cédula.]
                3. Envía ambos documentos en :green-background[un solo archivo PDF.]

                Estos documentos son esenciales para tu participación oficial.

                :green[**¡Bienvenid@ a Circle Up Community! Juntos haremos la diferencia.**]
                """,
                icon=":material/handshake:"
            )

            st.balloons()

            time.sleep(3)
            st.session_state.enable_form = False

    return None

if st.session_state.enable_form:
    main()
else:
    st.title("Acuerdo de Voluntariado Circle Up Community")

    st.write("""
    Bienvenido al paso final para lanzar tu curso con Circle Up Community.
    Aquí formalizarás tu propuesta de curso de 2 horas para un sábado y aceptarás nuestro acuerdo de voluntariado.
    Al completar este formulario, recibirás el acuerdo de voluntariado por correo electrónico en aproximadamente 2 minutos.
    """)

    st.info("""
    Es crucial que firmes este documento y lo envíes de vuelta en :blue-background[un solo PDF] junto con una copia de tu cédula.Tu curso se programará oficialmente una vez recibamos estos documentos.
    Por favor, revisa y completa cuidadosamente cada sección. Tu atención a los detalles asegurará una colaboración exitosa.
    """)

    st.write("""
    Tu participación es valiosa para nuestra comunidad. Al formalizar tu propuesta, te unes a una red comprometida con el crecimiento colectivo.
    Agradecemos tu dedicación y esperamos el impacto positivo que crearemos juntos. ¡Estamos emocionados por dar vida a tu propuesta!
    """)

    st.title("1. Confirmación de Circle Up Community")
    st.info("Circle Up Community ha revisado y está de acuerdo con los siguientes elementos", icon=":material/lists:")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.", icon=":material/library_add_check:")

    st.title("2 Aspectos Logísticos")
    st.info("Por favor, confirme los siguientes elementos para finalizar la configuración del curso", icon=":material/lists:")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.", icon=":material/library_add_check:")
    
    st.title("3. Requisitos de Participación")
    st.info("Especifique claramente los requisitos mínimos para los participantes", icon=":material/lists:")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.", icon=":material/library_add_check:")

    st.title("4. Información General del Curso")
    st.info("Por favor, complete la siguiente información general sobre el curso", icon=":material/lists:")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.", icon=":material/library_add_check:")

    st.title("5. Consentimiento General")
    st.info("El voluntario debe leer detenidamente y aceptar los siguientes términos y condiciones", icon=":material/lists:")
    st.success("¡Tarea completada! Tu progreso ha sido guardado.", icon=":material/library_add_check:")

    st.success(
        """
        El Acuerdo de Voluntariado ha sido enviado a tu correo electrónico.

        :green[**Pasos a seguir**]
        1. Firma la carta de :green-background[Acuerdo de Voluntariado Circle Up Community.]
        2. Adjunta una :green-background[fotocopia de tu cédula.]
        3. Envía ambos documentos en :green-background[un solo archivo PDF.]

        Estos documentos son esenciales para tu participación oficial.

        :green[**¡Bienvenid@ a Circle Up Community! Juntos haremos la diferencia.**]
        """,
        icon=":material/handshake:"
    )

    

menu()

st.divider()
if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
    st.switch_page('app.py')

