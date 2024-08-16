from dataclasses import dataclass
from datetime import datetime, timedelta, time
import pytz
import locale

@dataclass
class CategoryUtils:
    @staticmethod
    def time_to_category() -> str:
        utc_now = datetime.utcnow()
        colombia_time = utc_now - timedelta(hours=5)
        
        current_time = colombia_time.time()

        categories = [
            ("00:00", "01:59"), ("02:00", "03:59"), ("04:00", "05:59"), ("06:00", "07:59"),
            ("08:00", "09:59"), ("10:00", "11:59"), ("12:00", "13:59"), ("14:00", "15:59"),
            ("16:00", "17:59"), ("18:00", "19:59"), ("20:00", "21:59"), ("22:00", "23:59")
        ]

        for start, end in categories:
            start_time = datetime.strptime(start, "%H:%M").time()
            end_time = datetime.strptime(end, "%H:%M").time()
            
            if start_time <= current_time <= end_time:
                return f"{start}-{end}"

        return "No encontrado"


    @staticmethod
    def format_date(fecha_str, city=''):
        dias_semana = {
            0: "Lunes",
            1: "Martes",
            2: "Miércoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sábado",
            6: "Domingo"
        }

        meses = {
            'January': 'enero',
            'February': 'febrero',
            'March': 'marzo',
            'April': 'abril',
            'May': 'mayo',
            'June': 'junio',
            'July': 'julio',
            'August': 'agosto',
            'September': 'septiembre',
            'October': 'octubre',
            'November': 'noviembre',
            'December': 'diciembre'
        }

        fecha = datetime.strptime(fecha_str, '%d-%m-%Y')
        zona_colombia = pytz.timezone('America/Bogota')
        fecha_colombia = zona_colombia.localize(fecha)

        # Usar el mapeo personalizado para el día de la semana
        dia_semana = dias_semana[fecha_colombia.weekday()]
        
        # Usar strftime para obtener el nombre del mes en inglés y luego traducirlo al español
        mes_ingles = fecha_colombia.strftime('%B')
        mes = meses[mes_ingles]
        
        dia = fecha_colombia.day
        año = fecha_colombia.year
        
        if city != '':
            city = ', ' + city

        return f"{dia_semana}, {dia} de {mes} de {año}{city}"
        
    @staticmethod
    def parental_review(birth_date_str: str) -> str:
        try:
            birth_date = datetime.strptime(birth_date_str, "%d-%m-%Y")
        except ValueError:
            return "Formato inválido"

        today = datetime.now()
        age = today.year - birth_date.year

        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
            
        if age <= 17:
            return "Pending"
        else:
            return "Not Applicable"

    @staticmethod
    def age_to_category(birth_date_str: str) -> str:
        try:
            birth_date = datetime.strptime(birth_date_str, "%d-%m-%Y")
        except ValueError:
            return "Formato inválido"

        today = datetime.now()
        age = today.year - birth_date.year

        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1

        categories = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60+"]

        if age >= 60:
            return "60+"
        for category in categories:
            start, end = map(int, category.split("-"))
            if start <= age <= end:
                return category

        return "No encontrado"

    @staticmethod
    def date_to_day_of_week() -> str:
        utc_now = datetime.utcnow()
        colombia_date = utc_now - timedelta(hours=5)
        
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        return days[colombia_date.weekday()]

    @staticmethod
    def get_current_date() -> str:
        utc_now = datetime.utcnow()
        colombia_date = utc_now - timedelta(hours=5)
        return colombia_date.strftime("%d-%m-%Y")
    

    @staticmethod
    def markdown_design() -> str:
        style = """
        <style>
            /* Estilos base */
            body, div, span, applet, object, iframe, p, blockquote, pre,
            a, abbr, acronym, address, big, cite, code,
            del, dfn, em, img, ins, kbd, q, s, samp,
            small, strike, strong, sub, sup, tt, var,
            b, u, i, center,
            dl, dt, dd, ol, ul, li,
            fieldset, form, label, legend,
            table, caption, tbody, tfoot, thead, tr, th, td,
            article, aside, canvas, details, embed, 
            figure, figcaption, footer, header, hgroup, 
            menu, nav, output, ruby, section, summary,
            time, mark, audio, video {
                font-size: 1.05rem;
            }

            /* Encabezados */
            h1, h2, h3 { font-size: 1.45rem; }
            h4 { font-size: 1.55rem; }
            h5, h6 { font-size: 1.35rem; }

            /* Elementos de texto específicos */
            .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
                font-size: 1.5rem;
            }

            /* Elementos de lista y tabla */
            li, td, th {
                font-size: 1.1rem;
            }

            /* Ajustes para elementos de código */
            code, pre {
                font-size: 1.1rem;
            }

            /* Ajustes para elementos de métrica */
            .stMetricValue {
                font-size: 1.55rem !important;
            }
            .stMetricLabel {
                font-size: 1.1rem !important;
            }
        </style>
        """
        return style