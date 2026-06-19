from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    BigInteger,
    ForeignKey,
    Enum as SqlEnum
)

from sqlalchemy.orm import relationship

from database import Base


class ChecklistPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    timestamp = Column(BigInteger, nullable=False)
    priority = Column(String)

    address_id = Column(
        Integer,
        ForeignKey("addresses.id"),
        nullable=True
    )

    address = relationship("Address")


class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)

    priority = Column(
        SqlEnum(ChecklistPriority),
        nullable=False
    )
    title = Column(String, nullable=False)
    is_completed = Column(Boolean, nullable=False)