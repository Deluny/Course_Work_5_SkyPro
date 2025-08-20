import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def create_database():
    """Создание базы данных и таблиц"""
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Создаем базу данных, если она не существует
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME}")

    cur.close()
    conn.close()

    # Подключаемся к созданной базе и создаем таблицы
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    with conn.cursor() as cur:
        # Создаем таблицу employers
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255)
            )
        """)

        # Создаем таблицу vacancies
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

    conn.commit()
    conn.close()
