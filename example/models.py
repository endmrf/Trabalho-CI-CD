import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSON
from src.infra.config import Base

class Example(Base):
    """Examples Entity"""

    __tablename__ = "examples"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    company_id = Column(String(36), nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    datetime_created = Column(
        DateTime, default=datetime.datetime.utcnow(), nullable=True
    )
    datetime_updated = Column(
        DateTime, default=datetime.datetime.utcnow(), nullable=True
    )

    def __repr__(self):
        return f"Example [name={self.name}]"

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.company_id == other.company_id
        ):
            return True
        return False
