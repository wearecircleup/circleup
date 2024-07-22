from dataclasses import dataclass
from typing import List, Dict, Any
import json
import gspread
from google.oauth2 import service_account
import streamlit as st

@dataclass
class Sheets:
    document_id: str
    sheet_name: str

    def __post_init__(self):
        key_sheets = json.loads(st.secrets["sheetskey"])
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_info(key_sheets, scopes=scope)
        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(self.document_id).worksheet(self.sheet_name)

    def _find_row_by_email(self, email: str) -> int:
        try:
            return self.sheet.find(email).row
        except gspread.exceptions.CellNotFound:
            return -1

    @st.cache_data(ttl=3600)
    def create(self, data: List[List[str]]) -> bool:
        try:
            # Asegurarse de que data sea una lista de listas
            if not isinstance(data[0], list):
                data = [data]
            
            # Obtener el número actual de filas
            num_rows = len(self.sheet.get_all_values())
            
            # Insertar las nuevas filas
            for row in data:
                num_rows += 1
                self.sheet.insert_row(row, num_rows)
            
            return True
        except gspread.exceptions.APIError as e:
            st.error(f"Error de API al crear el registro: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Error al crear el registro: {str(e)}")
            return False

    @st.cache_data(ttl=3600)
    def update(self, email: str, new_data: List[str]) -> bool:
        try:
            row = self._find_row_by_email(email)
            if row != -1:
                self.sheet.update(f'A{row}:Z{row}', [new_data])
                return True
            else:
                st.warning(f"No se encontró ningún registro con el email: {email}")
                return False
        except Exception as e:
            st.error(f"Error al actualizar el registro: {str(e)}")
            return False

    @st.cache_data(ttl=3600)
    def delete(self, email: str) -> bool:
        try:
            row = self._find_row_by_email(email)
            if row != -1:
                self.sheet.delete_rows(row)
                return True
            else:
                st.warning(f"No se encontró ningún registro con el email: {email}")
                return False
        except Exception as e:
            st.error(f"Error al eliminar el registro: {str(e)}")
            return False

    @st.cache_data(ttl=3600)
    def read(self, email: str = None) -> List[Dict[str, Any]]:
        try:
            if email:
                row = self._find_row_by_email(email)
                if row != -1:
                    values = self.sheet.row_values(row)
                    headers = self.sheet.row_values(1)
                    return [dict(zip(headers, values))]
                else:
                    st.warning(f"No se encontró ningún registro con el email: {email}")
                    return []
            else:
                all_values = self.sheet.get_all_records()
                return all_values
        except Exception as e:
            st.error(f"Error al leer los datos: {str(e)}")
            return []

# Ejemplo de uso:
# transaction = ExcelTransaction('1QArb7G_XG2sgOlx68S9oU0RYpDdcbzwJ_uSd0pbejmE', 'Hoja1')
# transaction.create([['21-07-2024', '20:14', 'Nicolas', 'Munevar', '25-29', 'gocircleup@gmail.com', 'Admin', 'Zipaquira']])
# transaction.update('gocircleup@gmail.com', ['21-07-2024', '20:14', 'Nicolas', 'Munevar Updated', '25-29', 'gocircleup@gmail.com', 'User', 'Bogota'])
# transaction.delete('gocircleup@gmail.com')
# data = transaction.read('gocircleup@gmail.com')
# all_data = transaction.read()