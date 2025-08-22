from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from models import Employer, Vacancy


class Database:
    """Класс для работы с базой данных"""

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def create_tables(self) -> None:
        """Создание таблиц в базе данных"""
        with self.conn.cursor() as cur:
            # Таблица employers
            cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url VARCHAR(255)
                )
            """)

            # Таблица vacancies
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id INTEGER PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    title VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    url VARCHAR(255)
                )
            """)
            self.conn.commit()

    def insert_employer(self, employer: Employer) -> None:
        """Добавление работодателя в базу данных"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s) "
                "ON CONFLICT (employer_id) DO UPDATE SET name = EXCLUDED.name, url = EXCLUDED.url",
                (employer.employer_id, employer.name, employer.url)
            )
            self.conn.commit()

    def insert_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в базу данных"""
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO vacancies (vacancy_id, employer_id, title, salary_from, salary_to, url) "
                "VALUES (%s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (vacancy_id) DO UPDATE SET "
                "title = EXCLUDED.title, salary_from = EXCLUDED.salary_from, "
                "salary_to = EXCLUDED.salary_to, url = EXCLUDED.url",
                (vacancy.vacancy_id, vacancy.employer_id, vacancy.title,
                 vacancy.salary_from, vacancy.salary_to, vacancy.url)
            )
            self.conn.commit()

    def close(self) -> None:
        """Закрытие соединения с базой данных"""
        self.conn.close()