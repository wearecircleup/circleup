import streamlit as st
from menu import menu
import pandas as pd
from utils.body import (html_banner, pensum_email_file,verify_pensum_dialog)
from classes.email_class import Email
from classes.pensum_class import PensumLoader
from utils.prompt_templates import pensum_feedback

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'send_email' not in st.session_state:
    st.session_state.send_email = True

if 'verified' not in st.session_state:
    st.session_state.verified = True

st.html(html_banner)

def anthropic_email(pensum,mail_server):
    mail_server.send_pensum_anthropic_prompt(
        user=st.session_state.user_auth.cloud_id,
        user_name=f'{st.session_state.user_auth.first_name.upper()} {st.session_state.user_auth.last_name.upper()}',
        course_name=pensum.course.upper(),
        plain_pensum = pensum_feedback.format(PROPUESTA=pensum.pensum)
    )

def send_file(file,pensum):
    if file is not None:
        mail_server = Email()
        success = mail_server.send_pensum_xlsx(
            recipient=st.session_state.user_auth.email,
            user_name=f'{st.session_state.user_auth.first_name.capitalize()} {st.session_state.user_auth.last_name.capitalize()}',
            file=file,
            course_name= pensum.course
        )
        if success:
            pensum_email_file()
            anthropic_email(pensum,mail_server)
            st.session_state.send_email = True
            st.session_state.verified = False
        else:
            st.error('Error al enviar el email. Por favor, intente de nuevo.')
    else:
        st.warning('Por favor, cargue un archivo antes de intentar enviarlo.')



def verify_pensum():
    st.session_state.send_email = False

menu()

try:
    st.markdown(f"### :blue[**Hola {st.session_state.user_auth.first_name.capitalize()}!**]")
    st.markdown("_Este es tu laboratorio de pruebas del pensum_")

    st.write(f"""
    Es increíble que hayas llegado a este punto de querer escribir algo para tu comunidad. Como ya sabes, el pensum es el lienzo donde se plasman todas las buenas ideas y casos hipotéticos que creemos pueden ser un éxito en Circle Up o en el aprendizaje basado en la comunidad (Community Based Learning). Aquí, podrás estructurar y dar forma a tus propuestas de manera efectiva.
    """)

    st.audio('./gallery/pensum_guide.mp3', format='audio/mpeg')



    @st.cache_data
    def template_file():
        file_path = './gallery/template.xlsx'
        with open(file_path, 'rb') as file:
            return file.read()
    

    st.markdown("#### Pantilla Pensum")
    st.write("Ahora que tienes tu cuenta, puedes compartir ideas para nuevos cursos. He preparado un template para ayudarte. Descárgalo, complétalo y súbelo cuando estés listo.")
    st.info("Te sugiero mantener los nombres de columnas y hojas en el archivo sin cambios. Completa solo los espacios de respuesta siguiendo las instrucciones para evitar problemas.")

    excel_data = template_file()
    st.download_button(
    label="Descargar Platilla",
    data=excel_data,
    file_name="template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True,
    type="primary"
    )

    st.markdown("#### Cargar Propuesta")
    st.write("Cargar archivo aquí para recibir feedback de CircleUp. Luego hacer clic en **Verificar archivo** y **Enviar email**.")

    uploaded_file = st.file_uploader("Cargar archivo Pensum", type="xlsx")

    if uploaded_file is None:
        st.info("Por favor, cargue el archivo usando el botón de arriba.", icon="ℹ️")
    else:
        pensum_loader = PensumLoader(uploaded_file)
        course = pensum_loader.course
        st.session_state.verified = False
        if pensum_loader.missing:
            st.warning(f"**Información incompleta** [_Verificar Pensum File_]\n{pensum_loader.missing}")
            st.session_state.verified = True

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Verificar Archivo', type='secondary', on_click=verify_pensum, use_container_width=True,disabled=st.session_state.verified):
            verify_pensum_dialog()

    with col2:
        if st.button('Enviar Email', type='primary', use_container_width=True, disabled=st.session_state.send_email,):
            st.session_state.verified = True
            st.session_state.send_email = True
            send_file(uploaded_file,pensum_loader)
except AttributeError:
    st.switch_page('app.py')

