import streamlit as st

st.set_page_config(
    page_title="Circle Up Community",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import json
from menu import menu
from utils.form_options import modality
from google.cloud import firestore
from classes.firestore_class import Firestore
from classes.spread_class import Sheets
from classes.utils_class import CategoryUtils
from utils.form_options import careers, volunteer_level
from typing import Dict, Any, List
import time
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.session_state.page_selected = None
st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)

@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

@st.cache_data(ttl=900,show_spinner=False)
def check_user_request_status(user_id):
    firestore = Firestore(firestore_client())
    return firestore.document_exists("volunteer_request", user_id)

def validate_form():
    for key in st.session_state:
        if key.startswith('volunteer_') and not st.session_state[key]:
            return False
    return True

def validate_user_status():
    return (st.session_state.user_auth.user_status != 'Inactive' and 
            st.session_state.user_auth.user_role == "Learner")


def prepare_sheets_data(instance_data,cloud_id):
    """
    Prepara los datos específicos para enviar a Google Sheets.
    """
    utils = CategoryUtils()

    return [
        utils.get_current_date(),
        utils.date_to_day_of_week(),
        utils.time_to_category(),
        instance_data.first_name,
        instance_data.last_name,
        instance_data.gender,
        utils.age_to_category(instance_data.dob),
        instance_data.email,
        instance_data.user_role,
        instance_data.city_residence,
        st.session_state.volunteer_education,
        st.session_state.volunteer_profession_category,
        st.session_state.volunteer_experience,
        st.session_state.volunteer_availability,
        st.session_state.volunteer_commitment,
        cloud_id,
        'Pending',
        "Pending"]


@st.cache_data(ttl=900,show_spinner=False)
def send_to_sheets(data: List[List[str]]):
    try:
        sheet = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM','Be Volunteer')
        sheet.create(data)
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False
    

def create_social_links():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button(":material/travel_explore: LinkedIn", "https://www.linkedin.com/company/circleup-community/",type='secondary',use_container_width=True)
    with col2:
        st.link_button(":material/phone_in_talk: WhatsApp", "https://wa.me/573046714626?text=Hola%20Circle%20Up%20Community!",type='secondary',use_container_width=True)
    with col3:
        st.link_button(":material/event: Calendly", "https://calendly.com/wearecircleup/15min",type='secondary',use_container_width=True)


def circle_up_introduction():
    st.title("¿Te interesaría participar como voluntario?")

    st.info(
    "Haz una diferencia real en tu comunidad con solo "
    ":blue[**4 horas al mes, el 1% de tu tiempo mensual, 25+ años de edad y mínimo 3 años de experiencia en tu área.**]. Serán 2 horas para preparar y 2 horas para presentar tu clase.",icon=":material/diversity_3:")

    tab1, tab2, tab3 = st.tabs(["Circle Up Community", "Proceso Simple", "Genera Impacto"])

    with tab1:
        st.write("""
        Circle Up Community te ofrece la oportunidad de generar un :blue[**impacto directo**] en tu comunidad con una mínima inversión de tiempo. Compartirás tu experiencia con total :blue[**flexibilidad**], adaptándote a tu agenda profesional. Te brindaremos :blue[**apoyo completo**] en la creación de material educativo, lo que a su vez potenciará tus habilidades de liderazgo y comunicación.
        """)

        st.info("""
        Con solo el :blue[**1% de tu tiempo mensual**], formarás parte de una :blue[**red de profesionales**] comprometidos con el cambio social, ampliando tus perspectivas y oportunidades de colaboración.
        """,icon=":material/self_improvement:")

    with tab2:

        st.info("""
        **Paso 1** Nuestro proceso está diseñado para ser :blue[**rápido y sencillo**], respetando tu tiempo. 
        Comienza registrándote con el formulario al pie de esta página. Inmediatamente después, 
        agendaremos una breve reunión virtual de máximo 20 minutos donde diseñaremos juntos tu sesión 
        y elegiremos la fecha, el lugar, la hora y la modalidad para tu clase de 2 horas, que será un sábado 
        dentro de las próximas 2-3 semanas.
        """,icon=":material/self_improvement:")

        st.info("""
        **Paso 2** Tras la reunión inicial, deberás enviar el acuerdo de voluntariado firmado y una copia de tu cédula en un único PDF.
        En este momento, ya tendrás definida la fecha, el lugar, la hora y la modalidad de tu clase.
        """,icon=":material/self_improvement:")

        st.info("""
        **Paso 3** Finalizaremos con una corta reunión virtual, dos días antes de tu clase, para ultimar detalles. Esta reunión 
        también será de máximo 20 minutos.
        """,icon=":material/self_improvement:")


    with tab3:
        st.info("""
        En Circle Up Community, creemos en el poder transformador del conocimiento compartido. Tu experiencia en resolver desafíos complejos es :blue[**clave para inspirar y preparar a las próximas generaciones**]. Con una inversión mínima de tiempo—:blue[**solo el 1% de tu mes**]—puedes fomentar el pensamiento crítico, la resolución creativa de problemas y el liderazgo efectivo.
        """,icon=":material/self_improvement:")

        st.write("""
        Tu participación contribuye directamente a construir comunidades más fuertes y resilientes, equipadas para enfrentar los desafíos del futuro. Cada sesión de 2 horas que impartas tiene el potencial de encender la chispa del cambio en quienes te escuchen, maximizando el impacto de tu valioso tiempo.
        """)

def volunteer_admitions():

    st.title("Formulario de Voluntarios")

    st.markdown("""
    Este formulario es el primer paso como voluntario en Circle Up. 
    Está diseñado para profesionales de **25 años** en adelante que deseen compartir su experiencia.
    """)

    if 'status_request' not in st.session_state:
        st.session_state.status_request = check_user_request_status(st.session_state.user_auth.cloud_id)

    if st.session_state.status_request:
        st.warning("Ya has enviado una solicitud de voluntariado. Tu solicitud está pendiente de validación. Por favor, está atento a tu email para más información.")
        return None

    with st.form("volunteer_form"):
        
        education = st.selectbox("Nivel educativo completado", options=volunteer_level, key="volunteer_education", index=None)
        profession_category = st.selectbox("Categoría profesional", options=careers, key="volunteer_profession_category", index=None)
        experience = st.number_input("Años de experiencia profesional", min_value=3, max_value=10, key="volunteer_experience")
        
        availability = st.selectbox("Tipo de voluntariado", options=modality,index=1, key="volunteer_availability")
        
        time_availability = st.selectbox("Disponibilidad de tiempo", options=[
            "Inmediata",
            "En 1-2 semanas",
            "En 2-3 semanas"
        ], key="volunteer_time_availability", index=2)
        
        commitment = st.slider("Horas que puedes donar al mes", min_value=4, max_value=8, step=2, key="volunteer_commitment", value=4)
        motivation = st.text_area("¿Por qué quieres ser parte de Circle Up?", key="volunteer_motivation", max_chars=300)
        
        submit_button = st.form_submit_button("Enviar Aplicación", use_container_width=True, type='primary')

    if submit_button:
        if validate_form() and validate_user_status():
            if not st.session_state.status_request:
                utils = CategoryUtils()

                volunteer_data = {
                    "age": utils.age_to_category(st.session_state.user_auth.dob),
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
                    "cloud_id_user": st.session_state.user_auth.cloud_id,
                    "cloud_id":'',
                    "user_status": st.session_state.user_auth.user_status,
                    "user_role": st.session_state.user_auth.user_role,
                    "status": 'Pending',
                    "notification": "Pending"
                }

                try:
                    firestore = Firestore(firestore_client())
                    doc = firestore.add_document("volunteer_request", volunteer_data)
                    time.sleep(2)
                    st.session_state.status_request = True
                    sheets_data = prepare_sheets_data(st.session_state.user_auth,doc.id)
                    
                    messages = [
                        ('Creando :blue[**solicitud...**]', 'auto_awesome_mosaic'),
                        ('Explora :blue[**Circle Up Community**]', 'travel_explore'),
                        ('Sé :blue[**embajador**] de tu comunidad profesional', 'military_tech')
                    ]

                    message_container = st.empty()

                    for msg, icon in messages:
                        message_container.info(msg, icon=f":material/{icon}:")
                        time.sleep(2)

                    time.sleep(1)
                    message_container.empty()

                    send_to_sheets([sheets_data]) 
                    time.sleep(2)

                    st.toast('¡Hip!')
                    time.sleep(1)
                    st.toast('¡Hip!')
                    time.sleep(1)
                    st.toast('¡Hurra! El registro se realizó correctamente.', icon=':material/library_add_check:')

                    st.success("¡Gracias por tu aplicación! Hemos recibido tu información y la evaluaremos pronto.")
                    st.info("Si tu aplicación es aprobada, recibirás un email con los siguientes pasos.")
                except ValueError as ve:
                    st.warning(str(ve))
                except Exception as e:
                    st.error(f"Hubo un error al procesar tu solicitud: {str(e)}")
            else:
                st.warning("Ya has enviado una solicitud de voluntariado. Tu solicitud está pendiente de validación. Por favor, está atento a tu email para más información.")
        else:
            if not validate_user_status():
                st.error("Lo sentimos, solo los usuarios activos con rol de Learner pueden enviar este formulario.")
            else:
                st.error("Por favor, completa todos los campos del formulario antes de enviar.")

if 'toogle_admision' not in st.session_state:
    st.session_state.toogle_admision = False

def toogle_view():
    st.session_state.toogle_admision = not st.session_state.toogle_admision

try: 
    menu()
    circle_up_introduction()
    if st.button('Diligenciar Formulario', type='primary', use_container_width=True):
        toogle_view()
    
    if st.session_state.toogle_admision:
        volunteer_admitions()

    st.divider()
    create_social_links()

    if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
        st.switch_page('app.py')

    st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)

except:
    st.switch_page('app.py')
