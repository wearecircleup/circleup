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
        key_sheets = json.loads(st.secrets["DRIVE_KEY"])
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_info(key_sheets, scopes=scope)
        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(self.document_id).worksheet(self.sheet_name)

    def _find_row_by_email(self, email: str) -> int:
        try:
            return self.sheet.find(email).row
        except gspread.exceptions.CellNotFound:
            return -1

    @st.cache_data(ttl=900,show_spinner=False)
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
        
    def replace_values(self, cloud_id: str, updates: Dict[str, Any]) -> bool:
        try:
            # Obtener todas las cabeceras
            headers = self.sheet.row_values(1)
            
            # Encontrar el índice de la columna 'cloud_id'
            cloud_id_index = headers.index('cloud_id') + 1
            
            # Buscar la fila con el cloud_id especificado
            cell = self.sheet.find(cloud_id, in_column=cloud_id_index)
            if not cell:
                st.error(f"No se encontró ninguna fila con cloud_id: {cloud_id}")
                return False
            
            row = cell.row
            
            # Preparar las actualizaciones
            cells_to_update = []
            for column, value in updates.items():
                if column in headers:
                    col_index = headers.index(column) + 1
                    cell = self.sheet.cell(row, col_index)
                    cell.value = value
                    cells_to_update.append(cell)
                else:
                    st.warning(f"La columna '{column}' no existe en la hoja. Se omitirá.")
            
            # Realizar las actualizaciones en lote
            if cells_to_update:
                self.sheet.update_cells(cells_to_update)
                return True
            else:
                st.warning("No se realizaron actualizaciones.")
                return False
            
        except gspread.exceptions.APIError as e:
            st.error(f"Error de API al actualizar los valores: {str(e)}")
            return False
        except Exception as e:
            st.error(f"Error al actualizar los valores: {str(e)}")
            return False

    @st.cache_data(ttl=900,show_spinner=False)
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

    @st.cache_data(ttl=900,show_spinner=False)
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

    @st.cache_data(ttl=900,show_spinner=False)
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