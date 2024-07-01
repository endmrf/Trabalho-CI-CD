from collections import namedtuple
from src.domain.use_cases import CreateExampleUseCaseInterface
from src.infra.repo import ExampleRepository

CreateExampleParameter = namedtuple(
    "CreateExampleParameter",
    "name description json_data company_id created_by updated_by datetime_created datetime_updated",
)


class CreateExampleUseCase(CreateExampleUseCaseInterface):
    """
    Use case gateway for create a new Example entity
    """

    repository = ExampleRepository()

    def proceed(self, parameter: CreateExampleParameter) -> dict:
        """
        Proceed the execution of use case by calling database to create a new single entity with parameters
        :param  - parameter: An Interfaced object with required data
        :return - A Dictionary with formated response of the request having 'success' and 'data' objects
        """

        try:
            record = self.repository.create_example(
                name=parameter.name,
                description=parameter.description,
                json_data=parameter.json_data,
                company_id=parameter.company_id,
                created_by=parameter.created_by,
                updated_by=parameter.updated_by,
                datetime_created=parameter.datetime_created,
                datetime_updated=parameter.datetime_updated,
            )
            serialized_record = record._asdict()
            return self._render_response(True, serialized_record)
        except:
            return self._render_response(False, None)
