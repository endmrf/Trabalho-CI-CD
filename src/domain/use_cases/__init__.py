"""Namespace de casos de uso."""
from .base_use_case import BaseUseCaseInterface
from .example_interfaces import (
    CreateExampleUseCaseInterface,
    ListExamplesUseCaseInterface,
    GetExampleUseCaseInterface,
    UpdateExampleUseCaseInterface,
    DeleteExampleUseCaseInterface,
)
from .user_interfaces import (
    CreateUserUseCaseInterface,
    ListUsersUseCaseInterface,
    GetUserUseCaseInterface,
    UpdateUserUseCaseInterface,
    DeleteUserUseCaseInterface,
)
