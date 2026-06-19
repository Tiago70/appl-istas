from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AddressCreate(BaseModel):
    latitude: float
    longitude: float


class NoteCreate(BaseModel):
    title: str
    content: str
    timestamp: int
    priority: Priority

    address: Optional[AddressCreate] = None

class ChecklistCreate(BaseModel):
    title: str
    priority: Priority
    isCompleted: bool