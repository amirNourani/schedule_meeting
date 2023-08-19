from sqlalchemy.orm import Session
from . import models, schemas


def get_meetings(db: Session):
    return db.query(models.Meeting).all()

def get_meeting(db: Session, id: int):
    meeting_item = db.query(models.Meeting).filter(models.Meeting.id == id).first()
    return meeting_item

def create_meeting(db: Session, new_meeting: schemas.MeetingCreate):
    db_meeting = models.Meeting(**new_meeting.dict())
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def delete_meeting(db: Session, id: int):
    db.query(models.Meeting).filter(models.Meeting.id == id).delete(synchronize_session= False)
    db.commit()
    return {}

def update_meeting(db: Session, id: int, updated_meeting: schemas.MeetingUpdate):
    meeting_db = get_meeting(db= db, id= id)
    meeting_data = updated_meeting.dict(exclude_unset=True)
    for key, value in meeting_data.items():
            setattr(meeting_db, key, value)
    db.add(meeting_db)
    db.commit()
    db.refresh(meeting_db)
    return meeting_db

