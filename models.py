from dataclasses import dataclass
from typing import Optional

@dataclass
class Employer:
    """Модель работодателя"""
    employer_id: int
    name: str
    url: Optional[str] = None

@dataclass
class Vacancy:
    """Модель вакансии"""
    vacancy_id: int
    employer_id: int
    title: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    url: Optional[str] = None