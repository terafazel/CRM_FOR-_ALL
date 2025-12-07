from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import models, schemas, database
from typing import List, Optional
from datetime import datetime, date, timedelta
import pandas as pd
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD for Accounts
@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = db.query(models.Account).offset(skip).limit(limit).all()
    return accounts

@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.put("/accounts/{account_id}", response_model=schemas.Account)
def update_account(account_id: int, account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in account.dict().items():
        setattr(db_account, key, value)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.delete("/accounts/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(db_account)
    db.commit()
    return {"message": "Account deleted"}

# CRUD for Contacts
@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).offset(skip).limit(limit).all()
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted"}

# CRUD for Activities
@app.post("/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    # Update last_activity_at for account
    db_account = db.query(models.Account).filter(models.Account.id == activity.account_id).first()
    if db_account:
        db_account.last_activity_at = datetime.utcnow()
        db.commit()
    return db_activity

@app.get("/activities/", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    activities = db.query(models.Activity).offset(skip).limit(limit).all()
    return activities

@app.get("/activities/{activity_id}", response_model=schemas.Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

@app.put("/activities/{activity_id}", response_model=schemas.Activity)
def update_activity(activity_id: int, activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    for key, value in activity.dict().items():
        setattr(db_activity, key, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(db_activity)
    db.commit()
    return {"message": "Activity deleted"}

# Follow-ups
@app.get("/followups/", response_model=List[schemas.Contact])
def get_followups(db: Session = Depends(get_db)):
    today = date.today()
    contacts = db.query(models.Contact).join(models.Activity).filter(
        models.Activity.follow_up_at <= datetime.combine(today, datetime.max.time()),
        models.Contact.status.notin_([models.Status.CONVERTED, models.Status.DROPPED])
    ).distinct().all()
    return contacts

# Search accounts
@app.get("/accounts/search/", response_model=List[schemas.Account])
def search_accounts(q: str, db: Session = Depends(get_db)):
    accounts = db.query(models.Account).filter(models.Account.name.ilike(f"%{q}%")).all()
    return accounts

# Search contacts
@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts(q: str, db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).filter(models.Contact.name.ilike(f"%{q}%")).all()
    return contacts

# Filter accounts
@app.get("/accounts/filter/", response_model=List[schemas.Account])
def filter_accounts(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Account)
    if status:
        query = query.filter(models.Account.status == status)
    return query.all()

# Filter contacts
@app.get("/contacts/filter/", response_model=List[schemas.Contact])
def filter_contacts(status: Optional[str] = None, role: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Contact)
    if status:
        query = query.filter(models.Contact.status == status)
    if role:
        query = query.filter(models.Contact.role_title.ilike(f"%{role}%"))
    return query.all()

# Dashboard
@app.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    account_counts = db.query(models.Account.status, db.func.count(models.Account.id)).group_by(models.Account.status).all()
    contact_counts = db.query(models.Contact.status, db.func.count(models.Contact.id)).group_by(models.Contact.status).all()
    last_week = datetime.utcnow() - timedelta(days=7)
    activity_count = db.query(db.func.count(models.Activity.id)).filter(models.Activity.created_at >= last_week).scalar()
    return {
        "accounts": {status.value if hasattr(status, 'value') else str(status): count for status, count in account_counts},
        "contacts": {status.value if hasattr(status, 'value') else str(status): count for status, count in contact_counts},
        "activities_last_7_days": activity_count
    }

# Import accounts
@app.post("/import/accounts/")
def import_accounts(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    for _, row in df.iterrows():
        account = models.Account(
            name=row['name'],
            industry=row.get('industry'),
            location=row.get('location'),
            status=getattr(models.Status, row.get('status', 'NEW').upper(), models.Status.NEW),
            notes=row.get('notes')
        )
        db.add(account)
    db.commit()
    return {"message": "Accounts imported"}

# Import contacts
@app.post("/import/contacts/")
def import_contacts(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    for _, row in df.iterrows():
        contact = models.Contact(
            account_id=row['account_id'],
            name=row['name'],
            role_title=row.get('role_title'),
            department=row.get('department'),
            email=row.get('email'),
            phone=row.get('phone'),
            seniority=row.get('seniority'),
            status=getattr(models.Status, row.get('status', 'NEW').upper(), models.Status.NEW)
        )
        db.add(contact)
    db.commit()
    return {"message": "Contacts imported"}

# Export accounts
@app.get("/export/accounts/")
def export_accounts(db: Session = Depends(get_db)):
    accounts = db.query(models.Account).all()
    df = pd.DataFrame([{
        'id': a.id,
        'name': a.name,
        'industry': a.industry,
        'location': a.location,
        'status': a.status.value,
        'notes': a.notes,
        'created_at': a.created_at,
        'updated_at': a.updated_at,
        'last_activity_at': a.last_activity_at
    } for a in accounts])
    df.to_csv('accounts_export.csv', index=False)
    return FileResponse('accounts_export.csv', media_type='text/csv', filename='accounts.csv')

# Export contacts
@app.get("/export/contacts/")
def export_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    df = pd.DataFrame([{
        'id': c.id,
        'account_id': c.account_id,
        'name': c.name,
        'role_title': c.role_title,
        'department': c.department,
        'email': c.email,
        'phone': c.phone,
        'seniority': c.seniority,
        'status': c.status.value,
        'created_at': c.created_at,
        'updated_at': c.updated_at
    } for c in contacts])
    df.to_csv('contacts_export.csv', index=False)
    return FileResponse('contacts_export.csv', media_type='text/csv', filename='contacts.csv')

# Export activities
@app.get("/export/activities/")
def export_activities(db: Session = Depends(get_db)):
    activities = db.query(models.Activity).all()
    df = pd.DataFrame([{
        'id': a.id,
        'account_id': a.account_id,
        'contact_id': a.contact_id,
        'type': a.type.value,
        'outcome': a.outcome.value,
        'remarks': a.remarks,
        'follow_up_at': a.follow_up_at,
        'priority': a.priority.value,
        'created_at': a.created_at
    } for a in activities])
    df.to_csv('activities_export.csv', index=False)
    return FileResponse('activities_export.csv', media_type='text/csv', filename='activities.csv')
