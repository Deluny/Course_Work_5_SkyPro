import requests
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, COMPANIES

def get_employer_data(employer_id):
    """Получение данных о работодателе по API"""
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_vacancies_data(employer_id):
    """Получение данных о вакансиях работодателя по API"""
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []


def insert_data_to_database():
    """Вставка данных в базу данных"""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    with conn.cursor() as cur:
        # Вставляем данные о работодателях
        for company_name, employer_id in COMPANIES.items():
            employer_data = get_employer_data(employer_id)

            if employer_data:
                # Вставляем данные работодателя
                cur.execute(
                    "INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s) "
                    "ON CONFLICT (employer_id) DO UPDATE SET name = EXCLUDED.name, url = EXCLUDED.url",
                    (employer_data['id'], employer_data['name'], employer_data['alternate_url'])
                )

                # Получаем и вставляем вакансии
                vacancies_data = get_vacancies_data(employer_id)
                for vacancy in vacancies_data:
                    salary = vacancy.get('salary')
                    salary_from = salary.get('from') if salary else None
                    salary_to = salary.get('to') if salary else None

                    cur.execute(
                        "INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url) "
                        "VALUES (%s, %s, %s, %s, %s, %s) "
                        "ON CONFLICT (vacancy_id) DO UPDATE SET "
                        "title = EXCLUDED.title, salary_from = EXCLUDED.salary_from, "
                        "salary_to = EXCLUDED.salary_to, url = EXCLUDED.url",
                        (vacancy['id'], employer_data['id'], vacancy['name'],
                         salary_from, salary_to, vacancy['alternate_url'])
                    )

        conn.commit()
        print("Данные успешно добавлены в базу данных!")

    conn.close()
