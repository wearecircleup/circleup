import streamlit as st
from menu import menu
from utils.body import unauthenticate_login
from google.cloud import firestore
import json
from classes.course_class import Course
from classes.enroll_class import Enrollment
from utils.body import succefull_enrollment
import time
from datetime import datetime
from utils.form_options import age_range, topics_of_interest
from utils.body import enrollment_warning,warning_unenroll,unenrolled_confirm,html_banner

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect to app.py if not logged in, otherwise show the navigation menu
welcome_course = """
    Cada curso es el resultado de un meticuloso proceso de :blue[planificación, conceptualización y desarrollo], 
    diseñado para ofrecerte la mejor experiencia educativa. Al pre-inscribirte, no solo das el primer paso hacia un enriquecimiento personal, 
    sino que también contribuyes a dar vida a una idea. ¡Juntos, haremos que cada idea se convierta en una realidad!.  
    """

suggest_enroll = """
Entendemos que comprometerse con un curso requiere tiempo y dedicación. 
Por eso, es crucial que consideres tu capacidad para involucrarte de manera activa, y si es posible, contribuir o 
tomar un rol de liderazgo dentro del curso.     

:blue[**Recuerda:**] los espacios son limitados. Reservar un lugar y no participar significa 
privar a otra persona de la oportunidad de aprender y crecer. ¡Asegúrate de que puedes comprometerte antes de reservar tu espacio!
"""

enrolled_message = """
    ¡Explora esta sección para verificar y cancelar tus preinscripciones en Circle Up ⚫! 
    Aquí encontrarás una variedad de cursos que se adaptan a tus intereses y horarios. 
    Nuestro sistema de gestión de preinscripciones es sencillo y eficiente, 
    permitiéndote hacer cambios según sea necesario.

"""


if 'filter_course' not in st.session_state:
    st.session_state.filter_course = []

if 'unenroll_course_request' not in st.session_state:
    st.session_state.unenroll_course_request = True 

@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db


def enrollmet_container(course):
    enrollment_dict = {
    'user_profile': {   
                    'fullname':st.session_state.user_auth.first_name + ' ' + st.session_state.user_auth.last_name,
                    'email':st.session_state.user_auth.email,
                    'city_residence':st.session_state.user_auth.city_residence, 
                    'skills': st.session_state.user_auth.skills,
                    'how_to_learn': st.session_state.user_auth.how_to_learn,
                    'education_level': st.session_state.user_auth.education_level,
                    'disability': st.session_state.user_auth.disability,
                    'ethnic_affiliation': st.session_state.user_auth.ethnic_affiliation,
                    'nationality': st.session_state.user_auth.nationality,
                    'gender': st.session_state.user_auth.gender,
                    'dob': st.session_state.user_auth.dob
                    },
    'volunteer_profile': {
                    'fullname':course.user_profile['fullname'],
                    'email':course.user_profile['email'],
                    'education_experience':course.user_profile['education_experience']
                    },

    'course_content': {
                    'course_name':course.course_name,
                    'course_description':course.course_description,
                    'min_audience':course.min_audience,
                    'max_audience':course.max_audience,
                    'target_population':course.target_population,
                    'date_specs':course.date_specs,
                    'course_place':course.course_place
            }
    }

    return enrollment_dict


def course_description(course):
    # Sección de datos del curso
    st.write('**Circle Up ⚫ Propuesta**')

    with st.container(height=400):
        st.write(f"¡Bienvenido **@{st.session_state.role_synonym}**! Aprender es solo el comienzo!")
        st.text_input(label='Nombre del Curso', value=course.course_name, key='__course_name', help='Proporciona un nombre claro y atractivo para tu curso.',disabled=True)
        st.text_area(label='Descripción del Curso', value=course.course_description, key='__course_description', help='Describe brevemente el contenido y los objetivos del curso.',disabled=True)
        st.text_input(label='Experiencia Academica @Nomads',value=course.user_profile['education_experience'],disabled=True)

    with st.container(height=110):
        layout = st.columns([1,1,3])
        layout[0].number_input(label='Aforo Mínimo',min_value=5,max_value=15, step=1,value=course.min_audience, key='__min_audience', help='Indica el número mínimo de participantes necesarios para iniciar el curso.',disabled=True)
        layout[1].number_input(label='Aforo Máximo',min_value=15,max_value=50, step=1,value=course.max_audience ,key='__max_audience', help='Establece la capacidad máxima de participantes para garantizar una experiencia óptima.',disabled=True)
        layout[2].multiselect(label='Perfil Demográfico', default=course.target_population, options=age_range, key='__target_population', help='Identifica el grupo demográfico al que está dirigido el curso.',disabled=True)
    with st.container(height=110):
        layout = st.columns([4,4])
        layout[0].text_input(label='Fechas/Horarios',value=course.date_specs,disabled=True)
        layout[1].text_input(label='Lugar/Tipo',value=course.course_place,disabled=True)

@st.cache_data(ttl=10,max_entries=2,show_spinner=False)
def courses_stream():
    stream_data = Course().available_courses(firestore_client())
    return stream_data

def course_enrollment(course):
    # Sección de datos del curso
    st.write('**Circle Up ⚫ Propuesta**')

    with st.container(height=250):
        st.text_input(label='Nombre del Curso', value=course['course_name'], key='enroll_course',help='Proporciona un nombre claro y atractivo para tu curso.',disabled=True)
        st.text_area(label='Descripción del Curso', value=course['course_description'],key='enroll_desc', help='Describe brevemente el contenido y los objetivos del curso.',disabled=True)

    with st.container(height=110):
        layout = st.columns([4,4])
        layout[0].text_input(label='Fechas/Horarios',value=course['date_specs'],disabled=True,key='enroll_date')
        layout[1].text_input(label='Lugar/Tipo',value=course['course_place'],disabled=True,key='enroll_place')

@st.cache_data(ttl=10,max_entries=2,show_spinner=False)
def courses_stream():
    stream_data = Course().available_courses(firestore_client())
    return stream_data


def retrive_course(course):
    stream_data = courses_stream()
    if len(stream_data) > 0 and stream_data is not None:
        select_document = [value for key,value in stream_data.items() if value['course_name'] == course][0]
        instance = Course(**select_document)
        return instance
    else:
        st.markdown('Circle Up ⚫ Elige Aprender!')


def age_categorization(dob):
    try:
        dob_str = datetime.strptime(dob, '%d-%m-%Y')
        age = datetime.now().year - dob_str.year
        if 14 <= age <= 17:
            return "14-17 años"
        elif 18 <= age <= 21:
            return "18-21 años"
        elif 22 <= age <= 35:
            return "22-35 años"
        elif 36 <= age <= 50:
            return "36-50 años"
        elif 51 <= age <= 65:
            return "51-65 años"
        elif 66 <= age <= 80:
            return "66-80 años"
        else:
            return "No Aplica"
    except ValueError:
        return "No Aplica"

def enroll_user_now(enroll_request,courses_volunteer):
    if enroll_request is not None and len(enroll_request) > 0:
        instance = Enrollment(**enroll_request)
        target_age = age_categorization(st.session_state.user_auth.dob)
        course = enroll_request['course_content']['course_name']
        email = courses_volunteer[course]

        auth_message = instance.enroll_authentication(target_age,email,course,firestore_client())
        
        auth_one = auth_message['enrolled'] == False
        auth_two = auth_message['target_age'] == True
        auth_three = auth_message['audience'] is not None
        auth_pipeline = [auth_one,auth_two,auth_three]
        if not auth_one:
            enrollment_warning('one')
        elif not auth_two:
            enrollment_warning('two')
        elif not auth_three:
            enrollment_warning('three')
        elif all(auth_pipeline):
            instance.upload_enrollment(auth_message['audience'],firestore_client())
            succefull_enrollment(instance.course_content['course_name'])


def category_onchange(courses_categories,courses_volunteer):
    filtered_courses = [course for course,categories in courses_categories.items() if st.session_state._filter_category in categories]
    filtered_courses = set(filtered_courses)
    course = st.selectbox(label='Filtrar Curso',key='_picked_course',index=None,placeholder='Seleccionar Curso',options=filtered_courses)
    if course is not None:
        course_instance = retrive_course(course)
        course_description(course_instance)
        enrollment_ref = enrollmet_container(course_instance)
        st.button(label='Reservar Lugar',use_container_width=True,type="primary",on_click=enroll_user_now,args=[enrollment_ref,courses_volunteer])


def shedule_logic():
    st.subheader(f'¡Courses, @{st.session_state.role_synonym}!')
    
    st.markdown(welcome_course)
    st.subheader('Circle Up ⚫ Pre-Inscripciones')

    st.markdown(suggest_enroll)

    data_courses = courses_stream()
    courses_categories = {data_courses[key]['course_name']:data_courses[key]['course_categories'] for key in list(data_courses.keys())}
    courses_volunteers = {data_courses[key]['course_name']:data_courses[key]['user_profile']['email'] for key in list(data_courses.keys())}
    categories_list = [data_courses[key]['course_categories'] for key in list(data_courses.keys())]
    categories = set([category for lists in categories_list for category  in lists])

    category = st.selectbox(label='Filtrar Categoria | **Elige una opción**',key='_filter_category',index=None,placeholder='Seleccionar Categoría',options=categories)
    if category is not None:
        category_onchange(courses_categories,courses_volunteers)


def is_confirmed_unenroll(course):
    st.session_state.unenroll_course_request = False
    warning_unenroll(course)

def remove_enroll(key,email,course_name):
    if email and course_name and key:
        Enrollment().unrollment(key,email,course_name,firestore_client())
        unenrolled_confirm()
        st.session_state.unenroll_course_request = True

def enrolled_logic():
    st.subheader('Circle Up ⚫ Reservas')
    st.markdown(enrolled_message)
    instance_enrollment = Enrollment().get_enrollments(st.session_state.user_auth.email,firestore_client())


    if len(instance_enrollment) > 0 and instance_enrollment is not None:
        data_courses = courses_stream()
        courses_volunteers = {data_courses[key]['course_name']:data_courses[key]['user_profile']['email'] for key in list(data_courses.keys())}
        
        courses = {enroll['course_content']['course_name']:enroll['user_profile']['email'] for _,enroll in instance_enrollment.items()}
        course = st.selectbox(label='Cursos Pre-Inscritos | **Elige una opción**',options=list(courses.keys()),placeholder='Seleccionar Curso')
        selected_course = [enroll['course_content'] for _,enroll in instance_enrollment.items() if enroll['course_content']['course_name'] == course]
        selected_key = [key for key,enroll in instance_enrollment.items() if enroll['course_content']['course_name'] == course]
        
        course_enrollment(selected_course[0])

        button_layout = st.columns([3,1,2])
        button_layout[0].button(label='Eliminar Recerva',type="primary",on_click=is_confirmed_unenroll,args=[course],use_container_width=True)
        button_layout[2].button(label='Confirmar',type="primary",on_click=remove_enroll,args=[selected_key,course,courses_volunteers[course]],disabled=st.session_state.unenroll_course_request,use_container_width=True)
    else:
        st.info("¡Hey! No tienes nada que borrar en este momento. ¡Anímate a seguir aprendiendo o por que no, haznos saber si quieres unirte a **@Nomads**!", icon="ℹ️")

def authenticated_login_crew():
    st.html(html_banner)
    shedule_logic()
    st.divider()
    enrolled_logic()

def authenticated_login_nomads():
    st.html(html_banner)
    shedule_logic()
    st.divider()
    enrolled_logic()
    # unenroll_logic()

def authenticated_login_sentinel():
    st.html(html_banner)
    shedule_logic()
    st.divider()
    enrolled_logic()

try:
    if st.session_state.user_auth is not None and st.session_state.user_auth.user_status == 'Activo':
        if st.session_state.user_auth.user_role == 'Learner':
            authenticated_login_crew()
        elif st.session_state.user_auth.user_role == 'Volunteer':
            authenticated_login_nomads()
        elif st.session_state.user_auth.user_role == 'Admin':
            authenticated_login_sentinel()
    else: 
        unauthenticate_login(st.session_state.user_auth.user_role,st.session_state.role)
except:
    st.switch_page("app.py")


menu()