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
from google.cloud.exceptions import NotFound, Conflict
from googleapiclient.errors import HttpError
import firebase_admin.exceptions
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')


st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)
st.session_state.page_selected = None


@st.cache_resource
def connector():
    key_firestore = json.loads(st.secrets["FIREBASE_KEY"])
    db = firestore.Client.from_service_account_info(key_firestore)
    Conn = Firestore(db)
    return Conn


menu()


def manage_volunteer_requests(connector: Firestore):
    st.title("Gestión de Solicitudes de Voluntarios")
    st.info("Gestione las solicitudes de voluntarios pendientes, aprobadas y denegadas.", icon=":material/table_chart:")
    if st.button("Actualizar datos", use_container_width=True, type='secondary'):
        st.cache_data.clear()
        st.rerun()
        
    # Lista de estados
    status_options = ["Pending", "Approved", "Denied"]
    selected_status = st.selectbox("Seleccione el estado de las solicitudes:", status_options)

    # Cargar solicitudes de voluntarios según el estado seleccionado
    volunteer_requests = connector.query_collection('volunteer_request', [('status', '==', selected_status)])
    
    if not volunteer_requests:
        st.warning(f"No hay solicitudes con estado {selected_status}.", icon=":material/notifications:")
    
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
                st.write(f"**Id:** {selected_request.data.get('cloud_id_user')}")
                st.write(f"**Experiencia:** {selected_request.data.get('experience')} año(s)")
                st.write(f"**Disponibilidad:** {selected_request.data.get('availability')}")
                st.write(f"**Tiempo disponible:** {selected_request.data.get('time_availability')}")
                st.write(f"**Compromiso:** {selected_request.data.get('commitment')} Hr./Mes")
            
            st.write(f"**Motivación:** {selected_request.data.get('motivation')}")
            st.write(f"**Notificación:** :blue[**{selected_request.data.get('notification')}**]")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Aprobar solicitud", use_container_width=True, disabled=selected_status == 'Approved'):
                    approve_request(connector, selected_request.data.get('cloud_id_user'), selected_request.data.get('cloud_id'))
                    st.success(f"Solicitud aprobada con éxito.", icon=":material/check_circle:")
            with col2:
                if st.button("Denegar solicitud", use_container_width=True, disabled=selected_status == 'Denied'):
                    deny_request(connector, selected_request.data.get('cloud_id_user'), selected_request.data.get('cloud_id'))
                    st.success(f"Solicitud denegada con éxito.", icon=":material/cancel:")

            email_button_disabled = selected_status == 'Pending' or selected_request.data.get('notification') == 'Send'
            if st.button("Enviar Email de Notificación", disabled=email_button_disabled, use_container_width=True):
                send_notification_email(connector, selected_request.data)

def approve_request(connector: Firestore, cloud_id_user: str,cloud_id: str):
    try:
        # Actualizar el rol de usuario a 'Volunteer' en users_collection
        connector.update_document('users_collection', cloud_id_user, {'user_role': 'Volunteer'})
        with st.spinner(":material/sync: Asignando Rol Voluntario... Esto puede tardar ~5 segs"):
            time.sleep(4)
        # Actualizar el estado a 'Approved' y la notificación a 'Pending' en volunteer_request
        connector.update_document('volunteer_request', cloud_id, {'status': 'Approved', 'notification': 'Pending', 'user_role': 'Volunteer'})
        with st.spinner(":material/schedule_send: Creando Notificación Aprovado... Esto puede tardar ~5 segs"):
            time.sleep(4)
        # Update Google Sheets
        last_update = CategoryUtils().get_current_date()
        sheet = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM', 'Be Volunteer')
        sheet.replace_values(cloud_id, {'status': 'Approved', 'notification': 'Pending', 'user_role': 'Volunteer', 'last_update': last_update})

    except NotFound as e:
        st.error(f"Error: El documento con ID {cloud_id} no fue encontrado. Detalles: {str(e)}")
        return

    except Conflict as e:
        st.error(f"Error: Conflicto al actualizar el documento. Puede que ya haya sido modificado. Detalles: {str(e)}")
        return

    except firebase_admin.exceptions.FirebaseError as e:
        st.error(f"Error de Firebase: {str(e)}")
        return

    except HttpError as e:
        st.error(f"Error al actualizar Google Sheets: {str(e)}")
        return

    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return

    st.success("La solicitud ha sido aprobada exitosamente.")
    st.rerun()

def deny_request(connector: Firestore, cloud_id_user: str,cloud_id: str):
    try:
        # Actualizar el rol de usuario a 'Learner' en users_collection
        connector.update_document('users_collection', cloud_id_user, {'user_role': 'Learner'})
        with st.spinner(":material/sync: Asignando Rol Learner... ~5 segs"):
            time.sleep(4)
        # Actualizar el estado a 'Denied' y la notificación a 'Pending' en volunteer_request
        connector.update_document('volunteer_request', cloud_id, {'status': 'Denied', 'notification': 'Pending', 'user_role': 'Learner'})
        with st.spinner(":material/schedule_send: Creando Notificación Denegado... ~5 segs"):
            time.sleep(4)
        last_update = CategoryUtils().get_current_date()
        sheet = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM', 'Be Volunteer')
        sheet.replace_values(cloud_id, {'status': 'Denied', 'notification': 'Pending', 'user_role': 'Learner', 'last_update': last_update})

    except NotFound as e:
        st.error(f"Error: El documento con ID {cloud_id} no fue encontrado. Detalles: {str(e)}")
        return

    except Conflict as e:
        st.error(f"Error: Conflicto al actualizar el documento. Puede que ya haya sido modificado. Detalles: {str(e)}")
        return

    except firebase_admin.exceptions.FirebaseError as e:
        st.error(f"Error de Firebase: {str(e)}")
        return

    except HttpError as e:
        st.error(f"Error al actualizar Google Sheets: {str(e)}")
        return

    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return

    st.success("La solicitud ha sido denegada exitosamente.")
    st.rerun()

def send_notification_email(connector: Firestore, volunteer_data: dict):
    email_sender = Email()
    full_name = f"{volunteer_data['first_name']} {volunteer_data['last_name']}"
    recipient_email = volunteer_data['email']
    is_approved = volunteer_data['status'] == 'Approved'

    if is_approved:
        subject = "¡Bienvenid@ Solicitud aprobada!"

        content = f"""
            <p>Hola <strong>{full_name}</strong>,</p>

            <p>¡Felicitaciones! Tu solicitud para ser voluntario/a en <strong>Circle Up Community</strong> ha sido <strong>aprobada</strong>. Estamos muy contentos de tenerte con nosotros.</p>
            <p>Queremos que tu experiencia sea increíble y sencilla. Aquí está lo que necesitas saber:</p>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr>
                    <th style="text-align: left; padding: 12px; background-color: #f2f2f2; border: 1px solid #ddd; width: 30%;">Tu compromiso</th>
                    <td style="padding: 12px; border: 1px solid #ddd;">
                        • 2 horas para co-crear tu curso con nosotros<br>
                        • 2 horas para dar la clase<br>
                        <strong>¡Solo 4 horas en total!</strong>
                    </td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 12px; background-color: #f2f2f2; border: 1px solid #ddd;">Desarrollo del curso</th>
                    <td style="padding: 12px; border: 1px solid #ddd;">
                        • Tú aportas tus ideas y conocimientos<br>
                        • Nosotros creamos el 90% del material y la presentación
                    </td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 12px; background-color: #f2f2f2; border: 1px solid #ddd;">Detalles de tu clase</th>
                    <td style="padding: 12px; border: 1px solid #ddd;">
                        Piensa en:<br>
                        • ¿Qué sábado te gustaría dar la clase? (Preferimos presencial)<br>
                        • ¿Cuántas personas máximo aceptarías?<br>
                        • ¿Qué edades crees que serían las mejores para tu curso?
                    </td>
                </tr>
                <tr>
                    <th style="text-align: left; padding: 12px; background-color: #f2f2f2; border: 1px solid #ddd;">Próximo paso</th>
                    <td style="padding: 12px; border: 1px solid #ddd;">
                        <a href="https://calendly.com/wearecircleup/15min" style="color: #0066cc; text-decoration: none;">Agenda una reunión con nosotros</a> para planear todo
                    </td>
                </tr>
            </table>

            <p>Recuerda, estamos aquí para ayudarte en cada paso. Queremos que disfrutes compartiendo tu conocimiento con la comunidad.</p>

            <p><strong>¡Gracias por unirte! Tu aporte va a hacer una gran diferencia.</strong></p>

            <p>Un abrazo,<br>
            Circle Up Community ⚫</p>
            """
    else:
        subject = "Solicitud Voluntariado"
        content = f"""
        <p>Estimado/a <strong>{full_name}</strong>,</p>

        <p>Gracias por tu interés en ser voluntario/a en <strong>Circle Up</strong>.</p>
        <p>Lamentamos informarte que en esta ocasión <strong>no podemos aprobar tu solicitud de voluntariado</strong>.</p>
        <p>Apreciamos sinceramente tu deseo de contribuir y te animamos a seguir buscando oportunidades para marcar la diferencia en tu comunidad.</p>
        <p>Si tienes alguna pregunta o te gustaría obtener más información sobre nuestra decisión, no dudes en contactarnos.</p>
        
        <p><strong>Te deseamos lo mejor en tus futuros esfuerzos de voluntariado.</strong></p>

        <p>Atentamente,<br>
        Circle Up Community ⚫</p>
        """

    try:
        email_sender.send_custom_email(recipient_email, full_name, subject, content)
        with st.spinner(":material/schedule_send: Enviando Notificación... ~5 segs"):
            time.sleep(4)
        try:
            with st.spinner(":material/schedule_send: Confirmando Notificación... ~5 segs"):
                time.sleep(4)
            connector.update_document('volunteer_request', volunteer_data['cloud_id'], {'notification': 'Send'})
        except NotFound:
            st.error(f"Error: No se encontró el documento del voluntario en Firestore.")
            return
        except Conflict:
            st.warning(f"Advertencia: Conflicto al actualizar el documento en Firestore. Puede que ya haya sido modificado.")
        except firebase_admin.exceptions.FirebaseError as e:
            st.error(f"Error de Firebase al actualizar el documento: {str(e)}")
            return
        
        try:
            last_update = CategoryUtils().get_current_date()
            sheet = Sheets('1lAPcVR3e7MqUJDt2ys25eRY7ozu5HV61ZhWFYuMULOM','Be Volunteer')
            with st.spinner(":material/sync: Actualizar Notificaciónes... ~5 segs"):
                time.sleep(4)
            sheet.replace_values(volunteer_data['cloud_id'],{'notification': 'Send','last_update':last_update})
        except HttpError as e:
            st.error(f"Error al actualizar Google Sheets: {str(e)}")
            return
        
        st.success(f"Email enviado exitosamente a {full_name}", icon=":material/mark_email_read:")
    
    except smtplib.SMTPException as e:
        st.error(f"Error al enviar el email: {str(e)}")
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")


if __name__ == "__main__":
    try:
        connector = connector()
        manage_volunteer_requests(connector)
        st.divider()
        st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
        if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
            st.switch_page('app.py')
    except:
        st.switch_page('app.py')