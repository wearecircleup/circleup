import json
import streamlit as st
from menu import menu
import pandas as pd
from utils.body import (html_banner, pensum_email_file)
from classes.email_class import Email
from classes.utils_class import CategoryUtils
from google.cloud import firestore

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'send_fb' not in st.session_state:
    st.session_state.send_fb = True

if 'verified_fb' not in st.session_state:
    st.session_state.verified_fb = True

if 'content' not in st.session_state:
    st.session_state.content = ''

if 'show_html' not in st.session_state:
    st.session_state.show_html = False

st.session_state.page_selected = None

st.html(html_banner)
st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

@st.cache_resource
def firestore_client():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    return db

def send_feedback(feedback):
    user_name = st.session_state.user_nickname
    recipient = st.session_state.user_mail
    mail_server = Email()
    success = mail_server.send_claude_feedback(recipient=recipient, user_name=user_name,feedback=feedback)
    if success:
        pensum_email_file()
        st.session_state.send_fb = True
        st.session_state.verified_fb = False
    else:
        st.error('Error al enviar el email. Por favor, intente de nuevo.')

def verify_feedback():
    st.session_state.send_fb = False
    st.session_state.show_html = True

menu()

try:
    st.markdown(f"### :blue[**Hola {st.session_state.user_auth.first_name.capitalize()}!**]")

    st.markdown("#### Cargar Feedback")
    st.write("Cargar el archivo .txt con las sugerencias de Anthropic y luego enviar al correo electrónico del voluntario.")

    uploaded_file = st.file_uploader(label="Cargar Feedback", type="txt",label_visibility='hidden')

    if uploaded_file is None:
        st.info("Por favor, cargue el archivo usando el botón de arriba.", icon="ℹ️")
    else:
        try:
            st.session_state.content = uploaded_file.getvalue().decode('utf-8')
        except UnicodeDecodeError:
            st.session_state.content = uploaded_file.getvalue().decode('latin-1')
        st.session_state.verified_fb = False

    in1, in2 = st.columns(2)
    nickname = in1.text_input(label='Nombre Usuario',key='user_nickname',placeholder='Alan Turing')
    email = in2.text_input(label='Email Usuario',key='user_mail',placeholder='turing@mail.com')

    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button('Verificar Feedback', type='secondary', use_container_width=True, disabled=st.session_state.verified_fb) and nickname and email:
            verify_feedback()
        else:
            st.warning('Faltantes: **Nombre Usuario** o **Email Usuario**')
    with btn2:
        if st.button('Enviar Email', type='primary', use_container_width=True, disabled=st.session_state.send_fb):
            st.session_state.verified = True
            st.session_state.send_email = True
            send_feedback(st.session_state.content)

    # html_container = st.empty()

    # if st.session_state.show_html:
    #     html_container.html(st.session_state.content)

except AttributeError:
    st.switch_page('app.py')
