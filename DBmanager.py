import psycopg2
from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

class DBManager:
    def __init__(self, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST):
        self.conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host
        )

    def get_companies_and_vacancies_count(self):
        """Список компаний с количеством вакансий"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.vacancy_id) 
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Все вакансии с указанием компании"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.title, v.salary_from, v.salary_to, v.url 
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        """Средняя зарплата по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to)/2) 
                FROM vacancies 
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Вакансии с зарплатой выше средней"""
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM vacancies 
                WHERE (salary_from + salary_to)/2 > {avg}
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Поиск вакансий по ключевому слову"""
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM vacancies 
                WHERE title LIKE '%{keyword}%'
            """)
            return cur.fetchall()

    def __del__(self):
        self.conn.close()