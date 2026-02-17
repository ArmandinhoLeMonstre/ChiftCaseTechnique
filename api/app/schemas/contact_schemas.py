from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ContactsResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    website: Optional[str] = None
    write_date: datetime
    active: bool

    model_config = ConfigDict(from_attributes=True)