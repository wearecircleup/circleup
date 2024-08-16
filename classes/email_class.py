from dataclasses import dataclass
from typing import List, Optional, Any, Union
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from utils.email_templates import (pensum_html_file, pensum_plain_file,
                                pensum_html_anthropic, pensum_plain_anthropic,
                                claude_fb_html,claude_fb_plain,header)

import time
import streamlit as st
import datetime

class EmailSender:
    @staticmethod
    def create_message(sender: str, recipient: str, subject: str, plain_content: str, html_content: str, bcc: Optional[str] = None) -> MIMEMultipart:
        message = MIMEMultipart('alternative')
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = recipient
        if bcc:
            message["Bcc"] = bcc

        plain_mail = MIMEText(plain_content, 'plain')
        html_mail = MIMEText(html_content, 'html')
        message.attach(plain_mail)
        message.attach(html_mail)
        
        return message

    @staticmethod
    def add_attachment(message: MIMEMultipart, attachment: Union[bytes, str], filename: str) -> None:
        if isinstance(attachment, str):
            attachment = attachment.encode('utf-8')
        
        attachment_part = MIMEApplication(attachment, Name=filename)
        attachment_part['Content-Disposition'] = f'attachment; filename="{filename}"'
        message.attach(attachment_part)

    @staticmethod
    def send_email(sender: str, password: str, recipient: str, message: MIMEMultipart, 
                smtp_server: str = 'smtp.gmail.com', smtp_port: int = 465, 
                max_retries: int = 3, retry_delay: int = 5) -> bool:
        for attempt in range(max_retries):
            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as server:
                    server.login(sender, password)
                    server.send_message(message)
                return True

            except smtplib.SMTPServerDisconnected as e:
                if attempt < max_retries - 1:
                    print(f"Error de conexión: {e}. Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    print(f"Error de conexión después de {max_retries} intentos: {e}")
                    return False

            except smtplib.SMTPSenderRefused as e:
                print(f"Error del servidor (421): {e}. Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)

            except Exception as e:
                print(f"Error al enviar correo: {e}")
                return False

@dataclass
class Email:
    sender: str = 'wearecircleup@gmail.com'
    password: str = str(st.secrets["MAIL_KEY"])
    bcc: str = 'wearecircleup@gmail.com'
    smtp_server: str = 'smtp.gmail.com'
    smtp_port: int = 465

    def send_pensum_xlsx(self, recipient: str, user_name: str, file: Any, course_name: str, max_retries=3, retry_delay=5):
        subject = f'{user_name.upper()}-PENSUM'
        file_name = f"PENSUM | {user_name.upper()}.xlsx"

        plain = pensum_plain_file(user_name, recipient, course_name)
        html = pensum_html_file(user_name, recipient, course_name)
        
        message = EmailSender.create_message(self.sender, recipient, subject, plain, html, self.bcc)
        EmailSender.add_attachment(message, file.getvalue(), file_name)
        
        return EmailSender.send_email(
            sender=self.sender, 
            password=self.password, 
            recipient=recipient, 
            message=message,
            smtp_server=self.smtp_server, 
            smtp_port=self.smtp_port, 
            max_retries=max_retries, 
            retry_delay=retry_delay
        )
    
    def send_claude_feedback(self,recipient:str,user_name:str,feedback:str,max_retries=3, retry_delay=5):
        subject = f'{user_name.upper()}-PENSUM'

        plain = claude_fb_plain(user_name, recipient, feedback)
        html = claude_fb_html(user_name, recipient, feedback)

        message = EmailSender.create_message(self.sender, recipient, subject, plain, html, self.bcc)

        return EmailSender.send_email(
            sender=self.sender, 
            password=self.password, 
            recipient=recipient, 
            message=message,
            smtp_server=self.smtp_server, 
            smtp_port=self.smtp_port, 
            max_retries=max_retries, 
            retry_delay=retry_delay
        )


    def send_pensum_anthropic_prompt(self, user: str, user_name: str, course_name: str, plain_pensum: str, max_retries=3, retry_delay=5):
        subject = f'{user_name}-PENSUM'
        file_name = f"PENSUM | {user_name.upper()} | {datetime.datetime.today().strftime('%Y-%m-%d')}.txt"
        recipient = self.sender

        plain = pensum_plain_anthropic(user_name, user, course_name)
        html = pensum_html_anthropic(user_name, user, course_name)

        message = EmailSender.create_message(self.sender, recipient, subject, plain, html, self.bcc)
        EmailSender.add_attachment(message, plain_pensum, file_name)

        return EmailSender.send_email(
            sender=self.sender, 
            password=self.password, 
            recipient=recipient, 
            message=message,
            smtp_server=self.smtp_server, 
            smtp_port=self.smtp_port, 
            max_retries=max_retries, 
            retry_delay=retry_delay
        )
    

    def send_custom_email(self, recipient: str, user_name: str, subject: str, content: str, max_retries=3, retry_delay=5):
        
        plain = content
        html = f""" <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50; margin: 0; padding: 0;">
                        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 95%; margin: 0 auto;">
                            <tr>
                                <td style="padding: 20px;">
                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border-radius: 10px; overflow: hidden;">
                                        <tr>
                                            <td style="line-height: 0;">
                                                <img src="{header}" alt="Header" style="width: 100%; height: auto; display: block; border-radius: 10px;">
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <div style="padding: 20px;">
                                        {content}
                                    </div>
                                    
                                    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #400073; border-radius: 10px;">
                                        <tr>
                                            <td align="center" style="padding: 15px;">
                                                <a href="https://www.linkedin.com/company/circleup-community/" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin: 0 10px; text-decoration: none; color: white; font-weight: bold;">LinkedIn</a>
                                                <a href="https://wa.me/573046714626?text=Hola%20Circle%20Up%20Community!" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin: 0 10px; text-decoration: none; color: white; font-weight: bold;">WhatsApp</a>
                                                <a href="https://calendly.com/wearecircleup/15min" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin: 0 10px; text-decoration: none; color: white; font-weight: bold;">Calendly</a>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </body>
                    </html>
                """

        message = EmailSender.create_message(self.sender, recipient, subject, plain, html, self.bcc)

        return EmailSender.send_email(
            sender=self.sender, 
            password=self.password, 
            recipient=recipient, 
            message=message,
            smtp_server=self.smtp_server, 
            smtp_port=self.smtp_port, 
            max_retries=max_retries, 
            retry_delay=retry_delay
        )



