import streamlit as st
import pandas as pd
from menu import menu
from google.cloud import firestore
import json
from classes.utils_class import CategoryUtils
from classes.spread_class import Sheets
from classes.firestore_class import Firestore
from classes.blobs_class import GoogleBlobs
from classes.users_class import Users
from typing import Dict, List, Optional
from itertools import chain
from google.cloud.exceptions import NotFound, Conflict
from googleapiclient.errors import HttpError
import firebase_admin.exceptions
import time

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

st.session_state.page_selected = None

if 'show_explore' not in st.session_state:
    st.session_state.show_explore = False
if 'show_manage' not in st.session_state:
    st.session_state.show_manage = False


@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

@st.cache_data(ttl=900,show_spinner=False)
def cached_upload_file(google_blobs, file):
    try:
        file_link = google_blobs.upload_file(file)
        return str(file_link) if file_link is not None else ""
    except Exception as e:
        st.error(f"Error al subir el archivo: {str(e)}")
        return ""

@st.cache_data(ttl=900, show_spinner=False)
def get_course_data():
    try:
        Conn = connector()
        course_requests = Conn.query_collection('course_proposal', [('status', '==', 'Approved')])
        courses_data = [doc.data for doc in course_requests]
        dataset = pd.DataFrame(courses_data)
        dataset.rename(columns={'cloud_id':'cloud_id_course'}, inplace=True)
        return dataset
    except Exception as e:
        return pd.DataFrame(columns=[
            'created_at', 'cloud_id_volunteer', 'first_name', 'last_name', 'gender', 'email',
            'volunteer_profile', 'cloud_id', 'course_categories', 'course_name', 'course_objective',
            'modality_proposal', 'min_audience', 'max_audience', 'allowed_age', 'city_proposal',
            'place_proposal', 'start_date', 'devices_proposal', 'tech_resources', 'prior_knowledge',
            'status', 'signed_concent', 'updated_at', 'notification'
        ])

@st.cache_data(ttl=900, show_spinner=False)
def get_intake_data():
    try:
        Conn = connector()
        course_requests = Conn.query_collection('intake_collection', [
            ('cloud_id_user', '==', st.session_state.user_auth.cloud_id),
            ('status', '==', 'Enrolled')
        ])
        courses_data = [doc.data for doc in course_requests]
        dataset = pd.DataFrame(courses_data)
        return dataset
    except Exception as e:
        return pd.DataFrame(columns=[
            'enrolled_at', 'week', 'hour_range', 'cloud_id', 'cloud_id_user', 'cloud_id_volunteer',
            'cloud_id_course', 'first_name', 'last_name', 'email', 'start_date', 'summary',
            'attendance_record', 'email_notice', 'email_reminder', 'status', 'last_change'
        ])

def lock_data(field):
    try:
        data_courses = get_course_data()
        users_enrollments = get_intake_data()
        enlistment = pd.merge(data_courses, users_enrollments, on=['cloud_id_course'], how='inner')
        categories = enlistment[field].str.split(',')
        flattened_categories = chain.from_iterable(categories)
        unique_categories = sorted(set(flattened_categories))
        
        return unique_categories
    except Exception as e:
        return []

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

def send_to_sheets(data: List[List[str]],sheet_id,sheet_name):
    try:
        sheet = Sheets(sheet_id,sheet_name)
        sheet.create(data)
        return True
    except Exception as e:
        return False
    
def update_sheets(cloud_id):
    last_update = CategoryUtils().get_current_date()
    updates = {'attendance_record': 0, 'email_notice': 'Pending','email_reminder': 0,'status':'Unenrolled','last_change':last_update}
    try:
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Enrollment')
        sheet.replace_values(cloud_id, updates)
        return True
    except Exception as e:
        return False

def update_firebase(cloud_id):
    last_update = CategoryUtils().get_current_date()
    updates = {'attendance_record': 0, 'email_notice': 'Pending','email_reminder': 0,'status':'Unenrolled','last_change':last_update}
    try:
        connector().update_document('intake_collection', cloud_id, updates)
        return True
    except Exception as e:
        
        return False

def send_to_firebase(data: Dict):
    try:
        intake_data = connector().add_document('intake_collection', data)
        return intake_data.id
    except Exception as e:
        return False

def enrollment_notice(data: Dict, selected_course):
    st.session_state.confirmation_message = ":green-background[Tu inscripción ha sido registrada exitosamente]. Ahora aparecerás en :green[**Gestionar Inscripciones**]. :green-background[Recibirás un email en ~5 min.]"

    st.session_state.show_explore = False
    
    cloud_id = send_to_firebase(data)
    data['cloud_id'] = cloud_id 
    sheet_entry = [list(data.values())]

    with st.spinner("Guardando tu inscripción...\n\n"
                    "1. Vas a recibir un email en ~5min.\n"
                    "2. Si no recibes el email, escribe a wearecircleup@gmail.com\n"
                    "3. Si quieres donar o ayudar, escribe a +57 3046714626"):
        
        time.sleep(3)
        send_to_sheets(sheet_entry,'1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Enrollment')
        time.sleep(3)

    st.session_state.lock_courses = lock_data('course_name')    
    st.rerun()

def unenrollment_notice(cloud_id: str, selected_course):
    st.session_state.confirmation_message = f":green-background[**Inscripción cancelada**] para :green[**{selected_course}**]. :green-background[**El cambio es inmediato**]. Puedes volver a inscribirte en cualquier momento, pero ten en cuenta que los cupos pueden completarse rápidamente."

    st.session_state.show_manage = False
    update_firebase(cloud_id)

    with st.spinner("Actualizando tu inscripción...\n\n"
                    "1. Vas a recibir un email en ~5min.\n"
                    "2. Si no recibes el email, escribe a wearecircleup@gmail.com\n"
                    "3. Si quieres donar o ayudar, escribe a +57 3046714626"):
        
        time.sleep(3)
        update_sheets(cloud_id)
        time.sleep(3)

    st.session_state.lock_courses = lock_data('course_name')

def show_explore():
    st.session_state.show_explore = True
    st.session_state.show_manage = False

def show_manage():
    st.session_state.show_manage = True
    st.session_state.show_explore = False


def is_age_category_appropriate(user_age_category: str, allowed_ages: str) -> bool:
    """Verifica si la categoría de edad del usuario está en las categorías permitidas."""
    allowed_categories = [cat.strip() for cat in allowed_ages.split(',')]
    return user_age_category in allowed_categories

def filter_age_appropriate_courses(data_courses: pd.DataFrame, user_age_category: str) -> pd.DataFrame:
    """Filtra los cursos apropiados para la categoría de edad del usuario."""
    return data_courses[data_courses['allowed_age'].apply(lambda x: is_age_category_appropriate(user_age_category, x) if pd.notna(x) else False)]

def update_intakes():
    get_intake_data.clear()
    st.rerun()

def entry_unregister():
    try:
        data_courses = get_course_data()
        intake_courses = get_intake_data()

        st.write(intake_courses)

        if data_courses.empty or intake_courses.empty:
            st.error("No se pudieron cargar los datos de los cursos. Por favor, intenta más tarde.", icon=":material/error:")
            return

        course_options = list(set(st.session_state.lock_courses))

        if course_options:
            st.warning("**¿Estás seguro de que deseas cancelar tu inscripción en algún curso?** :orange[**Esta acción no se puede deshacer.**]", icon=":material/shadow_minus:")

            st.info("**Paso 1:** Selecciona el curso que deseas cancelar", icon=":material/ads_click:")
            selected_course = st.selectbox(
                "Elige el curso que quieres cancelar:",
                options=course_options,
                index=None,
                placeholder='Seleccionar Curso'
            )

            if selected_course:
                try:
                    selected_request = data_courses[data_courses['course_name'] == selected_course].iloc[0]
                except IndexError:
                    st.error(f"No se encontró información para el curso '{selected_course}'. Por favor, contacta al soporte.", icon=":material/error:")
                    return

                if not selected_request.empty:
                    try:
                        filter_ids = data_courses[data_courses['course_name'] == selected_course][['cloud_id_course','cloud_id_volunteer']]
                        course_definition = filter_ids.to_dict(orient='records')[0]

                        volunter_id = intake_courses['cloud_id_volunteer'] == course_definition['cloud_id_volunteer']
                        course_id = intake_courses['cloud_id_course'] == course_definition['cloud_id_course']
                        
                        enrollment_id = intake_courses[(volunter_id) & (course_id)]['cloud_id']
                        
                        if enrollment_id.empty:
                            st.error("No se encontró tu inscripción para este curso. Por favor, contacta al soporte.", icon=":material/error:")
                            return
                        
                        enrollment_id = str(enrollment_id.iloc[0])

                        st.write("Aquí tienes la información del curso que has seleccionado para cancelar")
                        course_description(selected_request)

                        st.error("**¿Estás segur@ de que deseas cancelar tu inscripción en este curso?**", icon=":material/delete:")
                        if st.button('Cancelar Inscripción', type='secondary', use_container_width=True):
                            unenrollment_notice(enrollment_id, selected_course)
                            st.success(st.session_state.confirmation_message, icon=":material/data_check:")

                    except KeyError as e:
                        st.error(f"Error al procesar los datos del curso: {str(e)}. Por favor, contacta al soporte.", icon=":material/error:")
                    except Exception as e:
                        st.error(f"Ocurrió un error inesperado: {str(e)}. Por favor, intenta de nuevo o contacta al soporte.", icon=":material/error:")

            else:
                st.info("Selecciona un curso de la lista para proceder con la cancelación.", icon=":material/ads_click:")
        else:
            st.warning("Por el momento no tenemos cursos disponibles para ti. Si crees que esto es un error, por favor contáctanos a wearecircleup@gmail.com.", icon=":material/notifications:")

    except Exception as e:
        st.error(f"Se produjo un error inesperado: {str(e)}. Por favor, intenta de nuevo o contacta al soporte.", icon=":material/error:")


def entry_registration():
    try:
        data_courses = get_course_data()

        if data_courses.empty:
            st.warning("No hay cursos disponibles en este momento. Por favor, intenta más tarde.", icon=":material/calendar_clock:")
            return

        user_age_category: str = CategoryUtils().age_to_category(st.session_state.user_auth.dob)
        age_appropriate_courses = filter_age_appropriate_courses(data_courses, user_age_category)
        
        if not age_appropriate_courses.empty:
            st.write("Entonces, revisemos los siguientes pasos para explorar y registrarte en los cursos.")

            st.info("**Paso 1** Elige una Categoría", icon=":material/self_improvement:")
            category_options: List[str] = get_uniques(age_appropriate_courses, 'course_categories')
            selected_category: Optional[str] = st.selectbox(
                "Explora nuestras categorías y elige la que más te interese",
                options=category_options,
                index=None,
                placeholder='Seleccionar Categoría'
            )

            if selected_category:
                st.write("Explora los cursos de tu categoría elegida. Cada uno ofrece una experiencia única de aprendizaje.")
                st.info("**Paso 2** Seleccionar Curso", icon=":material/self_improvement:")
                filtered_courses = age_appropriate_courses[age_appropriate_courses['course_categories'].str.contains(selected_category, na=False)]
                course_options: List[str] = filtered_courses['course_name'].tolist()
                selected_course: Optional[str] = st.selectbox(
                    "Ahora, echa un vistazo a los cursos disponibles en esta categoría:",
                    options=course_options,
                    index=None,
                    placeholder='Seleccionar Curso'
                )

                if selected_course:
                    selected_request = filtered_courses[filtered_courses['course_name'] == selected_course].iloc[0]
                    if selected_course not in st.session_state.lock_courses:
                        if not selected_request.empty:
                            st.write("Aquí tienes toda la información detallada sobre el curso seleccionado. Revisa cuidadosamente los objetivos, el perfil del instructor y los requisitos para asegurarte de que este curso sea el adecuado para ti.")
                            course_description(selected_request)

                            utils = CategoryUtils()

                            reminder = f"""El curso de {selected_request['course_name']} {
                                'será en modalidad ' + selected_request['modality_proposal'].lower() 
                                if selected_request['modality_proposal'].lower() == 'virtual' 
                                else f"se realizará en {selected_request['place_proposal']}, {selected_request['city_proposal']}"
                            }. Está diseñado para participantes de {selected_request['allowed_age']}{
                                f" y es recomendable que cuentes con {selected_request['prior_knowledge'].lower()}" 
                                if selected_request['prior_knowledge'].lower() != 'no aplica' 
                                else ''
                            }. Seremos un grupo de {selected_request['min_audience']} a {selected_request['max_audience']} personas{
                                f", así que no olvides {selected_request['tech_resources'].lower()}" 
                                if selected_request['tech_resources'].lower() != 'no aplica' 
                                else ''
                            }. Este curso se encuentra dentro de las categorías de {selected_request['course_categories']}."""
                            
                            data_collection = {
                                'enrolled_at': utils.get_current_date(),
                                'week': utils.date_to_day_of_week(),
                                'hour_range': utils.time_to_category(),
                                'cloud_id': None,
                                'cloud_id_user': st.session_state.user_auth.cloud_id,
                                'cloud_id_volunteer': selected_request['cloud_id_volunteer'],
                                'cloud_id_course': selected_request['cloud_id_course'],
                                'first_name': st.session_state.user_auth.first_name,
                                'last_name': st.session_state.user_auth.last_name,
                                'email': st.session_state.user_auth.email,
                                'start_date': selected_request['start_date'],
                                'summary': reminder,
                                'attendance_record': 0,
                                'email_notice': 'Pending',
                                'email_reminder': 0,
                                'status': 'Enrolled',
                                'last_change': utils.get_current_date()
                            }
                            
                            if st.button('Registrarse', use_container_width=True, type='primary'):
                                enrollment_notice(data_collection, selected_course)
                                st.success(st.session_state.confirmation_message, icon=":material/data_check:")

                    else:
                        st.success(
                            f"¡Genial! Ya estás en :green[**{selected_course}**]. Revisa tu email para actualizaciones. Si no los recibes, escribe a wearecircleup@gmail.com. Mientras tanto, explora más cursos en :green[**Circle Up Community**].",
                            icon=":material/concierge:")
                else:
                    st.info("Selecciona un curso para ver más detalles. Cada curso ha sido cuidadosamente diseñado para ofrecerte una experiencia de aprendizaje enriquecedora.", icon=":material/library_books:")
            else:
                st.info("Explora nuestras categorías para encontrar el tema que más te apasione. Tenemos una amplia gama de opciones para satisfacer diversos intereses y niveles de experiencia.", icon=":material/explore:")
        else:
            st.warning("Por el momento no tenemos cursos disponibles para tu rango de edad, pero no te preocupes. Estamos trabajando constantemente para ampliar nuestra oferta. Te avisaremos tan pronto como tengamos opciones adecuadas para ti.", icon=":material/notifications:")

    except Exception as e:
        st.error(f"Error al procesar la inscripción: {str(e)}")

def parental_update(connector: Firestore, cloud_id: str):
    try:
        connector.update_document('users_collection', cloud_id, {'parental_consent': 'Authorized'})
        with st.spinner(":material/sync: Concediendo accesos... Un momento"):
            time.sleep(4)

    except firebase_admin.exceptions.FirebaseError as e:
        st.error(f"Error de Firebase: {str(e)}")
        return

    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return

    st.success("La solicitud ha sido aprobada exitosamente.")
    st.rerun()

def parental_logs(link_auth=None):
    utils = CategoryUtils()
    return [
        utils.get_current_date(),
        utils.date_to_day_of_week(),
        utils.time_to_category(),
        st.session_state.user_auth.first_name,
        st.session_state.user_auth.last_name,
        utils.age_to_category(st.session_state.user_auth.dob),
        st.session_state.user_auth.email,
        st.session_state.user_auth.user_role,
        st.session_state.user_auth.city_residence,
        st.session_state.user_auth.cloud_id,
        link_auth]

def main():
    try:
        st.warning(":orange[**Duración Cursos**] :orange[**2 horas maximo**], sesión exclusiva / :orange-background[Cupos limitados]", icon=":material/attach_file:")

        if 'lock_courses' not in st.session_state:
            st.session_state.lock_courses = lock_data('course_name')

        if 'confirmation_message' in st.session_state:
            st.success(st.session_state.confirmation_message, icon=":material/data_check:")
            # del st.session_state.confirmation_message

        if not st.session_state.show_explore and not st.session_state.show_manage:
            st.info("**Paso 0:** :blue-background[¿Qué te gustaría hacer?] En :blue[**Explorar Cursos**] puedes registrarte en cursos que te interesen, y en :blue[**Gestionar Inscripciones**] puedes revisar tus cursos inscritos o cancelar tu participación.", icon=":material/self_improvement:")

            col1, col2 = st.columns(2)
            with col1:
                st.button(":material/travel_explore: Explorar Cursos", key="discover_courses", type='primary', 
                        use_container_width=True, on_click=show_explore)
            with col2:
                st.button(":material/bookmarks: Gestionar Inscripciones", key="manage_registrations", type='secondary', 
                        use_container_width=True, on_click=show_manage)

        if st.session_state.show_explore:
            entry_registration()

        if st.session_state.show_manage:
            entry_unregister()

    except Exception as e:
        st.error(f"Se ha producido un error inesperado: {str(e)}")

def parental_menu():
    st.info(
            f"Hola {' '.join([item.capitalize() for item in st.session_state.user_auth.first_name.split(' ')])}, "
            "Circle Up Community tiene un único requisito importante para participantes menores de 18 años, una :blue-background[autorización] de tu representante. Es un proceso sencillo que solo se hace una vez"
            "\n\n• Descarga y completa el [Consentimiento Informado Autorización Menores](https://drive.google.com/file/d/1XQbCa3bo46WBEZ1jM4vYJC06Ts_bJ9vr) con tu representante."
            "\n\n• Sube el archivo junto con una copia del documento de identidad del mismo representante en un solo [archivo PDF](https://www.ilovepdf.com/es/unir_pdf). Al cargar este documento, tendrás :blue-background[acceso] libre a Circle Up Community.",
            icon=":material/fingerprint:"
        )

    google_blobs = GoogleBlobs('1Idxz8Iyx67XNXsw-kOVMJK__as8vOu6q')

    with st.form("upload_form"):
        uploaded_file = st.file_uploader("Documento Firmado Drive", type=['pdf'])
        
        data_sharing = st.checkbox("Confirmo que la información proporcionada es verídica y precisa, y que el archivo cargado es un [único PDF](https://www.ilovepdf.com/es/unir_pdf) que contiene la [autorización firmada](https://drive.google.com/file/d/1XQbCa3bo46WBEZ1jM4vYJC06Ts_bJ9vr) y la :blue-background[fotocopia de la cédula] del representante legal.")
        
        submit_button = st.form_submit_button(":material/send: Enviar Consentimiento Informado",use_container_width=True)
        
        if submit_button:
            if uploaded_file is not None and data_sharing == True:
                new_filename = f"{st.session_state.user_auth.email}-{st.session_state.user_auth.cloud_id}.pdf"
                uploaded_file.name = new_filename
                with st.spinner("Enviando archivo..."):
                    st.session_state.sign_document = cached_upload_file(google_blobs, uploaded_file)
                    time.sleep(3)
                    st.session_state.user_auth.parental_consent = 'Authorized'
                    st.session_state.sign_document = parental_logs(st.session_state.sign_document)
                    parental_update(connector(),st.session_state.user_auth.cloud_id)
                    time.sleep(1)
                    send_to_sheets(st.session_state.sign_document,'1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM','Parental Concent')
                    time.sleep(1)
            else:
                st.info("Por favor, carga el archivo y confirma la información.", icon=":material/upload_file:")

try:
    st.title("Explora Nuestros Cursos")
    st.write("Bienvenido a nuestra plataforma de aprendizaje. Aquí podrás encontrar cursos diseñados para potenciar tus habilidades y conocimientos.")

    if st.session_state.user_auth.parental_consent in ['Not Applicable','Authorized']:
        if st.button(':material/cloud_sync: Actualizar Inscripciones',use_container_width=True):
                    update_intakes()
        main()
        if st.button(":material/explore: Volver a Explorar", type='primary', use_container_width=True):
            st.session_state.show_manage = False
            st.session_state.show_explore = False

    else:
        parental_menu()

    st.divider()
    if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
        st.switch_page('app.py')
except AttributeError:
    st.switch_page('app.py')

menu()