from dataclasses import dataclass, field
import pandas as pd
from typing import Optional, Any
import streamlit as st
from classes.email_class import Email
import datetime

@dataclass
class PensumLoader:
    file: Any
    pensum: Optional[str] = field(init=False)
    missing: Optional[str] = field(init=False)
    course: Optional[Any] = field(init=False)

    def __post_init__(self):
        self.missing = ""
        self.pensum = self.load_pensum()
        self.course = self.course_name()

    @staticmethod
    def load_sheet(file, sheet_name):
        feature = ['General Pensum', 'Respuesta']
        sheet = pd.read_excel(file, sheet_name=sheet_name)[feature]
        last_valid_row = sheet['General Pensum'].last_valid_index() + 1
        return sheet.iloc[:last_valid_row]

    def check_missing_data(self, sheet, sheet_name):
        missing_data = sheet[sheet.isnull().any(axis=1)]
        if not missing_data.empty:
            self.missing += '\n'.join(
                f"\n**Pagina** {sheet_name} | **Campo** {row['General Pensum']}"
                for idx, row in missing_data.iterrows()
            ) + "\n"

    @staticmethod
    def sheet_to_dict(sheet):
        result = []
        for key, value in sheet.set_index('General Pensum')['Respuesta'].to_dict().items():
            cleaned_key = key.replace('\n', '').lower()
            result.append(f"{cleaned_key}: {value}")
        return '\n'.join(result)

    def load_sheets(self, sheet_name):
        sheet = self.load_sheet(self.file, sheet_name)
        self.check_missing_data(sheet, sheet_name)
        return self.sheet_to_dict(sheet)

    def course_name(self):
        sheet = self.load_sheet(self.file, 'Información General').set_index('General Pensum').to_dict()['Respuesta']
        course = list(sheet.values())[0]
        return course
    
    def load_pensum(self):
        sheets = ['Información General', 'Estructura del Curso', 'Metodología', 'Evaluación', 'Recursos Adicionales', 'Experiencia']
        pensum = '\n'.join(self.load_sheets(sheet_name) for sheet_name in sheets)
        if not self.missing:
            self.missing = None
        return pensum