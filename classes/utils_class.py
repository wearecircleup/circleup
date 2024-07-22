from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CategoryUtils:
    @staticmethod
    def time_to_category() -> str:
        utc_now = datetime.utcnow()
        colombia_time = utc_now - timedelta(hours=5)
        
        time = colombia_time.strftime("%H:%M")

        categories = [
            "00:00-01:59", "02:00-03:59", "04:00-05:59", "06:00-07:59",
            "08:00-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:59",
            "16:00-17:59", "18:00-19:59", "20:00-21:59", "22:00-23:59"
        ]

        for category in categories:
            start, end = category.split("-")
            start_time = datetime.strptime(start, "%H:%M").time()
            end_time = datetime.strptime(end, "%H:%M").time()
            
            if start_time <= colombia_time.time() <= end_time:
                return category

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