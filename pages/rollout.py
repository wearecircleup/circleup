import streamlit as st

st.set_page_config(
    page_title="Circle Up Community",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import json
from menu import menu
from utils.body import html_banner
from google.cloud import firestore
from classes.firestore_class import Firestore
from classes.email_class import Email
from classes.spread_class import Sheets
from classes.utils_class import CategoryUtils
from classes.blobs_class import GoogleBlobs
import time
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


if 'sign_document' not in st.session_state:
    st.session_state.sign_document = ''

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.session_state.page_selected = None

st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)

@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
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
    
    volunteer_list = [f"{req.data.get('cloud_id')} - {req.data.get('email')}" for req in volunteer_requests]
    
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

            st.info(f":blue[**Perfil Profesional**] {selected_request.data.get('volunteer_profile')}", icon=":material/account_circle:")
            st.info(f":blue[**Curso Propuesta**] {selected_request.data.get('course_name')}", icon=":material/web_traffic:")

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
            
            if selected_status in ['Pending','Denied']:

                google_blobs = GoogleBlobs('1xRglgLMUhscS_hh90_kJ00lwRIv_a5pk')
                uploaded_file = st.file_uploader("Documento Firmado Drive", type=['pdf'])

                if uploaded_file is not None:
                    
                    new_filename = f"{selected_request.data.get('email')}-{selected_request.data.get('cloud_id_volunteer')}-{selected_request.data.get('cloud_id')}.pdf"
                    uploaded_file.name = new_filename

                    if st.button(":material/upload_file: Subir a Google Drive",use_container_width=True):
                        with st.spinner("Subiendo archivo..."):
                            st.session_state.sign_document = cached_upload_file(google_blobs, uploaded_file)
                            time.sleep(3)
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

            email_button_disabled = selected_request.data.get('notification') == 'Send'
            if st.button(":material/mail: Enviar Email de Notificación", disabled=email_button_disabled, use_container_width=True):
                send_notification_email(connector, selected_request.data)

def approve_request(connector: Firestore, cloud_id: str):

    signature = st.session_state.sign_document
    
    last_update = CategoryUtils().get_current_date()
    with st.spinner("Aprobando Propuesta..."):
        connector.update_document('course_proposal', cloud_id, {'status': 'Approved','notification':'Pending','signed_concent': signature,'updated_at': last_update})
        time.sleep(3)
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
        sheet.replace_values(cloud_id,{'status': 'Approved','notification':'Pending', 'signed_concent': signature,'updated_at': last_update})
        time.sleep(2)
        st.success(f"Propuesta aprobada con éxito.", icon=":material/thumb_up:")
        st.rerun()

def deny_request(connector: Firestore, cloud_id: str):
    with st.spinner("Denegando Propuesta..."):
        last_update = CategoryUtils().get_current_date()
        connector.update_document('course_proposal', cloud_id, {'status': 'Denied','notification':'Pending','updated_at': last_update})
        time.sleep(3)
        sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
        sheet.replace_values(cloud_id,{'status': 'Denied','notification':'Pending','updated_at': last_update})
        time.sleep(2)
        st.success(f"Propuesta denegada con éxito.", icon=":material/thumb_down:")
        st.rerun()

def send_notification_email(connector: Firestore, volunteer_data: dict):
    utils = CategoryUtils()
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
    start_date = utils.format_date(volunteer_data['start_date'],volunteer_data['city_proposal'])

    is_approved = volunteer_data['status'] == 'Approved'

    if is_approved:
        subject = f"¡Felicidades! Tu curso Aprobado"
        content = f"""
            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 95%; margin: 0 auto;">
                <tr>
                    <td style="padding: 20px;">
                        <div style="padding: 20px;">
                            <h3>Hola {full_name},</h3>

                            <p>Tu curso <strong>{course_name}</strong> ha sido aprobado por el equipo de Circle Up Community. Felicitaciones y gracias por tu compromiso.</p>

                            <p><strong>Fecha de inicio: {start_date}</strong></p>

                            <p>Detalles del curso:</p>
                            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Nombre Propuesta</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{course_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Categoría(s)</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{course_categories}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Modalidad</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{modality_proposal}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Lugar</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{place_proposal}, {city_proposal}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Capacidad</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{min_audience} - {max_audience} participantes</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Rango de edad</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{allowed_age}</td>
                                </tr>
                            </table>

                            <p><strong>Tus responsabilidades:</strong></p>
                            <ol>
                                <li>Preparar el material didáctico y plan de lecciones.</li>
                                <li>Familiarizarte con la plataforma.</li>
                                <li>Cumplir con la fecha de inicio: <strong>{start_date}</strong>.</li>
                            </ol>

                            <p><strong>Importante:</strong> Es tu responsabilidad contactarnos ante cualquier duda o imprevisto. Estamos aquí para apoyarte, pero dependemos de tu comunicación oportuna.</p>

                            <p>Valoramos tu experiencia y compromiso. Juntos haremos de este curso un éxito.</p>

                            <p>Saludos,<br>
                            Circle Up Community ⚫</p>
                        </div>
                    </td>
                </tr>
            </table>
        """
    else:
        subject = f"Actualización Propuesta"
        content = f"""
            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 100%; margin: 0 auto;">
                <tr>
                    <td style="padding: 20px;">
                        <div style="padding: 20px;">
                            <p>Hola {full_name},</p>

                            <p>Gracias por tu propuesta del curso <strong>{course_name}</strong>. Hemos revisado cuidadosamente tu propuesta y apreciamos el tiempo y esfuerzo que has invertido en desarrollarla.</p>

                            <p>Lamentamos informarte que en este momento <strong>no podemos aprobar el curso en su formato actual</strong>. Sin embargo, creemos que tu propuesta tiene potencial y varias oportunidades de mejora.</p>

                            <p>Detalles básicos de la propuesta:</p>
                                            
                            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Nombre Propuesta</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{course_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f2f2f2;"><strong>Modalidad</strong></td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{modality_proposal}</td>
                                </tr>
                            </table>

                            <p>Entendemos que recibir esta noticia puede ser desalentador, pero queremos asegurarte que valoramos tu iniciativa y experiencia. Consideramos que con algunos ajustes, tu propuesta podría ser un gran aporte para nuestra comunidad.</p>

                            <p>Te invitamos a:</p>
                            <ol>
                                <li>Revisar nuestras pautas para propuestas de cursos.</li>
                                <li>Considerar cómo podrías refinar o adaptar tu idea.</li>
                                <li>Contactarnos para discutir tu propuesta en detalle.</li>
                            </ol>

                            <p>Estamos aquí para apoyarte en el desarrollo de tu idea. Por favor, no dudes en contactarnos por WhatsApp o correo electrónico, según tu preferencia, para discutir cómo podemos trabajar juntos para mejorar tu propuesta.</p>

                            <p>Esperamos tener noticias tuyas pronto.</p>

                            <p>Saludos,<br>
                            Circle Up Community ⚫</p>
                        </div>
                    </td>
                </tr>
            </table>
        """

    try:
        with st.spinner(":material/send: Enviando email..."):
            email_sender.send_custom_email(recipient_email, full_name, subject, content)
            time.sleep(3)
            connector.update_document('course_proposal', volunteer_data['cloud_id'], {'notification': 'Send'})
            time.sleep(1)
            sheet = Sheets('1c_Pjefz-dtpBI2Yq6iPvPnSC5IkkWh7eCmdWaG39tzw','Proposals')
            sheet.replace_values(volunteer_data['cloud_id'],{'notification': 'Send'})
            time.sleep(2)
        st.success(f"Email enviado exitosamente a :green[**{full_name}**]", icon=":material/mail:")
    except Exception as e:
        st.error(f"Error al enviar el email: {str(e)}")




if __name__ == "__main__":
    try:
        connector = connector()
        manage_volunteer_requests(connector)
        menu()
        st.divider()
        st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
        if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
            st.switch_page('app.py')
    except:
        st.switch_page('app.py')

