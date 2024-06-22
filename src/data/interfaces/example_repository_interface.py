from datetime import datetime
from abc import ABC, abstractmethod
from typing import List
from src.domain.models import Example


class ExampleRepositoryInterface(ABC):
    """Interface to Example Repository"""

    @abstractmethod
    def create_example(
        cls,
        name: str,
        description: str,
        json_data: dict,
        company_id: str,
        created_by: str = "SYSTEM",
        updated_by: str = "SYSTEM",
        datetime_created: datetime = datetime.utcnow(),
        datetime_updated: datetime = datetime.utcnow(),
    ) -> Example:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def get_example(self, id: str, company_id: str) -> Example:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def update_example(
        cls,
        id: str,
        name: str,
        description: str,
        json_data: dict,
        company_id: str,
        updated_by: str = "SYSTEM",
        datetime_updated: datetime = datetime.utcnow(),
    ) -> Example:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def delete_example(self, id: str, company_id: str) -> bool:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def select_examples(
        cls, company_id: str, name: str = "", description: str = ""
    ) -> List[Example]:
        """abstractmethod"""

        raise Exception("Method not implemented")
