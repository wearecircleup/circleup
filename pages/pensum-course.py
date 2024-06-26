import datetime
import streamlit as st
from menu import menu
import pandas as pd
from dataclasses import dataclass, asdict
from utils.body import (warning_empty_data,unauthenticate_login,pensum_confirmation,
                        warning_profile_changes,succeed_update_profiles,
                        html_banner,pensum_email_sent)
from utils.form_options import topics_of_interest, age_range
import json
from google.cloud import firestore
import time
import anthropic
from classes.anthropic_agent import evaluate_proposal_langchain
from classes.email_class import Email


st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'pensum_fields_validation' not in st.session_state:
    st.session_state.pensum_fields_validation = False
if 'pensum_anthropic_review' not in st.session_state:
    st.session_state.pensum_anthropic_review = True
if 'catche_claude' not in st.session_state:
    st.session_state.catche_claude = None
if 'catche_proposal' not in st.session_state:
    st.session_state.catche_proposal = None
if 'expander_pensum' not in st.session_state:
    st.session_state.expander_pensum = True
if 'expander_claude' not in st.session_state:
    st.session_state.expander_claude = False
if 'send_email_button' not in st.session_state:
    st.session_state.send_email_button = True
    


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
def data_anthropic(proposal):
    if proposal is not None:    
        # claude_review = Rubric().evaluate_proposal(proposal,anthropic_client())
        claude_review = evaluate_proposal_langchain(proposal,anthropic_client())
        return claude_review


st.html(html_banner)

def pensum_form():

    with st.container():
        st.markdown('#### Información General')
        st.text_input(label='Nombre del curso',placeholder='Programación Creativa con Scratch',help='¿Cómo se llamará tu curso?',key='_pensum_name')
        gn_cols = st.columns([2,2])
        gn_cols[0].selectbox(label='Área temática',index=None,options=topics_of_interest,help='¿A qué área del conocimiento pertenece?',key='_knowledgebase_area')
        gn_cols[1].selectbox(label='Modalidad',index=None,options=['Presencial','Virtual','Híbrido'],help='¿Será presencial, virtual o híbrido?',key='_modality')
        gn_cols[0].number_input(label='Número de sesiones',min_value=1,max_value=4,step=1,help='¿En cuántas sesiones se dividirá el curso?',key='_num_sessions')
        gn_cols[1].number_input(label='Duración/Sesión',min_value=1,max_value=2,step=1,help='¿Cuántas horas durará cada sesión?',key='_hours_per_session')
        st.multiselect(label='Público objetivo',default=None,options=age_range,help='¿A quién va dirigido el curso?',key='_target_pop')

    with st.container():
        st.markdown('#### Objetivos de Aprendizaje')
        key_objective_placeholder = """Desarrollar el pensamiento computacional y la creatividad de los participantes a través de la creación de proyectos interactivos con Scratch.
        """
        key_result_placeholder = """1. Comprender los conceptos básicos de la programación (secuencias, bucles, condicionales). 2. Utilizar Scratch para crear animaciones, juegos y historias interactivas.
        """

        st.text_area(label='Objetivo general',placeholder=key_objective_placeholder,help='¿Qué quieres que los participantes logren al finalizar el curso?',key='_key_objective')
        st.text_area(label='Objetivos específicos',placeholder=key_result_placeholder,help='¿Qué conocimientos, habilidades o actitudes específicas adquirirán los participantes?',key='_key_results')

    st.write('Estructura del Curso')

    topic_placeholder = "Introducción a Scratch"
    content_placeholder = """1. Interfaz de Scratch; 2. Bloques básicos; 3. Movimiento y apariencia de objetos
    """
    activities_placeholder = """1. Crear un personaje y hacerlo moverse; 2. Cambiar el fondo y agregar sonidos
    """
    materials_placeholder = """1. Computador con Scratch; 2. Proyector
    """

    with st.container():
        st.markdown('#### Sesión Uno')
        st.text_input(label='Tema',placeholder=topic_placeholder,help='¿Cuál es el tema principal de la primera sesión?',key='_topic1')
        st.text_area(label='Contenido',placeholder=content_placeholder,help='¿Qué contenidos específicos se abordarán?',key='_content1')
        st.text_area(label='Actividades',placeholder=activities_placeholder,help='¿Qué actividades realizarán los participantes?',key='_activities1')
        st.text_area(label='Materiales',placeholder=materials_placeholder,help='¿Qué materiales se necesitarán?',key='_materials1')

    with st.container():
        st.markdown('#### Sesión Dos')
        st.text_input(label='Tema',placeholder=topic_placeholder,help='¿Cuál es el tema principal de la primera sesión?',key='_topic2')
        st.text_area(label='Contenido',placeholder=content_placeholder,help='¿Qué contenidos específicos se abordarán?',key='_content2')
        st.text_area(label='Actividades',placeholder=activities_placeholder,help='¿Qué actividades realizarán los participantes?',key='_activities2')
        st.text_area(label='Materiales',placeholder=materials_placeholder,help='¿Qué materiales se necesitarán?',key='_materials2')

    with st.container():
        st.markdown('#### Sesión Tres')
        st.text_input(label='Tema',placeholder=topic_placeholder,help='¿Cuál es el tema principal de la primera sesión?',key='_topic3')
        st.text_area(label='Contenido',placeholder=content_placeholder,help='¿Qué contenidos específicos se abordarán?',key='_content3')
        st.text_area(label='Actividades',placeholder=activities_placeholder,help='¿Qué actividades realizarán los participantes?',key='_activities3')
        st.text_area(label='Materiales',placeholder=materials_placeholder,help='¿Qué materiales se necesitarán?',key='_materials3')

    with st.container():
        st.markdown('#### Sesión Cuatro')
        st.text_input(label='Tema',placeholder=topic_placeholder,help='¿Cuál es el tema principal de la primera sesión?',key='_topic4')
        st.text_area(label='Contenido',placeholder=content_placeholder,help='¿Qué contenidos específicos se abordarán?',key='_content4')
        st.text_area(label='Actividades',placeholder=activities_placeholder,help='¿Qué actividades realizarán los participantes?',key='_activities4')
        st.text_area(label='Materiales',placeholder=materials_placeholder,help='¿Qué materiales se necesitarán?',key='_materials4')

    with st.container():
        st.markdown('#### Metodología')
        st.text_input(label='Enfoque pedagógico',placeholder='prendizaje activo y colaborativo.',help='¿Qué enfoque utilizarás para facilitar el aprendizaje?',key='_learning_approach')
        st.text_area(label='Estrategias de enseñanza',placeholder='Demostraciones prácticas.',help='¿Qué técnicas y actividades utilizarás para enseñar los contenidos?',key='_learning_strategy')
        st.text_area(label='Recursos didácticos',placeholder='Tutoriales interactivos de Scratch.',help='¿Qué materiales y herramientas utilizarás para apoyar el aprendizaje?',key='_learning_resources')

    with st.container():
        st.markdown('#### Evaluación')
        st.text_area(label='Criterios de evaluación',placeholder='Participación activa en las actividades',help='¿Cómo evaluarás el aprendizaje de los participantes?',key='_learning_assessment')

@st.experimental_dialog("Detalles de la Métrica")
def show_metric_details(criterio, puntaje, comentario):
    st.subheader(f"{criterio} - Puntuación: {puntaje}/5")
    st.progress(puntaje / 5)
    st.write(f"**Descripción:** {criterio}")
    st.write(f"**Comentario:** {comentario}")
    if puntaje < 4:
        if puntaje == 3:
            st.warning("Este aspecto necesita atención. Considere implementar las sugerencias proporcionadas.")
        else:
            st.error("Este punto requiere una revisión significativa. Es crucial abordar las áreas mencionadas.")
    else:
        st.success("Este aspecto está bien desarrollado. Mantener el buen trabajo.")


def main(data):
    # Cálculo de la puntuación total
    total_score = sum(v[0] for v in data.values())
    
    # Resumen
    st.subheader("Evaluación General")
    st.progress(total_score / 45)
    st.write(f"Puntuación Total: {total_score}/45")
    
    if total_score >= 35:
        st.success("Recomendación: Aprobar la propuesta.")
    else:
        st.error("Recomendación: No aprobar la propuesta.")

    # Botones para cada métrica
    st.subheader("Detalles por Métrica")
    cols = st.columns(3)
    for i, (criterio, (puntaje, comentario)) in enumerate(data.items()):
        with cols[i % 3]:
            if st.button(f"{criterio} - {puntaje}/5", use_container_width=True):
                show_metric_details(criterio, puntaje, comentario)

    total_score = sum(v[0] for v in data.values())
    areas_to_improve = [k for k, v in data.items() if v[0] < 4]
    
    conclusion = f"Puntuación total: {total_score}/45"
    
    if total_score >= 40:
        status = "Excelente"
        color = "green"
    elif total_score >= 35:
        status = "Sólida"
        color = "blue"
    elif total_score >= 30:
        status = "Potencial"
        color = "orange"
    else:
        status = "Necesita revisión"
        color = "red"

    reflective_questions = {
        'Claridad': "¿Cómo podrías explicar tu propuesta de manera más concisa y comprensible?",
        'Relevancia': "¿De qué manera específica tu curso aborda las necesidades actuales de la comunidad de Tocancipá?",
        'Viabilidad': "¿Qué recursos adicionales o ajustes podrían hacer tu propuesta más factible?",
        'Impacto': "¿Cómo podrías medir y maximizar el impacto de tu curso en la comunidad?",
        'Titulo': "¿Qué título alternativo capturaría mejor la esencia y atractivo de tu curso?",
        'Objetivos': "¿Cómo podrías hacer tus objetivos más específicos, medibles y alcanzables?",
        'Idea': "¿Qué aspecto innovador podrías añadir para destacar tu propuesta?",
        'Actividades': "¿Qué actividad práctica adicional reforzaría el aprendizaje de los estudiantes?",
        'Metodología': "¿Cómo podrías incorporar más aprendizaje basado en proyectos en tu metodología?"
    }

    st.write("### Conclusión")
    st.info("La propuesta muestra potencial para impactar positivamente en la comunidad. "
            "Con las mejoras sugeridas, especialmente en las áreas identificadas, este curso podría "
            "convertirse en un valioso recurso para el desarrollo de habilidades en jóvenes.")

    if areas_to_improve:
        for area in areas_to_improve:
            with st.container():
                st.markdown(f':blue[**{area}**]')
                st.write(data[area][1])  # Mostrar el comentario original
                st.info(f"**Reflexiona:** {reflective_questions[area]}")
    else:
        st.success("¡Felicidades! Todas las áreas de tu propuesta están bien desarrolladas.")

    st.write("### Próximos pasos")
    if status == "Excelente":
        st.success("Tu propuesta está lista para ser implementada. Considera cómo puedes mantener y mejorar continuamente la calidad del curso.")
    elif status == "Sólida":
        st.info("Tu propuesta es fuerte. Enfócate en refinar los detalles menores para llevarla al siguiente nivel.")
    elif status == "Potencial":
        st.warning("Tu propuesta tiene bases sólidas. Trabaja en las áreas de mejora identificadas para fortalecerla significativamente.")
    else:
        st.error("Tu propuesta necesita trabajo adicional. Considera repensar algunos aspectos fundamentales y no dudes en buscar orientación adicional.")

def rm_interln(text):
    return text.replace('\n','').replace('-',';')


def pensum_user_data():
    inputs = {
        'pensum_name': st.session_state._pensum_name, 
        'knowledgebase_area': st.session_state._knowledgebase_area, 
        'modality': st.session_state._modality,
        'num_sessions': st.session_state._num_sessions,
        'hours_per_session': st.session_state._hours_per_session,
        'target_pop': st.session_state._target_pop,
        'key_objective': st.session_state._key_objective,
        'key_results': st.session_state._key_results,
        'topic1': st.session_state._topic1,
        'content1': st.session_state._content1,
        'activities1': st.session_state._activities1,
        'materials1': st.session_state._materials1,
        'learning_approach': st.session_state._learning_approach,
        'learning_strategy': st.session_state._learning_strategy,
        'learning_resources': st.session_state._learning_resources,
        'learning_assessment': st.session_state._learning_assessment
    }
    
    field_names = {
        'pensum_name': 'Nombre del curso',
        'knowledgebase_area': 'Área temática',
        'modality': 'Modalidad',
        'num_sessions': 'Número de sesiones',
        'hours_per_session': 'Duración/Sesión',
        'target_pop': 'Público objetivo',
        'key_objective': 'Objetivo general',
        'key_results': 'Objetivos específicos',
        'topic1': '**Tema** (Sesión #1)',
        'content1': '**Contenido** (Sesión #1)',
        'activities1': '**Actividades** (Sesión #1)',
        'materials1': '**Materiales** (Sesión #1)',
        'learning_approach': 'Enfoque pedagógico',
        'learning_strategy': 'Estrategias de enseñanza',
        'learning_resources': 'Recursos didácticos',
        'learning_assessment': 'Criterios de evaluación'
    }

    proposal = f"""
    Título del Curso: {inputs['pensum_name']}

    Área de Conocimiento: {inputs['knowledgebase_area']}
    Modalidad: {inputs['modality']}
    Duración: {inputs['num_sessions']} sesión(es) de {inputs['hours_per_session']} hora(s) cada una
    Público Objetivo: {', '.join(inputs['target_pop'])}

    Objetivo General:
    {rm_interln(inputs['key_objective'])}

    Objetivos Específicos:
    {rm_interln(inputs['key_results'])}

    Estructura del Curso:
    Tema 1: {inputs['topic1']}
    Contenido: {rm_interln(inputs['content1'])}
    Actividades: {rm_interln(inputs['activities1'])}
    Materiales: {rm_interln(inputs['materials1'])}
    
    Tema 2: {st.session_state._topic2}
    Contenido: {rm_interln(st.session_state._content2)}
    Actividades: {rm_interln(st.session_state._activities2)}
    Materiales: {rm_interln(st.session_state._materials2)}

    Tema 3: {st.session_state._topic3}
    Contenido: {rm_interln(st.session_state._content3)}
    Actividades: {rm_interln(st.session_state._activities3)}
    Materiales: {rm_interln(st.session_state._materials3)}

    Tema 4: {st.session_state._topic4}
    Contenido: {rm_interln(st.session_state._content4)}
    Actividades: {rm_interln(st.session_state._activities4)}
    Materiales: {rm_interln(st.session_state._materials4)}

    Metodología:
    Enfoque pedagógico: {rm_interln(inputs['learning_approach'])}
    Estrategias de enseñanza: {rm_interln(inputs['learning_strategy'])}
    Recursos didácticos: {rm_interln(inputs['learning_resources'])}

    Evaluación:
    Criterios de evaluación: {rm_interln(inputs['learning_assessment'])}
    """

    missing_fields = [field_names[key] for key, value in inputs.items() if not value]
    
    if not missing_fields:
        return inputs,proposal
    else:
        missing_fields_str = ", ".join(missing_fields)
        warning_empty_data(missing_fields_str)
        st.session_state.pensum_anthropic_review = True
        return None,None
    

def validate_proposal_input():
    inputs,_ = pensum_user_data()
    if inputs:
        st.session_state.pensum_anthropic_review = False
        pensum_confirmation(inputs)

def send_to_claude():
    inputs,proposal = pensum_user_data()
    st.session_state.pensum_anthropic_review = True
    st.session_state.catche_proposal = proposal
    st.session_state.expander_claude = True
    st.session_state.expander_pensum = False


def write_pensum():
    with st.form('form_pensum'):
        pensum_form()
    button_layout = st.columns([3,1,2])
    button_layout[0].button(label='Pensum Review',type="primary",on_click=validate_proposal_input,disabled=st.session_state.pensum_fields_validation,use_container_width=True)
    button_layout[2].button(label='Anthropic Review',type="primary",on_click=send_to_claude,disabled=st.session_state.pensum_anthropic_review,use_container_width=True)

def send_email_pensum(anthropic_reponse):
    mail = Email()
    mail.send_pensum(recipient=st.session_state.user_auth.email,
                    data = anthropic_reponse, 
                    user_name= st.session_state.user_auth.first_name.capitalize(),
                    proposal=str(st.session_state.catche_proposal))
    pensum_email_sent()
    st.session_state.send_email_button = True


def claude_layout():
    if st.session_state.catche_proposal:
        st.write("En esta sección, podrás ver tu calificación y la retroalimentación detallada proporcionada por Claude para cada uno de los criterios de evaluación. Claude analiza aspectos como la claridad, relevancia, viabilidad, impacto, título, objetivos, idea, actividades y metodología de tu propuesta.")
        st.session_state.catche_claude = data_anthropic(st.session_state.catche_proposal) 
        main(st.session_state.catche_claude)

menu()

try:
    # pensum_assessment = {
    # "Claridad": (4, "La idea general es clara, pero algunos términos podrían ser más específicos. ¿Podrías definir 'enfoque holístico'? ¿Cómo se relaciona esto con los objetivos del curso?"),
    # "Relevancia": (5, "El tema es muy relevante para la audiencia objetivo y aborda una necesidad actual. ¿Qué datos o estudios respaldan esta relevancia? ¿Cómo se alinea con las tendencias del mercado?"),
    # "Viabilidad": (3, "El plan es ambicioso, pero podría haber limitaciones de tiempo y recursos. ¿Cómo se garantizará la disponibilidad de los materiales? ¿Se ha considerado un plan alternativo en caso de contratiempos?"),
    # "Impacto": (4, "El impacto potencial es significativo, pero podría ser más específico. ¿Cómo se medirá el éxito del programa? ¿Qué indicadores clave de rendimiento se utilizarán?"),
    # "Titulo": (5, "El título es atractivo y refleja el contenido del pensum. N/A (No aplica sugerencia de mejora), ¿Se ha considerado un subtítulo para más contexto? ¿Cómo se diferenciará este título de otros similares?"),
    # "Objetivos": (4, "Los objetivos son claros, pero podrían ser más medibles. Reescribir: 'Al finalizar el curso, los participantes serán capaces de identificar y aplicar al menos tres estrategias de marketing digital para aumentar el tráfico web en un 15%.' ¿Cómo se evaluará el logro de estos objetivos? ¿Qué herramientas se utilizarán para medir el progreso?"),
    # "Idea": (5, "La idea central es innovadora y tiene potencial de éxito. ¿Qué investigaciones o experiencias previas respaldan esta idea? ¿Se han identificado posibles riesgos o desafíos?"),
    # "Actividades": (3, "Las actividades propuestas son interesantes, pero podrían ser más variadas. Reescribir: 'Incluir actividades prácticas como simulaciones de campañas de marketing, análisis de casos de estudio y talleres colaborativos.' ¿Cómo se adaptarán las actividades a diferentes estilos de aprendizaje? ¿Se ofrecerá retroalimentación individualizada a los participantes?"),
    # "Metodologia": (4, "La metodología es adecuada, pero podría beneficiarse de más detalles. ¿Se utilizarán herramientas tecnológicas específicas? ¿Cómo se fomentará la participación activa de los estudiantes?"),
    # }

    st.markdown(f"### :blue[**{st.session_state.user_auth.first_name.capitalize()}**], este es tu laboratorio de pruebas o escritura del pensum")

    st.write(f"""
    Es increíble que hayas llegado a este punto de querer escribir algo para tu comunidad. Como ya sabes, el pensum es el lienzo donde se plasman todas las buenas ideas y casos hipotéticos que creemos pueden ser un éxito en Circle Up o en el aprendizaje basado en la comunidad (Community Based Learning). Aquí, podrás estructurar y dar forma a tus propuestas de manera efectiva.
    """)

    st.audio('./gallery/pensum_guide.mp3',format='audio/mpeg')

    with st.expander('Escribe tu pensum aquí',expanded=st.session_state.expander_pensum):
        write_pensum()

    st.divider()

    st.markdown('### Evaluación del pensum')

    st.write(f"""
    Ahora es el momento de lanzar las preguntas clave para determinar qué tan buena es tu idea y qué necesita para mejorar. Para esto, {st.session_state.user_auth.first_name.capitalize()}, contaremos con la ayuda del último modelo de inteligencia artificial de Anthropic: Claude Sonnet 3.5. Claude evaluará tu propuesta en aspectos críticos como claridad, relevancia, viabilidad, impacto, título, objetivos, idea, actividades y metodología. Después de la evaluación de Claude, revisaremos juntos los resultados y trabajaremos en las sugerencias.
    """)

    with st.expander('Ver evaluación de Claude',expanded=st.session_state.expander_claude):
        claude_layout()
        st.button('Enviar Backup',key='_email_pensum',on_click=send_email_pensum,args=[st.session_state.catche_claude],disabled=st.session_state.send_email_button,type='primary',use_container_width=True)

except:
    st.switch_page("app.py")