from dataclasses import dataclass
from datetime import datetime, timedelta, time

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
            .stMarkdown { font-size: 16px; line-height: 1.6; }
            h1 { font-size: 2rem; }
            h2 { font-size: 1.8rem; }
            h3 { font-size: 1.6rem; }
            h4 { font-size: 1.4rem; }
            p { font-size: 1rem; }
            
            /* Pantallas medianas (992px a 1199px) */
            @media screen and (max-width: 1199px) and (min-width: 992px) {
                .stMarkdown { font-size: 15px; }
                h1 { font-size: 1.9rem; }
                h2 { font-size: 1.7rem; }
                h3 { font-size: 1.5rem; }
                h4 { font-size: 1.3rem; }
            }
            
            /* Tablets (768px a 991px) */
            @media screen and (max-width: 991px) and (min-width: 768px) {
                .stMarkdown { font-size: 14px; }
                h1 { font-size: 1.8rem; }
                h2 { font-size: 1.6rem; }
                h3 { font-size: 1.4rem; }
                h4 { font-size: 1.2rem; }
            }
            
            /* Móviles grandes (576px a 767px) */
            @media screen and (max-width: 767px) and (min-width: 576px) {
                .stMarkdown { font-size: 12px; }
                h1 { font-size: 1.4rem; }
                h2 { font-size: 1.2rem; }
                h3 { font-size: 1rem; }
                h4 { font-size: 0.9rem; }
                p { font-size: 0.8rem; }
            }
            
            /* Móviles pequeños (hasta 575px) */
            @media screen and (max-width: 575px) {
                .stMarkdown { font-size: 8px; }
                h1 { font-size: 1rem; }
                h2 { font-size: 0.9rem; }
                h3 { font-size: 0.8rem; }
                h4 { font-size: 0.75rem; }
                p { font-size: 0.5rem; }
            }
        </style>
        """
        return style