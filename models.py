from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class Status(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    NURTURING = "NURTURING"
    CONVERTED = "CONVERTED"
    DROPPED = "DROPPED"

class ActivityType(str, enum.Enum):
    CALL = "CALL"
    EMAIL = "EMAIL"
    MEETING = "MEETING"
    OTHER = "OTHER"

class ActivityOutcome(str, enum.Enum):
    REACHED = "REACHED"
    NOT_REACHABLE = "NOT_REACHABLE"
    VOICEMAIL = "VOICEMAIL"
    CALL_BACK_LATER = "CALL_BACK_LATER"
    WRONG_NUMBER = "WRONG_NUMBER"
    INTERESTED = "INTERESTED"
    NOT_INTERESTED = "NOT_INTERESTED"

class Priority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String)
    location = Column(String)
    status = Column(Enum(Status), default=Status.NEW)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity_at = Column(DateTime)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    name = Column(String, nullable=False)
    role_title = Column(String)
    department = Column(String)
    email = Column(String)
    phone = Column(String)
    seniority = Column(String)
    status = Column(Enum(Status), default=Status.NEW)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    type = Column(Enum(ActivityType), default=ActivityType.CALL)
    outcome = Column(Enum(ActivityOutcome))
    remarks = Column(Text, nullable=False)
    follow_up_at = Column(DateTime)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    created_at = Column(DateTime, default=datetime.utcnow)