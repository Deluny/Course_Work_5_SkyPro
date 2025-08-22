from typing import List, Dict, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from abc import ABC, abstractmethod


class DBManager(ABC):
    """Абстрактный класс для работы с данными в БД"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        pass


class PostgreSQLDBManager(DBManager):
    """Реализация DBManager для PostgreSQL"""

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.vacancy_id) as vacancies_count
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name
                ORDER BY vacancies_count DESC
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT e.name as company_name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                ORDER BY e.name, v.title
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to)/2) as avg_salary
                FROM vacancies 
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """)
            result = cur.fetchone()
            return result[0] if result[0] else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT e.name as company_name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE (v.salary_from + v.salary_to)/2 > %s
                ORDER BY (v.salary_from + v.salary_to)/2 DESC
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT e.name as company_name, v.title, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id
                WHERE LOWER(v.title) LIKE %s
                ORDER BY e.name, v.title
            """, (f'%{keyword.lower()}%',))
            return cur.fetchall()

    def close(self) -> None:
        """Закрытие соединения с базой данных"""
        self.conn.close()