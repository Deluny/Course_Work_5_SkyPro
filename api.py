from abc import ABC, abstractmethod
from typing import List, Optional

import requests

from models import Employer, Vacancy


class API(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_employer(self, employer_id: int) -> Optional[Employer]:
        pass

    @abstractmethod
    def get_vacancies(self, employer_id: int) -> List[Vacancy]:
        pass


class HeadHunterAPI(API):
    """Реализация API для HeadHunter"""

    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_employer(self, employer_id: int) -> Optional[Employer]:
        url = f"{self.base_url}/employers/{employer_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return Employer(
                employer_id=data['id'],
                name=data['name'],
                url=data.get('alternate_url')
            )
        return None

    def get_vacancies(self, employer_id: int) -> List[Vacancy]:
        url = f"{self.base_url}/vacancies?employer_id={employer_id}&per_page=100"
        response = requests.get(url)
        vacancies = []

        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                salary = item.get('salary')
                vacancies.append(Vacancy(
                    vacancy_id=item['id'],
                    employer_id=employer_id,
                    title=item['name'],
                    salary_from=salary.get('from') if salary else None,
                    salary_to=salary.get('to') if salary else None,
                    url=item.get('alternate_url')
                ))
        return vacancies