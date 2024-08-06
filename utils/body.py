import streamlit as st
import pandas as pd


psudo_title = "**Lorem ipsum nunc at libero elit curabitur**"
medium_parragraph = """
Lorem ipsum nunc at libero elit curabitur at lacus lectus placerat, condimentum metus nulla nec sollicitudin fusce orci aliquam congue mattis, condimentum pellentesque euismod himenaeos et suspendisse phasellus dictumst velit. Habitant massa sed aliquet aliquam ac vestibulum et curabitur odio sit viverra ante, eleifend auctor etiam risus quam elementum metus posuere ligula tristique neque lacus platea, curae est orci feugiat viverra mi dolor donec inceptos praesent phasellus.
"""




disclaimer_delete = """
Estás a punto de eliminar tu propuesta de curso de forma permanente. Esta acción es irreversible y no podrás recuperar la información eliminada. 
Si estás absolutamente seguro(a) confirma la eliminación.
"""

html_banner = """
<div style="position: relative; width: 100%; padding: 10px;">
    <div style="border-radius: 10px; overflow: hidden;">
        <img src="https://i.ibb.co/q59pdXX/home.png" alt="Imagen de fondo" style="width: 100%; height: auto;">
    </div>
</div>
"""


html_home = """
<div style="position: relative; width: 100%; padding: 10px;">
    <div style="border-radius: 15px; overflow: hidden;">
        <img src="https://i.ibb.co/TcPD5dK/footer.png" alt="Imagen de fondo" style="width: 100%; height: auto;">
    </div>
</div>
"""

#Delete Warning
@st.dialog("Eliminar Curso")
def warning_deletion(course):
    st.subheader(f'@Eliminar **{course}**')
    st.error(disclaimer_delete,icon="🔥")

@st.dialog("Curso Eliminado")
def deletion_confirm():
    st.info("¡Eliminado! Si necesitas ayuda, no dudes en contactar a sporte", icon="ℹ️")
    st.markdown("**¡Sigue adelante con Circle Up ⚫!**")
    st.snow()


@st.dialog("Cancelar Pre-Inscripcion")
def warning_unenroll(course):
    st.subheader(f'@Cancelando Reserva a **{course}**')
    st.error(f'Estas segur@ que ya no quires participar de **{course}**, es posible que al aforo se complete y ya no puedas inscribirte nuevamente ',icon="🔥")


@st.dialog("Pre-Inscripción Cancelada")
def unenrolled_confirm():
    st.info("¡Tu pre-inscripción ha sido cancelada con éxito!", icon="ℹ️")
    st.markdown("**¡Sigue adelante con Circle Up ⚫!**")
    st.snow()


# Warning Dialogs
@st.dialog("¡Ups! Tenemos una advertencia")
def enrollment_warning(auth_warning):
    if auth_warning == 'one':
        st.info("No te preocupes, parece que ya recibimos tu registro. Te avisaremos para confirmar el inicio de las clases.", icon="ℹ️")
        st.markdown("**¡Sigue adelante con Circle Up ⚫!**")
    elif auth_warning == 'two':
        st.info("Cuando conceptualizamos el curso, nunca pensamos en excluir a nadie. Sin embargo, esta vez el contenido no aplica para tu grupo etario.", icon="ℹ️")
        st.markdown("**¡Sigue adelante con Circle Up ⚫!**")
    elif auth_warning == 'three':
        st.info("Los cupos son limitados y esta vez hemos alcanzado el aforo permitido. No te desanimes, te informaremos tan pronto como encontremos algo que se ajuste a tus temas de interes!.", icon="ℹ️")
        st.markdown("**¡Sigue adelante con Circle Up ⚫!**")



@st.dialog("¡Vamos! ¡Actualicemos!",width="small")
def warning_course_changes(changes):
    attributes = {
        'course_name':'Nombre del Curso', 
        'course_description':'Descripción del Curso',
        'min_audience':'Aforo Mínimo',
        'max_audience':'Aforo Máximo',
        'press_title':'Título para Redes Sociales',
        'press_slogan':'Slogan para Invitar al Público',
        'course_categories':'Categorías del Curso',
        'target_population':'Perfil Demográfico'
    }

    st.markdown("Actualizar tu curso nos ayuda a mantener datos precisos y actualizados.")
    with st.container(height=300):
        st.subheader('**Actualizaciones Identificadas**')
        if len(changes) > 0:
            for key, update in changes.items():
                st.markdown(f'- Nuev@ [**{attributes[key]}**]: :blue[**{update[0]}**] | [**{attributes[key]}**] Anterior: :blue[**{update[1]}**]')

            st.info("Confirma antes de actualizar!", icon="ℹ️")
        else:
            st.info("No se identifican cambios", icon="ℹ️")


@st.dialog("¡Vamos! ¡Actualicemos!",width="small")
def warning_profile_changes(changes):
    attributes = {
        'first_name':'Nombre', 
        'last_name':'Apellido',
        'email':'Correo Electronico',
        'password':'Contraseña',
        'address':'Direccion',
        'phone_number':'Telefono Celular',
        'id_user':'Número Documento Identidad',
        'id_user_type':'Tipo D.I.',
        'city_residence':'Cuidad Residencia', 
        'guardian_fullname':'Nombre Tutor legal/Emergencia',
        'guardian_relationship':'Parentesco',
        'emergency_phone':'Telefono Tutor/Emergencia',
        'how_to_learn':'¿Cómo aprendes mejor?',
        'skills':'¿Cuáles son tus habilidades?',
        'strengths':'¿Cuáles son tus fortalezas?',
        'weaknesses':'¿Cuáles son tus debilidades?'
    }

    st.markdown("Actualizar tu perfil, especialmente tu correo electrónico, números de contacto y número de emergencia, nos ayuda a mantener nuestra base de datos precisa y actualizada.")
    with st.container(height=300):
        st.subheader('**Actualizaciones Identificadas**')
        if any([value[-1] for value in changes.values()]):
            for key, update in changes.items():
                if update[-1]: 
                    if key != 'password':
                        st.markdown(f'- Has actualizado [**{attributes[key]}**] :green[**Antes:**] :blue[**{update[1]}**] | :green[**Ahora:**] :blue[**{update[0]}**]')
                    else: 
                        st.markdown(f'Has actualizado :blue[**Contraseña **********]')
            st.info("Confirma antes de actualizar!", icon="ℹ️")
        else:
            st.info('¡Por ahora no has realizado ninguna actualización! Por favor, verifica si hay cambios.', icon="ℹ️")

@st.dialog("¡Atención! Acceso Denegado")
def unauthenticate_login(session_role):
    roles = {'Admin':'Sentinel','Volunteer':'Nomads','Learner':'Crew'}
    st.subheader(f'Sin acceso @{session_role}')
    st.markdown(f"Lo siento, pero actualmente no tienes autorización para acceder a las herramientas de **{session_role}**.")
    st.image(image='./gallery/nomad.png', use_column_width=True)


@st.dialog("¡Ups! Parece que hubo un problema.")
def warning_login_failed(email:str = None,password:str = None):
    if email and password :
        st.markdown('Hemos tenido dificultades para encontrar tu cuenta.')
        st.markdown('- Revisa que tu **correo electrónico y contraseña** estén  correctos. Es posible que haya errores de mayúsculas, minúsculas o de escritura.')
    else: 
        st.markdown('Hemos tenido dificultades para encontrar tu cuenta.')
        st.markdown('- Revisa que tu **correo electrónico y contraseña** estén  correctos. Es posible que haya errores de mayúsculas, minúsculas o de escritura.')
        st.warning("Por favor, asegúrate de revisar tu **correo electrónico y contraseña**!", icon="⚠️")

disclaimer_data_agreemet = """Al proporcionar mis datos, :blue-background[acepto] que sean utilizados y gestionados internamente, en conformidad con las leyes de protección de datos de Colombia. Esto incluye la Ley de :blue-background[Protección de Datos Personales (Ley 1581 de 2012)] y sus decretos reglamentarios. Entiendo que mis datos serán tratados con el debido respeto y protección, y que no serán compartidos con terceros sin consentimiento explícito"""

@st.dialog("Tratamiento de Datos")
def warning_data_sharing():
    st.markdown(disclaimer_data_agreemet)
    st.divider()
    st.warning("Por favor, asegúrate de aceptar el tratamiento de datos para completar tu registro.",icon="⚠️")

@st.dialog("¡Ups! Datos Faltantes")
def warning_empty_data(fields:str=''):
    st.markdown('Hemos notado que algunos campos están sin llenar. Te invitamos a revisar nuevamente el formulario, puede que falte completar algún campo!')
    st.warning(f"Por favor, verifica que todos los campos estén diligenciados correctamente.")
    st.info(f"{fields}",icon='ℹ️')

@st.dialog("¡Ups! Algo salió mal")
def warning_reupload():
    st.markdown('Hemos notado que el nombre del curso que intentas subir ya está en el sistema.')
    st.divider()
    st.warning("Por favor, verifica que no estás sobrescribiendo un curso. Recuerda que tienes la opción de eliminar o actualizar en caso de que desees renombrar cursos.", icon="⚠️")

# Info Dialogs

@st.dialog("Verificación Pensum")
def verify_pensum_dialog():
    st.subheader(f'Hola, {st.session_state.user_auth.first_name}!')

    st.markdown(f"""
    Vemos que todos los campos están diligenciados. Ten presente que todos los temas son bienvenidos 
    siempre que se alineen con liderazgo, pensamiento crítico y solución de problemas.
    
    Si crees que debes hacer ajustes antes de enviarlo, es el momento. 
    Si no, puedes cerrar este diálogo y hacer clic en **Enviar Email**.
    """)
    if st.button("Entendido",use_container_width=True,type='primary'):
        st.session_state.send_email = False
        st.session_state.verified = True
        st.rerun()


@st.dialog("¡Aprende Sobre Tribus",width="large")
def tribu_definition():
    st.subheader('¡Descubre su Esencia!')
    
    tribus_mean = """
    :blue[**Tribu Crew**]: Son el corazón de nuestra comunidad, los estudiantes entusiastas que se inscriben y participan activamente en los cursos. 
    Su pasión por el aprendizaje y su compromiso con la mejora continua son la fuerza motriz que impulsa nuestra misión social academica.

    
    :blue[**Tribu Nomads**]: Estos son los creativos visionarios, los voluntarios dedicados que diseñan y planifican los cursos. 
    Su innovación y esfuerzo garantizan que cada curso no solo sea educativo, sino también inspirador y enriquecedor.

    
    :blue[**Tribu Sentinel**]: Ellos son los guardianes de la calidad, los administradores que supervisan y aseguran que los cursos cumplan 
    con los estándares establecidos. Su vigilancia y atención al detalle mantienen la integridad y la calidad de los cursos.
    """
    st.markdown(tribus_mean)

@st.dialog("¿Está listo para revisión?", width="large")
def pensum_confirmation(inputs):
    def clean_text(text):
        return " ".join(text.replace("\n", " ").replace("-", "").split()) if isinstance(text, str) else text
    
    inputs = {key: clean_text(value) for key, value in inputs.items()}

    st.markdown(f"## {inputs['pensum_name']}")

    st.markdown("### Información General")
    st.info(f"""
    **Área de Conocimiento:** {inputs['knowledgebase_area']}
    **Modalidad:** {inputs['modality']}
    **Duración:** {inputs['num_sessions']} sesión{'es' if int(inputs['num_sessions']) > 1 else ''} de {inputs['hours_per_session']} hora{'s' if float(inputs['hours_per_session']) > 1 else ''} cada una
    **Duración Total:** {int(inputs['num_sessions']) * float(inputs['hours_per_session'])} horas
    **Público Objetivo:** Individuos en los siguientes rangos de edad:
    {', '.join(inputs['target_pop'])}

    Este curso ha sido diseñado para proporcionar una formación {inputs['modality'].lower()} en {inputs['knowledgebase_area']}, 
    adaptada a las necesidades específicas de los participantes en los rangos de edad mencionados.
    """)

    with st.expander("Objetivos de Aprendizaje", expanded=True):
        st.write(f"""
        1. **Objetivo general:** {inputs['key_objective']}
        2. **Objetivos específicos:** {inputs['key_results']}
        """)

    with st.expander("Estructura del Curso", expanded=True):
        sesiones = [
            (i+1, inputs.get(f'topic{i+1}', ''), inputs.get(f'content{i+1}', ''), 
            inputs.get(f'activities{i+1}', ''), inputs.get(f'materials{i+1}', ''))
            for i in range(4)
        ]
        df_estructura = pd.DataFrame(sesiones, columns=["Sesión", "Tema", "Contenido", "Actividades", "Materiales"])
        st.dataframe(df_estructura, hide_index=True,use_container_width=True)

    with st.expander("Metodología", expanded=True):
        st.write(f"""
        - **Enfoque pedagógico:** {inputs['learning_approach']}
        - **Estrategias de enseñanza:** {inputs['learning_strategy']}
        - **Recursos didácticos:** {inputs['learning_resources']}
        """)

    with st.expander("Evaluación", expanded=True):
        st.write(f"""
        - **Criterios de evaluación:** {inputs['learning_assessment']}
        """)

    st.warning("""
    ⚠️ **ADVERTENCIA**
    La validación de este pensum tendrá un costo al ser evaluada por Claude de Anthropic.

    - La evaluación otorgará un máximo de 45 puntos.
    - Claude es una IA generativa capaz de evaluar la información según criterios predefinidos.
    - El costo se debe al uso de recursos computacionales avanzados.

    Por favor, envía solo si estás seguro de que todo está listo para ser evaluado.
    """)

# Kudos Dialogs
@st.dialog("¡Curso Actualizado!")
def succeed_update_course(name):
    st.subheader(f'¡Hola, @{name}! ¡Tu Curso ha sido actualizado!')
    st.markdown("¡La información ya está en nuestro sistema! Ahora, ¡puedes seguir adelante y realizar más propuestas!")
    st.divider()
    st.success("¡Listo! Si necesitas ayuda, no dudes en contactar a sporte", icon="✅")
    st.markdown("**¡Sigue adelante con Circle Up ⚫!**")
    st.balloons()


@st.dialog("¡Registro Exitoso!")
def succeed_signup(tribe):
    st.subheader(f'Bienvenido a la tribu @**{tribe}** 🎉')
    st.markdown("¡Tu registro ha sido exitoso! Ahora puedes continuar al inicio de sesión para comenzar a disfrutar de nuestra comunidad.")
    st.divider()
    st.success("¡Registro exitoso! Bienvenido a nuestra comunidad. ¡Gracias por unirte!", icon="✅")
    st.markdown(":blue[**¡Comencemos la Aventura!**]")
    st.balloons()

@st.dialog("¡Perfil actualizado!")
def succeed_update_profiles(name):
    st.subheader(f'@{name}, ¡has actualizado tu perfil con éxito!')
    st.markdown("¡Tus datos ya están en nuestro sistema! Ahora puedes continuar con confianza, sabiendo que no te perderás ninguna invitación.")
    st.divider()
    st.success("¡Actualización del estado completada con éxito! ¡Gracias!", icon="✅")
    cols = st.columns([1,4,1])
    cols[1].markdown("**¡Continúa con tu viaje!**")
    st.balloons()


@st.dialog("¡Propuesta Enviada!")
def succeed_proposal(course):
    st.subheader('¡Tu idea está en camino!')
    st.markdown(f"¡Tu curso :blue[@{course}], ha sido registrado en nuestro sistema y lo veras en :blue[2 minutos]! Ahora, vamos a trabajar juntos para hacerlo realidad.")
    st.divider()
    st.success("¡Gracias por compartir tu idea! Este es solo el comienzo de algo asombroso. ", icon="✅")
    st.markdown("**¡Sigue con Circle Up ⚫!**")
    st.balloons()

@st.dialog("Pre-Incripcion Enviada!")
def succefull_enrollment(course):
    st.subheader('¡Tu solicitud está en camino!')
    st.markdown(f"¡Acabas de resevar un lugar para :blue[@{course}]!")
    st.success("¡Todos los cursos estan sujetos a cambios en el ultimo segundo, asi que siempre te estaresmos avisando por correo electronico el estado del curso", icon="✅")
    st.markdown("**¡Sigue con Circle Up ⚫!**")
    st.balloons()



@st.dialog("¡Email Enviado!")
def pensum_email_sent():
    st.subheader('🎉 ¡Excelente! Tu email está en camino')
    
    st.markdown("""
    Hemos enviado un email con el análisis detallado de Anthropic sobre tu curso. 
    Este email contiene:

    - Feedback valioso sobre tu propuesta
    - Preguntas para reflexionar
    - Ideas para inspirar tu creatividad
    
    💡 Recuerda: las grandes ideas necesitan tiempo. Tómate el tuyo para revisarlo con calma.
    """)
    
    st.success("Tu creatividad es el motor del cambio. ¡Sigue adelante!", icon="🚀")
    
    st.balloons()

import streamlit as st

@st.dialog("¡Email Enviado!")
def pensum_email_file():
    st.subheader('🎉 ¡Tu pensum ha sido recibido!')
    
    st.markdown("""
    • Revisaremos tu propuesta en las próximas 24 horas.  
    • Recibirás un email con preguntas clave y sugerencias.   
    • Nos enfocaremos en potenciar liderazgo, resolución de problemas y pensamiento crítico.   
    """)
    
    st.success("💡 Tu creatividad impulsa el cambio. ¡Gracias por contribuir a nuestra comunidad de aprendizaje!", icon="🚀")
    st.balloons()
    st.info("¿Preguntas? Contáctanos en cualquier momento.", icon="ℹ️")

