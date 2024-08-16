import streamlit as st

st.set_page_config(
    page_title="Circle Up",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from datetime import datetime
import time
import json
from google.cloud import firestore
from classes.users_class import Users
from classes.firestore_class import Firestore
from classes.spread_class import Sheets   
from classes.utils_class import CategoryUtils
from classes.email_class import Email
from typing import List, Dict, Optional
from dataclasses import asdict
from utils.form_options import (disabilities, ethnics, skills,
                                how_to_learn, weaknesses, strengths,
                                volunteer_keywords, gender_list, id_user_list,
                                topics_of_interest, education_level)

from utils.form_instructions import form_definitions
import re
import random
import string
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


from menu import menu


def user_to_json(user: Users) -> str:
    return json.dumps(asdict(user))

def json_to_user(json_str: str) -> Users:
    return Users(**json.loads(json_str))

def load_user_from_session() -> Optional[Users]:
    if 'user_data' in st.session_state:
        return json_to_user(st.session_state.user_data)
    return None

def initialize_session_state():
    """Initialize session state variables."""
    variables = [
        ('disabilities', disabilities),
        ('ethnics', ethnics),
        ('skills', skills),
        ('how_to_learn', how_to_learn),
        ('weaknesses', weaknesses),
        ('strengths', strengths),
        ('volunteer_keywords', volunteer_keywords),
        ('gender', gender_list),
        ('form_definitions', form_definitions),
        ('id_user_list', id_user_list),
        ('topics_of_interest', topics_of_interest),
        ('education_level', education_level),
        ('_email_entered', None),
        ('_password_entered', None),
        ('ttl_data', 5),
        ('role_synonym', 'Crew'),
        ('register_button', False),
        ('_is_ethnic', "No"),
        ('_is_ethnic_affiliation', True),
        ('user_auth', load_user_from_session()),
        ('page_selected', None),
        ('page_msm', 'status')
    ]
    
    for key, value in variables:
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)

if 'change_password' not in st.session_state:
    st.session_state.change_password = False

if 'forgot_password' not in st.session_state:
    st.session_state.forgot_password = False

if 'token_password' not in st.session_state:
    st.session_state.token_password = False

if 'right_password' not in st.session_state:
    st.session_state.right_password = False

if 'email_account' not in st.session_state:
    st.session_state.email_account = None

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

def show_navigation():
    pages = {
        "Perfil": "pages/profile.py",
        "Explora Cursos": "pages/enroll.py",
        "Asistencia": "pages/attendance.py"
    }

    if st.session_state.user_auth.user_role == 'Learner':
        pages["Ser Voluntario"] = "pages/volunteering.py"

    if st.session_state.user_auth.user_role in ['Volunteer', 'Admin']:
        pages["Propuestas"] = "pages/dashboard.py"

    if st.session_state.user_auth.user_role == 'Admin':
        pages["Proponer Curso"] = "pages/proposal.py"
        pages["Crear Ideas"] = "pages/make.py"
        pages["Gestión Voluntarios"] = "pages/orchestrate.py"
        pages["Revisar Cursos"] = "pages/rollout.py"

    return pages

def prepare_sheets_data(instance_data: dict) -> List[str]:
    """
    Prepara los datos específicos para enviar a Google Sheets.
    """
    utils = CategoryUtils()
    now = datetime.now()
    return [
        utils.get_current_date(),
        utils.date_to_day_of_week(),
        utils.time_to_category(),
        instance_data.get('first_name', ''),
        instance_data.get('last_name', ''),
        instance_data.get('gender', ''),
        utils.age_to_category(instance_data.get('dob', '')),
        instance_data.get('email', ''),
        instance_data.get('user_role', ''),
        instance_data.get('city_residence', ''),
        'login'
    ]


def get_user_auth(email,token):
    try:
        Conn = connector()
        user_requests = Conn.query_collection('users_collection', [('email', '==', email)])
        time.sleep(1)
        user_secrets = user_requests[0].data
        if user_secrets['cloud_id']:
            connector().update_document('users_collection',user_secrets['cloud_id'],{'password':token})
            time.sleep(1)
            return True
    except Exception as e:
        return False

@st.cache_data(ttl=900, show_spinner=False)
def send_to_sheets(data: List[List[str]]) -> bool:
    try:
        sheet: Sheets = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM', 'Log In')
        sheet.create(data)
        return True
    except Exception as e:
        st.error(f"Lo siento, ha ocurrido un error al enviar los datos: {str(e)}")
        return False

def login_setup(email: str, password: str) -> str:
    if not email or not password:
        return "incomplete_fields"
    try:
        messages = [
            ('Preparando tu :blue[**Sesión...**]', 'auto_awesome_mosaic'),
            ('Explora :blue[**Circle Up Community**]', 'travel_explore'),
            ('Sé :blue[**Embajador**] de tu comunidad profesional', 'military_tech')
        ]

        message_container = st.empty()

        for msg, icon in messages:
            message_container.info(msg, icon=f":material/{icon}:")
            time.sleep(1)

        time.sleep(0.5)
        message_container.empty()

        query_data = connector().auth_firestore(email, password)
        time.sleep(1)
        instance = Users(**query_data)
        instance_data = asdict(instance)
        sheets_data = prepare_sheets_data(instance_data)
        send_to_sheets([sheets_data])
        time.sleep(1)

        st.session_state.user_auth = instance
        st.session_state.user_data = user_to_json(instance)
        st.session_state.login_status = 'logged_in'
        return "success"
    except:
        st.session_state.user_auth = None
        return "wrong_password"

def show_interactive_login_instructions():
    if st.button(':material/stairs_2: Ver pasos para acceder', use_container_width=True, type='secondary'):        
        st.toast('1. Ingresa tu correo electrónico', icon=":material/mail:")
        time.sleep(1.5)
        
        st.toast('2. Escribe tu contraseña', icon=":material/password:")
        time.sleep(1.5)
        
        st.toast('3. Haz clic en el botón **Ingresar**', icon=":material/ads_click:")
        time.sleep(1.5)
        
        st.toast('¿Nuevo en Circle Up? Haz clic en **Únete/Regístrate**', icon=":material/downhill_skiing:")
        time.sleep(1.5)
        
        st.balloons()

@st.cache_data(ttl=900, show_spinner=False)
def tokens_generator(email):
    utils = CategoryUtils()
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(8)).lower()
    token_password = token +  utils.get_current_date().replace('-','') + email
    firebase_token = {'cloud_id': token_password,'token': token, 'email':email}
    return firebase_token

def change_password_button():
    st.session_state.change_password = not st.session_state.change_password

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos :orange[**8 caracteres.**]")
    if not re.search(r"[A-Z]", password):
        errors.append("La contraseña debe contener al menos :orange[**una letra mayúscula.**]")
    if not re.search(r"[a-z]", password):
        errors.append("La contraseña debe contener al menos :orange[**una letra minúscula.**]")
    if not re.search(r"\d", password):
        errors.append("La contraseña debe contener al menos :orange[**un número.**]")
    if not re.search(r"[!\_\-@#$%^&*(),.?\":{}|<>]", password):
        errors.append("La contraseña debe contener al menos :orange[**un carácter especial.**]")
    
    is_valid = len(errors) == 0
    
    if not is_valid:
        funny_example = "N@pol3on!"
        message = "\n".join(f":material/password_2_off: {error}" for error in errors)
        message += f" ¿Qué tal si pruebas con algo como :orange[{funny_example}]? :material/vpn_lock:"
    else:
        message = "La contraseña cumple con todos los requisitos."
    
    return is_valid, message

def forgot_password() -> None:
    """
    Manage the password change process in a Streamlit app with improved user experience.
    """
    st.info("Sigue estos pasos para cambiar tu contraseña. :blue[**Primero**], introduce tu correo electrónico para recibir un token de recuperación. :blue[**Segundo**], ingresa el token recibido y verifica tu cuenta. :blue[**Finalmente**], establece tu nueva contraseña.",icon=":material/self_improvement:")


    handle_password_recovery()
    if st.session_state.forgot_password:
        handle_token_validation()
        if st.session_state.token_password:
            handle_password_update()

def handle_password_recovery() -> bool:
    """
    Handle the password recovery process.
    """
    with st.form('change_pass'):
        recover_email = st.text_input('Correo electrónico')
        submit_recover_password = st.form_submit_button(':material/qr_code_2_add: Recuperar Contraseña', type='primary', use_container_width=True)
    
    if submit_recover_password:
        if recover_email:
            send_recovery_email(recover_email)
            st.session_state.forgot_password = True
            st.session_state.email_account = recover_email
            return True
        else:
            st.warning("Por favor, introduce tu correo electrónico para continuar.",icon=":material/mail:")
    return False

def send_recovery_email(email: str) -> None:
    """
    Send a recovery email with a token.
    """
    st.info(f'Enviando email de recuperación a :blue[**{email}**]...',icon=":material/mail:")
    token = tokens_generator(email.lower().strip())
    
    try:
        connector().add_document('recover_account', token, token['cloud_id'])
        time.sleep(1)
        email_sender = Email()
        subject = "Recuperación de Contraseña"
        content = generate_email_content(token['token'])
    
        with st.spinner("Enviando email..."):
            email_sender.send_custom_email(email, '', subject, content)
        st.success("Email de recuperación enviado exitosamente. Por favor, revisa tu bandeja de entrada.",icon=":material/attach_email:")
        st.info("El siguiente paso es introducir el :blue[**token**] que recibirás en tu correo.",icon=":material/token:")
    except Exception as e:
        st.warning("El correo ya ha sido enviado. Si no lo encuentras en tu bandeja de entrada, :orange[**revisa la carpeta de spam o correos no deseados.**]",icon=':material/markunread_mailbox:')

def handle_token_validation() -> bool:
    """
    Handle the token validation process.
    """
    with st.form('validate_token'):
        user_token = st.text_input('Escribe el Token', type='password')
        submit_recover_account = st.form_submit_button(':material/contextual_token: Verificar Token', type='primary', use_container_width=True)

    if submit_recover_account:
        if user_token:
            if validate_token(st.session_state.email_account, user_token):
                st.success("Verificación exitosa. Se ha confirmado el token enviado a tu correo electrónico. :green[**Por favor, procede a cambiar tu contraseña.**]",icon=":material/self_improvement:")
                st.session_state.token_password = True
                return True
            else:
                st.error("Token inválido. Por favor, verifica e intenta de nuevo.",icon=":material/notifications:")
        else:
            st.warning("Por favor, completa todos los campos para continuar.",icon=":material/other_admission:")
    return False

def validate_token(email: str, token: str) -> bool:
    """
    Validate the recovery token.
    """
    token_auth = token + CategoryUtils().get_current_date().replace('-', '') + email.lower().strip()
    validate_token = connector().get_document('recover_account', token_auth)
    time.sleep(1)
    return all(validate_token.data.values())

def handle_password_update() -> None:
    """
    Handle the password update process with real-time validation.
    """
    new_password = st.text_input('Nueva contraseña', type='password')
    repeat_password = st.text_input('Repite tu nueva contraseña', type='password')
    
    if new_password and repeat_password:
        messages = []
        if new_password == repeat_password:
            st.success("Las contraseñas coinciden",icon=":material/all_match:")
            is_valid, password_message = validate_password(new_password)
            if not is_valid:
                messages.append(f":material/unsubscribe: **Contraseña inválida**\n\n{password_message}")
                for message in messages:
                    st.warning(message,icon=":material/vpn_key:")

            else:
                st.session_state.right_password = True
        else:
            st.warning("Las contraseñas no coinciden.",icon=":material/notifications:")

    if st.button(':material/deployed_code_history: Actualizar Contraseña', type='primary', use_container_width=True) and st.session_state.right_password:
        if new_password == repeat_password:
            if get_user_auth(st.session_state.email_account, new_password):
                st.success("¡Contraseña actualizada con éxito!")
                st.info("Ahora puedes iniciar sesión con tu nueva contraseña.")
                time.sleep(3)
                st.session_state.token_password = False
                st.session_state.forgot_password = False
                st.session_state.change_password = False
                st.session_state.right_password = False
                st.switch_page('app.py')
            else:
                st.error("No se pudo actualizar la contraseña. Por favor, intenta de nuevo más tarde.",icon=":material/password_2_off:")

        else:
            st.error("Las contraseñas no coinciden. Por favor, verifica e intenta de nuevo.",icon=":material/password:")
    else:
        st.error("Asegúrate de que tu contraseña sea fuerte y segura.", icon=":material/password:")

def generate_email_content(token: str) -> str:
    """
    Generate the content for the recovery email.
    """
    return f"""
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 95%; margin: 0 auto;">
            <tr>
                <td style="padding: 20px;">
                    <div style="padding: 20px;">
                        <h3>Recuperación de Contraseña</h3>

                        <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en Circle Up Community. 
                        Utiliza el siguiente token para restablecer tu contraseña. No compartas este token con nadie; ningún miembro del equipo de Circle Up Community te lo solicitará nunca.</p

                        <p style="text-align: center;"><h1><strong>{token}</strong></h1></p>

                        <p>Si no solicitaste este cambio, simplemente ignora este correo.</p>

                        <p>Saludos,<br>
                        Circle Up Community ⚫</p>
                        
                        <p style="font-size: 12px; color: #888;">Este correo electrónico contiene información confidencial. Si no eres el destinatario previsto, por favor, elimina este mensaje. Gracias por tu atención a la privacidad.</p>
                    </div>
                </td>
            </tr>
        </table>
    """
    

def main():
    st.title(":material/ads_click: **Inicio de Sesión | Circle Up Community**")
    
    if st.session_state.user_auth is None:

        st.info("Sigue estos pasos para ingresar. Haz clic en :blue[**Ver pasos para acceder**]")
        show_interactive_login_instructions()

        with st.form(key='login_form', clear_on_submit=False):
            email = st.text_input(label="Correo electrónico", placeholder="mail@mail.com", key="_email_entered")      
            password = st.text_input(label="Contraseña", placeholder="eMp3r@D0r", key="_password_entered", type="password")
            
            submit_button = st.form_submit_button(label=":material/ads_click: Ingresar", type="primary", use_container_width=True)

        if submit_button:
            st.session_state.user_auth = None
            status = login_setup(email, password)
            st.session_state.page_msm = 'success' if status == 'success' else 'fail'
            st.rerun()

        col1, col2, col3  = st.columns(3)
        with col1:
            if st.button(':material/touch_app: Crear Cuenta', type="primary", help='Registro', use_container_width=True):
                st.switch_page('pages/signup.py')
        with col2:
            if st.button(':material/arrow_drop_down_circle: ¿Qué es Community?', type="secondary", use_container_width=True):
                st.switch_page('pages/home.py')
        with col3:
            if st.button(':material/password_2_off: ¿Olvidaste tu contraseña?', type="secondary", use_container_width=True):
                change_password_button()
    
    else:
        st.success(f"Bienvenid@, {st.session_state.user_auth.first_name}! Tu cuenta ha sido autenticada. "
                    "Utiliza este :green[**Menú Rápido**] para acceder a las diferentes secciones de Circle Up Community", icon=":material/passkey:")
        
        pages = show_navigation()
        selected_page = st.selectbox("Menú Rápido", options=list(pages.keys()), key='page_selected',index=None)

        if selected_page:
            if st.button(f":material/scuba_diving: Ir a {selected_page}", type="primary",use_container_width=True):
                st.switch_page(pages[selected_page])
        else:        
            st.info(f"Tienes acceso a :blue[**{', '.join(list(pages.keys()))}**], selecciona una opción del menú para navegar a esa sección.")

    if st.session_state.user_auth is None and st.session_state.change_password:
        forgot_password()

    if st.session_state.page_msm == 'fail':
        st.error("No pudimos iniciar sesión. Por favor, revisa tu correo electrónico y contraseña.", icon=":material/notifications:")
    
    st.info(":blue[**¿Necesitas ayuda?**] Escribe a :blue[**wearecircleup@gmail.com**]", icon=":material/sos:")

    menu()
    st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
if __name__ == "__main__":
    main()





