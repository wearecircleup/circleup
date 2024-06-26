from dataclasses import dataclass, field
from typing import List, Optional
import ssl,smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from utils.email_templates import pensum_html,pensum_plain

from dataclasses import dataclass
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ssl
import time
import streamlit as st
import json
import datetime


@dataclass
class Email:
    sender: str = 'wearecircleup@gmail.com'
    password:str = str(st.secrets["service_password"])
    bcc: str = 'wearecircleup@gmail.com'
    smtp_server: str = 'smtp.gmail.com'
    smtp_port: int = 465

    def send_pensum(self,recipient, data,user_name,proposal, max_retries=3, retry_delay=5):
        
        file_name = f'{user_name.lower()}-anthropic | {datetime.datetime.today().strftime('%d-%m-%Y')}.txt'

        message = MIMEMultipart("alternative")
        message["Subject"] = 'Evaluación de Pensum @Circle Up'
        message["To"] = recipient
        message["From"] = self.sender
        message["Bcc"] = self.bcc

        text = pensum_plain(data)
        html = pensum_html(data,user_name)

        plain_mail = MIMEText(text, "plain")
        html_mail = MIMEText(html, "html")
        message.attach(plain_mail)
        message.attach(html_mail)
        
        if isinstance(proposal, str):
            proposal_bytes = proposal.encode('utf-8')
        elif isinstance(proposal, bytes):
            proposal_bytes = proposal
        else:
            proposal_bytes = str(proposal).encode('utf-8')

        attachment = MIMEApplication(proposal_bytes, Name=file_name)
        attachment['Content-Disposition'] = f'attachment; filename="{file_name}"'
        message.attach(attachment)

        for attempt in range(max_retries):
            try:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=ssl.create_default_context()) as server:
                    server.login(self.sender, self.password)
                    server.sendmail(self.sender, [recipient, self.bcc], message.as_string())
                return  True

            except smtplib.SMTPServerDisconnected as e:
                if attempt < max_retries - 1:  # Reintentar si no es el último intento
                    print(f"Error de conexión: {e}. Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    return False

            except smtplib.SMTPSenderRefused as e:
                # Manejar el error 421 aquí
                print(f"Error del servidor (421): {e}. Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)

            except Exception as e:  # Manejar otros errores de smtplib
                print(f"Error al enviar correo: {e}")
                return False
