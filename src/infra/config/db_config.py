import os
from typing import Union
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session


class DBConnectionHandler:
    """Sqlalchemy database connection"""

    def __init__(self, connection_string: Union[str, None] = None):

        self.log_enabled = os.getenv("LOG_AURORA") == "ENABLED"
        self.cluster_arn = os.getenv("AURORA_CLUSTER_ARN")
        self.secret_arn = os.getenv("AURORA_SECRET_ARN")
        self.database_name = os.getenv("AURORA_DATABASE_NAME")
        self.__connection_string: str = "postgresql+auroradataapi://:@/{}".format(
            self.database_name
        )

        if self.___has_test_database_environment():
            self.__connection_string = str(os.getenv("TEST_DATABASE_CONNECTION"))

        if connection_string is not None:
            self.__connection_string = connection_string

        engine = self.get_engine()
        session_maker = sessionmaker()
        self.session = session_maker(bind=engine)

    def ___is_aurora_serverless_available(self) -> bool:
        """Returna Se banco de dados aurora esta disponível
        :parram - None
        :return - bool: Se banco de dados aurora esta disponível
        """

        return self.cluster_arn is not None and self.secret_arn is not None

    def ___has_test_database_environment(self) -> bool:
        """Retorna se existe variavel de ambiente para banco de dados para testes
        :parram - None
        :return - bool: Se existe variavel de ambiente para banco de dados para testes
        """

        env_var_name = "TEST_DATABASE_CONNECTION"
        return os.getenv(env_var_name) is not None and os.getenv(env_var_name)  # type: ignore

    def get_engine(self, print_only=False):
        """Return connection Engine
        :parram - None
        :return - engine connection to Database
        """

        if self.___is_aurora_serverless_available():
            # Aurora RDS connection
            engine = create_engine(
                self.__connection_string,
                echo=self.log_enabled,
                connect_args=dict(
                    aurora_cluster_arn=self.cluster_arn, secret_arn=self.secret_arn
                ),
            )
        elif print_only is False:
            connection_string = f"{self.__connection_string}?"
            if "sqlite" in connection_string:
                connection_string += "check_same_thread=false"
            engine = create_engine(connection_string, query_cache_size=0)

        else:
            # Mocking only
            engine = create_engine(
                self.__connection_string,
                query_cache_size=0,
                echo=self.log_enabled,
                strategy="mock",
                executor=self.metadata_dump,
            )
        self.engine = engine
        return self.engine

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session is not None:
            self.session.close()

    def metadata_dump(self, sql, *multiparams, **params):
        # print or write to log or file etc
        if self.engine is not None:
            print(sql.compile(dialect=self.engine.dialect))
        else:
            print("Error at compiling engine. Engine was None at time of compilation")

    def create_temporary_session(self):
        temporary_session: Session = self.scoped_session_maker()
        return temporary_session

    def func_group_concat(self, column_criteria: any, separator: str):
        """
        Returns correlated database engine function for aggregate strings from group by sentence
        """
        if self.___has_test_database_environment():
            return func.group_concat(column_criteria, separator)
        else:
            return func.string_agg(column_criteria, separator)
