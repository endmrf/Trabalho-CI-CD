from collections import namedtuple
from src.domain.use_cases import GetExampleUseCaseInterface
from src.infra.repo import ExampleRepository

GetExampleParameter = namedtuple("GetExampleParameter", "id")


class GetExampleUseCase(GetExampleUseCaseInterface):
    """
    Use case gateway for get single Example entity
    """

    repository = ExampleRepository()

    def proceed(self, parameter: GetExampleParameter) -> dict:
        """
        Proceed the execution of use case by calling database to retrieve single entity by ID
        :param  - parameter: An Interfaced object with required data
        :return - A Dictionary with formated response of the request having 'success' and 'data' objects
        """

        try:
            record = self.repository.get_example(
                id=parameter.id
            )
            serialized_record = record._asdict()
            return self._render_response(True, serialized_record)
        except:
            return self._render_response(False, None)
