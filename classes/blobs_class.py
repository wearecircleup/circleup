import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Any
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

@dataclass
class GoogleBlobs:
    folder_id: str

    def __post_init__(self):
        key_drive = json.loads(st.secrets["sheetskey"])
        scope = ['https://www.googleapis.com/auth/drive.file']
        creds = service_account.Credentials.from_service_account_info(key_drive, scopes=scope)
        self.drive_service = build('drive', 'v3', credentials=creds)

    def upload_file(self, file: Any) -> str:
      try:
          file_metadata = {
              'name': file.name,
              'parents': [self.folder_id]
          }
          mimetype = 'application/pdf' if file.type == 'application/pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
          media = MediaIoBaseUpload(file, mimetype=mimetype, resumable=True)
          file = self.drive_service.files().create(
              body=file_metadata,
              media_body=media,
              fields='webViewLink'
          ).execute()
          
          # Extraer y procesar el enlace
          full_link = file.get('webViewLink', '')
          processed_link = full_link.split('/view')[0] + '/view' if '/view' in full_link else full_link
          
          return processed_link
      except Exception as e:
          st.error(f"Error al subir el archivo: {str(e)}")
          return None