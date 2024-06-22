# pylint: disable=E1101

import uuid
from datetime import datetime
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import String
from src.data.interfaces import ExampleRepositoryInterface
from src.domain.models import Example
from src.infra.config import DBConnectionHandler
from src.infra.entities import Example as ExampleModel


class ExampleRepository(ExampleRepositoryInterface):
    """Class to manage Example Repository"""

    __db_connection: DBConnectionHandler = None

    @classmethod
    def db_connection_instance(cls):
        if not cls.__db_connection:
            cls.__db_connection = DBConnectionHandler()
        return cls.__db_connection

    def __build_entiy_to_domain_interface(
        self, entity_instance: ExampleModel
    ) -> Example:
        """
        Transform infra Entity Example into named tuple domain model Example
        :param  - entity_instance: A ExampleModel
        :return - A domain Example
        """

        domain_entity = Example(
            id=entity_instance.id,
            name=entity_instance.name,
            description=entity_instance.description,
            company_id=entity_instance.company_id,
            created_by=entity_instance.created_by,
            updated_by=entity_instance.updated_by,
            datetime_created=entity_instance.datetime_created,
            datetime_updated=entity_instance.datetime_updated,
        )
        return domain_entity

    def create_example(
        self,
        name: str,
        description: str,
        company_id: str,
        created_by: str = "SYSTEM",
        updated_by: str = "SYSTEM",
        datetime_created: datetime = datetime.utcnow(),
        datetime_updated: datetime = datetime.utcnow(),
    ) -> Example:
        """
        Create new Example
        :param  - name: The name of the Example
                - description: The description of the Example
                - created_by: ID of the User doing create action, (default is 'SYSTEM')
                - datetime_created: Datetime of create action, (default is now())
                - updated_by: ID of the User doing update action, (default is 'SYSTEM')
                - datetime_updated: Datetime of update action, (default is now())
        :return - A Example created
        """

        with self.db_connection_instance() as db_connection:
            try:
                id = str(uuid.uuid4())
                entity_instance = ExampleModel(
                    id=id,
                    name=name,
                    description=description,
                    company_id=company_id,
                    created_by=created_by,
                    updated_by=updated_by,
                    datetime_created=datetime_created,
                    datetime_updated=datetime_updated,
                )
                db_connection.session.add(entity_instance)
                db_connection.session.commit()

                return self.__build_entiy_to_domain_interface(entity_instance)

            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()


    def update_example(
        self,
        id: str,
        name: str,
        description: str,
        company_id: str,
        updated_by: str = "SYSTEM",
        datetime_updated: datetime = datetime.utcnow(),
    ) -> Example:
        """
        Update data in Example
        :param  - id: ID of the Example
                - name: The name of the Example
                - description: The description of the Example
                - updated_by: ID of the User doing update action, (default is 'SYSTEM')
                - datetime_updated: Datetime of update action, (default is now())
        :return - A Example updated
        """

        with self.db_connection_instance() as db_connection:
            try:
                entity_instance = db_connection.session.get(ExampleModel, id)
                entity_instance.name = name
                entity_instance.description = description
                entity_instance.company_id = company_id
                entity_instance.updated_by = updated_by
                entity_instance.datetime_updated = datetime_updated
                db_connection.session.merge(entity_instance)
                db_connection.session.commit()

                return self.__build_entiy_to_domain_interface(entity_instance)
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None

    def delete_example(self, id: str, company_id: str) -> bool:
        """
        Delete Example by ID
        :param  - id: ID of Example
                - company_id: ID of Example company
        :return - If deleteion has been succeeded
        """

        with self.db_connection_instance() as db_connection:
            try:
                entity_instance = (
                    db_connection.session.query(ExampleModel)
                    .filter(
                        ExampleModel.id == id, ExampleModel.company_id == company_id
                    )
                    .first()
                )
                db_connection.session.delete(entity_instance)
                db_connection.session.commit()
                return True
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return False

    def select_examples(
        self, company_id: str, name: str = "", description: str = ""
    ) -> List[Example]:
        """
        Search Example by company and filter by name and/or desciption
        :param  - company_id: ID of Example company
                - name: The name of Example
                - description: The descriptions of Example
        :return - List of found Example
        """

        query_data = None
        with self.db_connection_instance() as db_connection:
            try:
                query_data = (
                    db_connection.session.query(ExampleModel).filter(
                        ExampleModel.company_id == company_id,
                        ExampleModel.name.ilike("%" + name + "%"),
                        ExampleModel.description.ilike("%" + description + "%"),
                    )
                ).all()
                return list(
                    map(
                        lambda instance: self.__build_entiy_to_domain_interface(
                            instance
                        ),
                        query_data,
                    )
                )
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None

    def get_example(self, id: str, company_id: str) -> Example:
        """
        Retrieve Example by ID and company ID
        :param  - id: ID of the Example
                - company_id: ID of Example company
        :return - A found Example by ID
        """

        query_data = None
        with self.db_connection_instance() as db_connection:
            try:
                query_data = (
                    db_connection.session.query(ExampleModel).filter(
                        ExampleModel.id == id, ExampleModel.company_id == company_id
                    )
                ).first()
                if query_data is not None:
                    return self.__build_entiy_to_domain_interface(query_data)
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None
