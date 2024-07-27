import json
import streamlit as st
from menu import menu
from utils.body import html_banner
from google.cloud import firestore
from classes.firestore_class import Firestore
from classes.email_class import Email
from classes.spread_class import Sheets
from classes.utils_class import CategoryUtils
from classes.blobs_class import GoogleBlobs
from google.cloud.firestore_v1.base_query import FieldFilter

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'sign_document' not in st.session_state:
    st.session_state.sign_document = ''

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)

st.html(html_banner)

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["textkey"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn


@st.cache_data(ttl=3600)
def cached_upload_file(google_blobs, file):
    try:
        file_link = google_blobs.upload_file(file)
        return str(file_link) if file_link is not None else ""
    except Exception as e:
        st.error(f"Error al subir el archivo: {str(e)}")
        return ""

menu()

def manage_volunteer_requests(connector: Firestore):
    st.title("Gestión de Propuestas de Voluntarios")
    st.info("Gestione las propuestas de cursos pendientes, aprobadas y denegadas.", icon=":material/table_chart:")

    if st.button("Actualizar datos", use_container_width=True, type='secondary'):
        st.cache_data.clear()
        st.success("Datos actualizados correctamente.", icon=":material/refresh:")
        st.rerun()

    status_options = ["Pending", "Approved", "Denied"]
    selected_status = st.selectbox("Seleccione el estado de las solicitudes:", status_options)

    volunteer_requests = connector.query_collection('course_proposal', [('status', '==', selected_status)])
    
    volunteer_list = [f"{req.data.get('first_name')} {req.data.get('last_name')} - {req.data.get('email')}" for req in volunteer_requests]
    
    if not volunteer_requests:
        st.warning(f"No hay propuestas con estado {selected_status}.", icon=":material/notifications:")

    selected_volunteer = st.selectbox("Seleccione una solicitud para revisar:", volunteer_list)

    if selected_volunteer:
        selected_email = selected_volunteer.split(' - ')[1]
        selected_request = next((req for req in volunteer_requests if req.data.get('email') == selected_email), None)

        if selected_request:

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Nombre:** {selected_request.data.get('first_name')} {selected_request.data.get('last_name')}")
                st.write(f"**Email:** {selected_request.data.get('email')}")
                st.write(f"**Categorías:** {selected_request.data.get('course_categories')}")
            with col2:
                st.write(f"**Id:** {selected_request.data.get('cloud_id_volunteer')}")
                st.write(f"**Id Prop:** {selected_request.data.get('cloud_id')}")
                st.write(f"**Modalidad:** {selected_request.data.get('modality_proposal')}")
                st.write(f"**Inicio Prop**: {selected_request.data.get('start_date')}")

            st.title("Perfil Profesional")
            st.info(f"{selected_request.data.get('volunteer_profile')}", icon=":material/account_circle:")

            col3, col4 = st.columns(2)
            with col3:
                st.success(f"**Audiencia**: {selected_request.data.get('min_audience')} a {selected_request.data.get('max_audience')} personas")
                st.success(f"Edad: **{selected_request.data.get('allowed_age')}** años")
                st.success(f"**Dispositivos** {selected_request.data.get('devices_proposal')}")
            with col4:
                st.success(f"**Ciudad:** {selected_request.data.get('city_proposal')}")
                st.success(f"**Lugar:** {selected_request.data.get('place_proposal')}")
                st.success(f"**Recursos** {selected_request.data.get('tech_resources')}")

            st.info(f"**Conocimientos Básicos** {selected_request.data.get('prior_knowledge')}", icon=":material/school:")
            
            google_blobs = GoogleBlobs('1b62BYUeYAqh6u7UNDboCDlhswcdWgteR')
            uploaded_file = st.file_uploader("Documento Firmado Drive", type=['docx', 'pdf'])

            if uploaded_file is not None:
                if st.button("Subir a Google Drive"):
                    with st.spinner("Subiendo archivo..."):
                        st.session_state.sign_document = cached_upload_file(google_blobs, uploaded_file)
                        if st.session_state.sign_document:
                            st.success(f"Archivo cargado exitosamente.", icon=":material/check_circle:")
                        else:
                            st.warning("No se pudo obtener el enlace del archivo subido.", icon=":material/link_off:")
            else:
                st.info("Por favor, sube un archivo primero.", icon=":material/upload_file:")

            col5, col6 = st.columns(2)
            with col5:
                if st.button("Aprobar solicitud", use_container_width=True, disabled=selected_status == 'Approved'):
                    approve_request(connector, selected_request.data.get('cloud_id'))
                    
            with col6:
                if st.button("Denegar solicitud", use_container_width=True, disabled=selected_status == 'Denied'):
                    deny_request(connector, selected_request.data.get('cloud_id'))

            email_button_disabled = selected_status == 'Pending' or selected_request.data.get('notification') == 'Send'
            if st.button("Enviar Email de Notificación", disabled=email_button_disabled, use_container_width=True):
                send_notification_email(connector, selected_request.data)

def approve_request(connector: Firestore, cloud_id: str):

    signature = st.session_state.sign_document
    
    last_update = CategoryUtils().get_current_date()
    connector.update_document('course_proposal', cloud_id, {'status': 'Approved', 'signed_concent': signature,'updated_at': last_update})

    sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
    sheet.replace_values(cloud_id,{'status': 'Approved', 'signed_concent': signature,'updated_at': last_update})
    st.success(f"Propuesta aprobada con éxito.", icon=":material/thumb_up:")
    st.rerun()

def deny_request(connector: Firestore, cloud_id: str):
    
    last_update = CategoryUtils().get_current_date()
    connector.update_document('course_proposal', cloud_id, {'status': 'Denied', 'signed_concent': 'Disapproved','updated_at': last_update})

    sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
    sheet.replace_values(cloud_id,{'status': 'Denied', 'signed_concent': 'Disapproved','updated_at': last_update})
    st.success(f"Propuesta denegada con éxito.", icon=":material/thumb_down:")
    st.rerun()

def send_notification_email(connector: Firestore, volunteer_data: dict):
    
    email_sender = Email()
    full_name = f"{volunteer_data['first_name']} {volunteer_data['last_name']}"
    recipient_email = volunteer_data['email']
    course_categories = volunteer_data['course_categories']
    course_name = volunteer_data['course_name']
    modality_proposal = volunteer_data['modality_proposal']
    min_audience = volunteer_data['min_audience']
    max_audience = volunteer_data['max_audience']
    allowed_age = volunteer_data['allowed_age']
    city_proposal = volunteer_data['city_proposal']
    place_proposal = volunteer_data['place_proposal']
    start_date = volunteer_data['start_date']


    is_approved = volunteer_data['status'] == 'Approved'

    if is_approved:
        subject = f"¡Felicidades! Tu curso ha sido aprobado"
        content = f"""
        <p>Estimado/a <strong>{full_name}</strong>,</p>

        <p>Nos complace enormemente informarte que tu curso <strong>{course_name}</strong> ha sido <strong>aprobado</strong> por el equipo de Circle Up. ¡Felicidades!</p>

        <p>Estamos emocionados de anunciar que tu curso comenzará el <strong>{start_date}</strong>. Tu experiencia será sin duda un valioso aporte para nuestra comunidad.</p>

        <p>Detalles del curso aprobado:</p>
        <ul>
            <li><strong>Nombre del curso:</strong> {course_name}</li>
            <li><strong>Categoria(s) Curso:</strong> {course_categories}</li>
            <li><strong>Modalidad:</strong> {modality_proposal}</li>
            <li><strong>Fecha de inicio:</strong> {start_date}</li>
            <li><strong>Lugar:</strong> {place_proposal}, {city_proposal}</li>
            <li><strong>Capacidad:</strong> {min_audience} - {max_audience} participantes</li>
            <li><strong>Rango de edad:</strong> {allowed_age}</li>
        </ul>

        <p>Próximos pasos:</p>
        <ol>
            <li>Prepara tu material didáctico y plan de lecciones.</li>
            <li>Familiarízate con la plataforma.</li>
            <li>Marca en tu calendario la fecha de inicio: <strong>{start_date}</strong>.</li>
        </ol>

        <p>Si necesitas algún recurso adicional o tienes preguntas, no dudes en contactarnos. Estamos aquí para apoyarte en todo lo que necesites para que tu curso sea un éxito rotundo.</p>

        <p><strong>Una vez más, ¡felicidades por tu curso! Tu dedicación y experiencia son fundamentales.</strong></p>

        <p>Atentamente,<br>
        Circle Up Community ⚫</p>
        """
    else:
        subject = f"Actualización sobre tu propuesta"
        content = f"""
        <p>Estimado/a <strong>{full_name}</strong>,</p>

        <p>Gracias por tu propuesta para el curso <strong>{course_name}</strong> en Circle Up. Apreciamos sinceramente el tiempo y esfuerzo que has invertido en desarrollar esta idea.</p>

        <p>Después de una revisión, lamentamos informarte que en esta ocasión <strong>no podemos aprobar el curso propuesto</strong> en su formato actual.</p>

        <p>Detalles de la propuesta revisada:</p>
        <ul>
            <li><strong>Nombre del curso:</strong> {course_name}</li>
            <li><strong>Modalidad:</strong> {modality_proposal}</li>
            <li><strong>Fecha propuesta:</strong> {start_date}</li>
            <li><strong>Lugar:</strong> {place_proposal}, {city_proposal}</li>
            <li><strong>Capacidad propuesta:</strong> {min_audience} - {max_audience} participantes</li>
            <li><strong>Rango de edad propuesto:</strong> {allowed_age}</li>
        </ul>

        <p>Aunque no podemos proceder con la propuesta en su forma actual, valoramos enormemente tu iniciativa y experiencia. Te animamos a considerar los siguientes pasos:</p>

        <ol>
            <li>Revisa nuestras pautas para propuestas de cursos y considera cómo podrías ajustar tu idea.</li>
            <li>Explora la posibilidad de colaborar con otros voluntarios en un curso similar o complementario.</li>
            <li>Programa una llamada para discutir formas de refinar tu propuesta.</li>
        </ol>

        <p>Estamos aquí para apoyarte en el desarrollo de tu idea. Si deseas discutir tu propuesta o explorar otras oportunidades de contribuir a Circle Up, por favor no dudes en contactarnos.</p>

        <p>Atentamente,<br>
        El equipo de Circle Up Community ⚫</p>
        """

    try:
        st.info("Enviando email de notificación...", icon=":material/send:")
        email_sender.send_custom_email(recipient_email, full_name, subject, content)
        connector.update_document('course_proposal', volunteer_data['cloud_id'], {'notification': 'Send'})
        
        last_update = CategoryUtils().get_current_date()
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
        sheet.replace_values(volunteer_data['cloud_id'],{'notification': 'Send'})
        st.success(f"Email enviado exitosamente a {full_name}", icon=":material/email_check:")
        st.rerun()
    except Exception as e:
        st.error(f"Error al enviar el email: {str(e)}")

connector = connector()
manage_volunteer_requests(connector)



