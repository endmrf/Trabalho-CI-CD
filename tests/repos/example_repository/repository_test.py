import os
import uuid
import pytest
from unittest import mock
from faker import Faker
from src.infra.repo import ExampleRepository
from src.infra.config import DBConnectionHandler
from tests.mock_util import MockUtil

fake = Faker()
MOCK_DB_PATH = "sqlite:///mock_data.db"


def generate_uuid():
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def mock_entity():
    return {
        "id": str(uuid.uuid4()),
        "company_id": str(uuid.uuid4()),
        "name": fake.name(),
        "description": fake.text(),
    }


@pytest.fixture(scope="session")
@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def db_connection_handler():
    return DBConnectionHandler()


@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def test_example_repository_create(mock_entity, db_connection_handler):
    """
    Test the create action into Repository
    :param - None
    :return - None
    """

    company_id = mock_entity["company_id"]
    example_repository = ExampleRepository()

    data = example_repository.create_example(
        name=mock_entity["name"],
        description=mock_entity["description"],
        company_id=company_id,
    )

    engine = db_connection_handler.get_engine()
    query_entity = engine.execute(
        "SELECT * FROM examples WHERE id='{}'".format(data.id)
    ).fetchone()

    assert data.name == query_entity.name
    assert data.description == query_entity.description
    assert data.company_id == query_entity.company_id

    engine.execute("DELETE FROM examples WHERE company_id='{}'".format(data.company_id))

@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def test_example_repository_get(mock_entity, db_connection_handler):
    """
    Test get single INSTANCE action into Repository
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("examples", mock_entity))

    example_repository = ExampleRepository()
    data = example_repository.get_example(
        id=mock_entity["id"]
    )

    assert data.id == mock_entity["id"]
    assert data.name == mock_entity["name"]
    assert data.description == mock_entity["description"]
    assert data.company_id == mock_entity["company_id"]

    engine.execute(
        "DELETE FROM examples WHERE company_id='{}'".format(mock_entity["company_id"])
    )
