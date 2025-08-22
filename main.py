from DBmanager import PostgreSQLDBManager
from api import HeadHunterAPI
from config import DB_CONFIG, COMPANIES
from database import Database


def create_database() -> None:
    """Создание базы данных и таблиц"""
    db = Database(**DB_CONFIG)
    db.create_tables()
    db.close()


def fill_database() -> None:
    """Заполнение базы данных данными о компаниях и вакансиях"""
    api = HeadHunterAPI()
    db = Database(**DB_CONFIG)

    for company_name, employer_id in COMPANIES.items():
        # Получаем данные о работодателе
        employer = api.get_employer(employer_id)
        if employer:
            db.insert_employer(employer)
            print(f"Добавлен работодатель: {employer.name}")

        # Получаем данные о вакансиях
        vacancies = api.get_vacancies(employer_id)
        for vacancy in vacancies:
            db.insert_vacancy(vacancy)

        print(f"Добавлено вакансий для {company_name}: {len(vacancies)}")

    db.close()


def user_interaction() -> None:
    """Взаимодействие с пользователем"""
    db_manager = PostgreSQLDBManager(**DB_CONFIG)

    while True:
        print("\nВыберите действие:")
        print("1. Получить список всех компаний и количество вакансий")
        print("2. Получить список всех вакансий")
        print("3. Получить среднюю зарплату по вакансиям")
        print("4. Получить вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            print("\nКомпании и количество вакансий:")
            for company in companies:
                print(f"{company['name']}: {company['vacancies_count']} вакансий")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            print("\nВсе вакансии:")
            for vacancy in vacancies:
                salary_info = f"{vacancy['salary_from']} - {vacancy['salary_to']}" if vacancy['salary_from'] or vacancy[
                    'salary_to'] else "Не указана"
                print(f"{vacancy['company_name']}: {vacancy['title']} ({salary_info}) - {vacancy['url']}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"\nСредняя зарплата по вакансиям: {avg_salary:.2f} руб.")

        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for vacancy in vacancies:
                salary_info = f"{vacancy['salary_from']} - {vacancy['salary_to']}" if vacancy['salary_from'] or vacancy[
                    'salary_to'] else "Не указана"
                print(f"{vacancy['company_name']}: {vacancy['title']} ({salary_info}) - {vacancy['url']}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nРезультаты поиска по слову '{keyword}':")
            for vacancy in vacancies:
                salary_info = f"{vacancy['salary_from']} - {vacancy['salary_to']}" if vacancy['salary_from'] or vacancy[
                    'salary_to'] else "Не указана"
                print(f"{vacancy['company_name']}: {vacancy['title']} ({salary_info}) - {vacancy['url']}")

        elif choice == "0":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

    db_manager.close()


if __name__ == "__main__":
    print("Создание базы данных и таблиц...")
    create_database()

    print("Заполнение базы данных данными...")
    fill_database()

    print("Запуск пользовательского интерфейса...")
    user_interaction()