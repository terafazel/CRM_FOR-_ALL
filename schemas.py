from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models import Status, ActivityType, ActivityOutcome, Priority

class AccountBase(BaseModel):
    name: str
    industry: Optional[str] = None
    location: Optional[str] = None
    status: Status = Status.NEW
    notes: Optional[str] = None

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_activity_at: Optional[datetime]

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    account_id: int
    name: str
    role_title: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    seniority: Optional[str] = None
    status: Status = Status.NEW

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    account_id: int
    contact_id: Optional[int] = None
    type: ActivityType = ActivityType.CALL
    outcome: ActivityOutcome
    remarks: str
    follow_up_at: Optional[datetime] = None
    priority: Priority = Priority.MEDIUM

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True