from typing import Dict

# Конфигурационные параметры
DB_CONFIG = {
    "dbname": "hh_vacancies",
    "user": "postgres",
    "password": "your_password",  # Замените на ваш пароль
    "host": "localhost",
    "port": "5432"
}

# Список компаний для анализа
COMPANIES: Dict[str, int] = {
    "Яндекс": 1740,
    "VK": 15478,
    "Сбер": 3529,
    "Тинькофф": 78638,
    "Ozon": 2180,
    "Kaspersky": 1057,
    "2ГИС": 64174,
    "СБАР": 888701,
    "Альфа-Банк": 80,
    "МТС": 3776
}