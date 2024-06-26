import streamlit as st
from menu import menu
import pandas as pd
import json
import time
from utils.body import (medium_parragraph,psudo_title,unauthenticate_login,
                        warning_empty_data,succeed_proposal,warning_course_changes,
                        succeed_update_course,warning_deletion,deletion_confirm,
                        warning_reupload,html_banner
                        )
from utils.form_options import age_range,topics_of_interest

from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter, Or
from dataclasses import dataclass, asdict
from classes.course_class import Course

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'course_instance' not in st.session_state:
    st.session_state.course_instance = Course() 

if 'course_instance_alter' not in st.session_state:
    st.session_state.course_instance_alter = Course() 

if 'updates_course_confirmation' not in st.session_state:
    st.session_state.updates_course_confirmation = False
    st.session_state.updates_course_request = True

if 'delete_course_confirmation' not in st.session_state:
    st.session_state.delete_course_confirmation = False
    st.session_state.delete_course_request = True

# Redirect to app.py if not logged in, otherwise show the navigation menu
@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

def proposal_course():
    # Sección de datos del curso
    st.write('**Circle Up ⚫ Conceptualización**')

    with st.container(height=320):
        st.write("¡Bienvenido, **@Nómada**! Tu experiencia fortalecerá nuestra búsqueda de conocimiento.")
        st.text_input(label='Nombre del Curso', placeholder='Astronomía', key='_course_name', help='Proporciona un nombre claro y atractivo para tu curso.')
        st.text_area(label='Descripción del Curso',  placeholder='Descubre el Universo junto a expertos en nuestro curso presencial. ¡Explora las maravillas del cosmos en una experiencia única!', key='_course_description', help='Describe brevemente el contenido y los objetivos del curso.')
    
    with st.container(height=350):
        st.write('Es crucial delinear y definir claramente el alcance del curso.')
        layout = st.columns([2, 2])
        layout[0].number_input(label='Aforo Mínimo',min_value=5,max_value=15, step=1,placeholder=15, key='_min_audience', help='Indica el número mínimo de participantes necesarios para iniciar el curso.')
        layout[1].number_input(label='Aforo Máximo',min_value=15,max_value=50, step=1 , placeholder=20, key='_max_audience', help='Establece la capacidad máxima de participantes para garantizar una experiencia óptima.')
        layout[0].text_input(label='Título para Redes Sociales', placeholder='Descubre el Universo', key='_press_title', help='Crea un título inspirador y memorable para promocionar el curso en redes sociales.')
        layout[1].text_input(label='Slogan para Invitar al Público', placeholder='Explora las Estrellas', key='_press_slogan', help='Proporciona un eslogan emocionante que invite a los participantes a unirse a la aventura.')
        layout[0].multiselect(label='Categorías del Curso', placeholder='Selecciona una categoría', options=topics_of_interest, key='_course_categories', help='Elige la categoría principal del curso.')
        layout[1].multiselect(label='Perfil Demográfico', placeholder='Selecciona un perfil', options=age_range, key='_target_population', help='Identifica el grupo demográfico al que está dirigido el curso.')
    
    # Sección de revisión y aprobación
    with st.container(height=200):
        st.write("¡Es hora de preparar nuestras herramientas y trazar el rumbo del viaje!")
        checker = st.columns(3)
        checker[0].checkbox(label='Revisión de Propuesta', key='_proposal_review', help='Solicita la evaluación de la hoja de ruta en nuestro consejo de nómadas.',disabled=True)
        checker[1].checkbox(label='Revisión Pensum', key='_proposal_writing', help='Proporciona detalles por escrito sobre el itinerario y los objetivos del curso.',disabled=True)
        checker[2].checkbox(label='Guía Metodológica', key='_methodology_review', help='Comparte la metodología del curso para garantizar un enfoque efectivo en el aprendizaje.',disabled=True)
        checker[0].checkbox(label='Desarrollo de Material para Clases', key='_subject_memories', help='Prepara materiales didácticos para enriquecer la experiencia de aprendizaje.',disabled=True)
        checker[1].checkbox(label='Aprobación', key='_proposal_approval', help='Obtén la aprobación oficial del curso por parte de las autoridades pertinentes.',disabled=True)
        checker[2].checkbox(label='Confirmación de Horarios/Lugar', key='_allocation', help='Confirma los horarios y lugares para la realización del curso.',disabled=True)


def proposal_update_course(course):
    # Sección de datos del curso
    st.write('**Circle Up ⚫ Propuesta**')

    with st.container(height=320):
        st.write("¡Bienvenido, **@Nómada**! Tu experiencia fortalecerá nuestra búsqueda de conocimiento.")
        st.text_input(label='Nombre del Curso', value=course.course_name, key='__course_name', help='Proporciona un nombre claro y atractivo para tu curso.')
        st.text_area(label='Descripción del Curso', value=course.course_description, key='__course_description', help='Describe brevemente el contenido y los objetivos del curso.')
    
    with st.container(height=350):
        st.write('Es crucial delinear y definir claramente el alcance del curso.')
        layout = st.columns([2, 2])
        layout[0].number_input(label='Aforo Mínimo',min_value=5,max_value=15, step=1,value=course.min_audience, key='__min_audience', help='Indica el número mínimo de participantes necesarios para iniciar el curso.')
        layout[1].number_input(label='Aforo Máximo',min_value=15,max_value=50, step=1,value=course.max_audience ,key='__max_audience', help='Establece la capacidad máxima de participantes para garantizar una experiencia óptima.')
        layout[0].text_input(label='Título para Redes Sociales', value=course.press_title, key='__press_title', help='Crea un título inspirador y memorable para promocionar el curso en redes sociales.')
        layout[1].text_input(label='Slogan para Invitar al Público', value=course.press_slogan, key='__press_slogan', help='Proporciona un eslogan emocionante que invite a los participantes a unirse a la aventura.')
        layout[0].multiselect(label='Categorías del Curso',default=course.course_categories, options=topics_of_interest, key='__course_categories', help='Elige la categoría principal del curso.')
        layout[1].multiselect(label='Perfil Demográfico', default=course.target_population, options=age_range, key='__target_population', help='Identifica el grupo demográfico al que está dirigido el curso.')
    
    # Sección de revisión y aprobación
    with st.container(height=200):
        st.write("¡Es hora de preparar nuestras herramientas y trazar el rumbo del viaje!")
        checker = st.columns(3)
        checker[0].checkbox(label='Revisión de Propuesta', value=course.course_prerequisites['proposal_review'],key='__proposal_review', help='Solicita la evaluación de la hoja de ruta en nuestro consejo de nómadas.',disabled=True)
        checker[1].checkbox(label='Revisión Pensum',value=course.course_prerequisites['proposal_writing'], key='__proposal_writing', help='Proporciona detalles por escrito sobre el itinerario y los objetivos del curso.',disabled=True)
        checker[2].checkbox(label='Guía Metodológica',value=course.course_prerequisites['methodology_review'], key='__methodology_review', help='Comparte la metodología del curso para garantizar un enfoque efectivo en el aprendizaje.',disabled=True)
        checker[0].checkbox(label='Desarrollo de Material para Clases',value=course.course_prerequisites['subject_memories'], key='__subject_memories', help='Prepara materiales didácticos para enriquecer la experiencia de aprendizaje.',disabled=True)
        checker[1].checkbox(label='Aprobación',value=course.course_prerequisites['proposal_approval'], key='__proposal_approval', help='Obtén la aprobación oficial del curso por parte de las autoridades pertinentes.',disabled=True)
        checker[2].checkbox(label='Confirmación de Horarios/Lugar',value=course.course_prerequisites['allocation'], key='__allocation', help='Confirma los horarios y lugares para la realización del curso.',disabled=True)


def course_instanciation():
    course_attributes = {
        'user_profile':{
                'fullname':st.session_state.user_auth.first_name + ' ' + st.session_state.user_auth.last_name,
                'email':st.session_state.user_auth.email,
                'phone_number':st.session_state.user_auth.phone_number,
                'id_user':st.session_state.user_auth.id_user,
                'user_role':st.session_state.user_auth.user_role,
                'user_status':st.session_state.user_auth.user_status,
                'education_experience':st.session_state.user_auth.education_experience
                },
        'course_name':st.session_state._course_name, 
        'course_description':st.session_state._course_description,
        'min_audience':st.session_state._min_audience,
        'max_audience':st.session_state._max_audience,
        'press_title':st.session_state._press_title,
        'press_slogan':st.session_state._press_slogan,
        'course_categories':st.session_state._course_categories,
        'target_population':st.session_state._target_population,
        'course_prerequisites': {
                                'proposal_review':st.session_state._proposal_review,
                                'proposal_writing':st.session_state._proposal_writing,
                                'methodology_review':st.session_state._methodology_review,
                                'subject_memories':st.session_state._subject_memories,
                                'proposal_approval':st.session_state._proposal_approval,
                                'allocation':st.session_state._allocation
                                } 
    }

    return course_attributes

def retrieve_manage_form():
    course_attributes = {
        'course_name':st.session_state.__course_name, 
        'course_description':st.session_state.__course_description,
        'min_audience':st.session_state.__min_audience,
        'max_audience':st.session_state.__max_audience,
        'press_title':st.session_state.__press_title,
        'press_slogan':st.session_state.__press_slogan,
        'course_categories':st.session_state.__course_categories,
        'target_population':st.session_state.__target_population
    }

    return course_attributes


def form_course_submition():
    course_consolidation = course_instanciation()
    if all(course_consolidation.values()):
        st.session_state.course_instance.update_course(**course_consolidation)
        course = course_consolidation['course_name']
        mail = course_consolidation['user_profile']['email']
        try:
            st.session_state.course_instance.upload_course(firestore_client(),course,mail)
            succeed_proposal(st.session_state.course_instance.course_name)
        except:
            warning_reupload()
    else: warning_empty_data()

def form_course_updates():
    app_email = st.session_state.user_auth.email
    app_user_id = st.session_state.user_auth.id_user
    app_role = st.session_state.user_auth.user_role
    innner_intance = Course().search_courses(app_email,app_user_id,app_role,firestore_client())
    return innner_intance




def is_confirmed(cls_course,app_form):
    changes = cls_course.catch_course_updates(**app_form)
    if len(changes) > 0:
        warning_course_changes(changes)
        st.session_state.updates_course_request = False
    else:
        st.session_state.updates_course_request = True
    
def is_confirmed_delete(course):
    st.session_state.delete_course_request = False
    warning_deletion(course)


def update_now(cls_course,app_form):
    cls_course.update_course(**app_form)
    cls_course.update_firestore_course(firestore_client())
    succeed_update_course(st.session_state.user_auth.first_name.capitalize())
    st.session_state.updates_course_request = True

def delete_now(id):
    Course().delete_course(id,firestore_client())
    deletion_confirm()


@st.cache_data(ttl=10,max_entries=2,show_spinner=False)
def retrive_user_courses(app_email,app_user_id,app_role):
    available_stream = Course().search_courses(app_email,app_user_id,app_role,firestore_client())
    return available_stream


def update_logic():
    app_email = st.session_state.user_auth.email
    app_user_id = st.session_state.user_auth.id_user
    app_role = st.session_state.user_auth.user_role
    available_stream = retrive_user_courses(app_email,app_user_id,app_role)
    if all(available_stream.keys()) and len(available_stream) > 0:
        courses = {available_stream[course_id]['course_name']:course_id for course_id in list(available_stream.keys())}   
        st.selectbox(label='Filtrar Curso',placeholder='Seleccionar Curso',options=list(courses.keys()),key='update_selection')
        chosen_course = available_stream[courses[st.session_state.update_selection]] 
        instance_document = Course(**chosen_course)
        instance_document.cloud_id = courses[st.session_state.update_selection]
        
        proposal_update_course(instance_document)
        updates_to_edit = retrieve_manage_form()
        button_layout = st.columns([3,1,2])
        button_layout[0].button(label='Verificar Cambios',type="primary",on_click=is_confirmed,args=[instance_document,updates_to_edit],disabled=st.session_state.updates_course_confirmation,use_container_width=True)
        button_layout[2].button(label='Guardar Cambios',type="primary",on_click=update_now,args=[instance_document,updates_to_edit],disabled=st.session_state.updates_course_request,use_container_width=True)

    else:
        st.info('¡Aún no has compartido ninguna propuesta! ¡Anímate y comparte tu conocimiento con todos!',icon='ℹ️')
    
    
def delete_logic():
    app_email = st.session_state.user_auth.email
    app_user_id = st.session_state.user_auth.id_user
    app_role = st.session_state.user_auth.user_role
    available_stream = retrive_user_courses(app_email,app_user_id,app_role)
    if all(available_stream.keys()) and len(available_stream) > 0:
        courses = {available_stream[course_id]['course_name']:course_id for course_id in list(available_stream.keys())}   
        st.selectbox(label='Filtrar Curso',placeholder='Seleccionar Curso',options=list(courses.keys()),key='delete_selection')
        chosen_course = available_stream[courses[st.session_state.delete_selection]] 
        instance_document = Course(**chosen_course)
        instance_document.cloud_id = courses[st.session_state.delete_selection]
        
        button_layout = st.columns([3,1,2])
        button_layout[0].button(label=f'Eliminar',type="primary",on_click=is_confirmed_delete,args=[instance_document.course_name],disabled=st.session_state.delete_course_confirmation,use_container_width=True)
        button_layout[2].button(label='Confirmar',type="primary",on_click=delete_now,args=[instance_document.cloud_id],disabled=st.session_state.delete_course_request,use_container_width=True)

    else:
        st.info('¡Aún no has compartido ninguna propuesta! ¡Anímate y comparte tu conocimiento con todos!',icon='ℹ️')
    
def authenticated_login_nomads():
    st.html(html_banner)
    st.subheader(f'¡Hola, @{st.session_state.user_auth.first_name.capitalize()}!')
    welcome_nomad = """
    Los Nomads son creadores y forman el núcleo de **Circle Up**. 
    Para nosotros, compartir conocimiento es una pasión. 
    Siempre encontramos formas de ofrecer una perpectiva diferente.
    Prepárate para sumergirte en un mundo de enseñanza. ¡Juntos vamos a aprender mucho!
    """

    welcome = """
    Descubre **Circle Up ⚫**, un espacio dedicado al desarrollo de propuestas de cursos cortos. 
    :blue[¿Tienes una idea para un curso corto?] ¡Genial! Completa el formulario a continuación. 
    Nos pondremos en contacto contigo para avanzar en las siguientes etapas de evaluación, :blue[¡sin complicaciones!].
    Nos encargaremos del resto. Prepárate para compartir tu conocimiento y habilidades con quienes más lo necesitan, 
    te aseguramos que será una experiencia gratificante!.
    """
    
    st.markdown(f"¿Sabías que perteneces a la tribu **{st.session_state.role_synonym}**? ¡Es genial tenerte con nosotros! {welcome_nomad}")
    st.subheader('Envia tu Curso/Propuesta')
    st.markdown(welcome)

    with st.expander(label='Espacio Creativo | Haz clic aquí para **expandir** o **contraer**'):
        with st.form(key='proposal_request',border=False):
            proposal_course()
            st.form_submit_button(label='Enviar Propuesta',type="primary",on_click=form_course_submition)  

    st.subheader('Gestiona Tus Propuestas')
    update_course_message = """
    A continuación, podrás actualizar o eliminar tus cursos propuestos. 
    Además, podrás verificar su estado y revisar tus ideas plasmadas en cursos anteriores, incluyendo títulos y metodologías. 
    Sea cual sea el caso, esta sección te permitirá realizar los ajustes que necesites. 
    Si tienes alguna duda, ¡solo levanta la mano!
    """

    st.markdown(update_course_message)
    with st.expander(label='Gestión de Cursos | Haz clic aquí para **expandir** o **contraer**'):
        update_logic()

    st.subheader('Elimar Propuesta')
    delete_course_message = """
    Esta sección te permite eliminar cualquier propuesta que hayas creado, independientemente del motivo. Tanto la creación como la eliminación de propuestas
    serán notificadas al administrador para su manejo adecuado. La única condición para que puedas eliminar tu propuesta es que no se encuentre en la fase
    de Confirmación de Horarios/Lugar o que incluso esa fase haya sido aprobada.
    """

    st.markdown(delete_course_message)
    with st.expander(label='Eliminar Cursos | Haz clic aquí para **expandir** o **contraer**'):
        delete_logic()
    

def authenticated_login_sentinel():
    st.html(html_banner)
    pass

try: 
    if st.session_state.user_auth is not None and st.session_state.user_auth.user_status == 'Activo':
        if st.session_state.user_auth.user_role == 'Learner':
            unauthenticate_login(st.session_state.user_auth.user_role)
        elif st.session_state.user_auth.user_role == 'Volunteer':
            authenticated_login_nomads()
        elif st.session_state.user_auth.user_role == 'Admin':
            authenticated_login_sentinel()
    else: 
        unauthenticate_login(st.session_state.user_auth.user_role)
except:
    st.switch_page("app.py")


menu()