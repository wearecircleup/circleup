import json
import streamlit as st
from menu import menu
from utils.body import html_banner
from google.cloud import firestore
from classes.firestore_class import Firestore
from classes.email_class import Email
from google.cloud.firestore_v1.base_query import FieldFilter

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .stTextInput, .stSelectbox {
        max-width: 100%;
    }
    p, .stMarkdown {
        font-size: 14px;
    }
    h1 {
        font-size: 24px;
    }
            
    h2 {
        font-size: 22px;
    }
            
    h3 {
        font-size: 22px;
    }
</style>
""", unsafe_allow_html=True)

st.html(html_banner)

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn

menu()

def manage_volunteer_requests(connector: Firestore):
    st.title("Gestión de Solicitudes de Voluntarios")

    if st.button("Actualizar datos", use_container_width=True, type='secondary'):
        st.cache_data.clear()
        st.rerun()

    # Lista de estados
    status_options = ["Pending", "Approved", "Denied"]
    selected_status = st.selectbox("Seleccione el estado de las solicitudes:", status_options)

    # Cargar solicitudes de voluntarios según el estado seleccionado
    volunteer_requests = connector.query_collection('volunteer_request', [FieldFilter('status', '==', selected_status)])
    
    # Crear lista de voluntarios para selección
    volunteer_list = [f"{req.data.get('first_name')} {req.data.get('last_name')} - {req.data.get('email')}" for req in volunteer_requests]
    
    selected_volunteer = st.selectbox("Seleccione una solicitud para revisar:", volunteer_list)

    if selected_volunteer:
        selected_email = selected_volunteer.split(' - ')[1]
        selected_request = next((req for req in volunteer_requests if req.data.get('email') == selected_email), None)

        if selected_request:
            st.subheader(f"Perfil :blue[**{selected_status}**] | :green[**{selected_request.data.get('user_role')}**]")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nombre:** {selected_request.data.get('first_name')} {selected_request.data.get('last_name')}")
                st.write(f"**Email:** {selected_request.data.get('email')}")
                st.write(f"**Edad:** {selected_request.data.get('age')}")
                st.write(f"**Educación:** {selected_request.data.get('education')}")
                st.write(f"**Profesión:** {selected_request.data.get('profession_category')}")
            with col2:
                st.write(f"**Id:** {selected_request.data.get('cloud_id')}")
                st.write(f"**Experiencia:** {selected_request.data.get('experience')} año(s)")
                st.write(f"**Disponibilidad:** {selected_request.data.get('availability')}")
                st.write(f"**Tiempo disponible:** {selected_request.data.get('time_availability')}")
                st.write(f"**Compromiso:** {selected_request.data.get('commitment')} Hr./Mes")
            
            st.write(f"**Motivación:** {selected_request.data.get('motivation')}")
            st.write(f"**Notificación:** :blue[**{selected_request.data.get('notification')}**]")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Aprobar solicitud", use_container_width=True, disabled=selected_status == 'Approved'):
                    approve_request(connector, selected_request.data.get('cloud_id'))
            with col2:
                if st.button("Denegar solicitud", use_container_width=True, disabled=selected_status == 'Denied'):
                    deny_request(connector, selected_request.data.get('cloud_id'))

            # Botón para enviar email
            email_button_disabled = selected_status == 'Pending' or selected_request.data.get('notification') == 'Send'
            if st.button("Enviar Email de Notificación", disabled=email_button_disabled, use_container_width=True):
                send_notification_email(connector, selected_request.data)

def approve_request(connector: Firestore, cloud_id: str):
    # Actualizar el rol de usuario a 'Volunteer' en users_collection
    connector.update_document('users_collection', cloud_id, {'user_role': 'Volunteer'})
    
    # Actualizar el estado a 'Approved' y la notificación a 'Pending' en volunteer_request
    connector.update_document('volunteer_request', cloud_id, {'status': 'Approved', 'notification': 'Pending','user_role': 'Volunteer'})
    st.rerun()

def deny_request(connector: Firestore, cloud_id: str):
    connector.update_document('users_collection', cloud_id, {'user_role': 'Learner'})
    # Actualizar el estado a 'Denied' y la notificación a 'Pending' en volunteer_request
    connector.update_document('volunteer_request', cloud_id, {'status': 'Denied', 'notification': 'Pending','user_role': 'Learner'})
    st.rerun()

def send_notification_email(connector: Firestore, volunteer_data: dict):
    email_sender = Email()
    full_name = f"{volunteer_data['first_name']} {volunteer_data['last_name']}"
    recipient_email = volunteer_data['email']
    is_approved = volunteer_data['status'] == 'Approved'

    if is_approved:
        subject = "¡Felicidades! Tu solicitud de voluntariado ha sido aprobada"
        content = f"""
        <p>Estimado/a <strong>{full_name}</sstrong>,</p>

        <p>Nos complace informarte que tu solicitud para ser voluntario/a en <strong>Circle Up</strong> ha sido <strong>aprobada</strong>.</p>
        <p>Queremos felicitarte por dar este importante paso para ayudar a nuestra comunidad.</p>
        <p>Para continuar con el proceso, necesitamos que completes los siguientes pasos:</p>

        <ol>
            <li>Responde a este <a href="https://forms.gle/USqzB8a53rPVXLHVA">breve formulario</a></li>
            <li>Agenda una <a href="https://calendly.com/wearecircleup/15min">reunión con nosotros</a> para la conceptualización de la idea y acompañamiento en el proceso</li>
        </ol>

        <p><strong>Estamos emocionados de tenerte en nuestro equipo y ansiosos por comenzar a trabajar juntos.</strong></p>
        <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
        <p><strong>¡Bienvenido/a a Circle Up!</strong></p>

        <p>Atentamente,<br>
        Circle Up Community ⚫ Team</p>
        """
    else:
        subject = "Actualización sobre tu solicitud de voluntariado"
        content = f"""
        <p>Estimado/a <strong>{full_name}</strong>,</p>

        <p>Gracias por tu interés en ser voluntario/a en <strong>Circle Up</strong>.</p>
        <p>Lamentamos informarte que en esta ocasión <strong>no podemos aprobar tu solicitud de voluntariado</strong>.</p>
        <p>Apreciamos sinceramente tu deseo de contribuir y te animamos a seguir buscando oportunidades para marcar la diferencia en tu comunidad.</p>
        <p>Si tienes alguna pregunta o te gustaría obtener más información sobre nuestra decisión, no dudes en contactarnos.</p>
        
        <p><strong>Te deseamos lo mejor en tus futuros esfuerzos de voluntariado.</strong></p>

        <p>Atentamente,<br>
        Circle Up Community ⚫ Team</p>
        """

    try:
        email_sender.send_custom_email(recipient_email, full_name, subject, content)
        connector.update_document('volunteer_request', volunteer_data['cloud_id'], {'notification': 'Send'})
        st.success(f"Email enviado exitosamente a {full_name}")
        st.rerun()
    except Exception as e:
        st.error(f"Error al enviar el email: {str(e)}")

connector = connector()
manage_volunteer_requests(connector)