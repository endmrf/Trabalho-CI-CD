from typing import NamedTuple, Optional

class Example(NamedTuple):
    id: str
    name: str
    company_id: str
    created_by: str
    updated_by: str
    datetime_created: str
    datetime_updated: str
    description: Optional[str] = None
    