from fastapi import (FastAPI, 
                     Depends, 
                     status, 
                     HTTPException,
                    )
from . import schemas, models, crud
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CONFERENCE_ROOM_TOTAL_SEATS = 20


@app.get('/meetings', response_model=list[schemas.Meeting], status_code= status.HTTP_200_OK)
def get_meetings(db: Session = Depends(get_db)):
    all_meetings = crud.get_meetings(db= db)
    return all_meetings

@app.get('/meetings/{id}', response_model=schemas.Meeting, status_code= status.HTTP_200_OK)
def show_meeting(id: int, db: Session = Depends(get_db)):
    meeting = crud.get_meeting(db= db, id= id)
    if not meeting:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='Meeting not found')
    return meeting 

@app.delete('/meetings/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delelte_meeting(id: int, db: Session = Depends(get_db)):
    meeting = crud.get_meeting(db= db, id= id)
    if not meeting:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Metting not found")
    return crud.delete_meeting(db= db, id= id) 

@app.put('/meetings/{id}', status_code= status.HTTP_202_ACCEPTED, response_model=schemas.Meeting)
def update_meeting(id: int, updated_meeting:schemas.MeetingUpdate, db: Session = Depends(get_db)):
    meeting = crud.get_meeting(db= db, id= id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Meeting not found')
    return crud.update_meeting(db= db, id= id, updated_meeting= updated_meeting)

# some scenarios when a conflict can occur 
def possible_conflicts(existing_meeting: list[schemas.Meeting], new_meeting: schemas.Meeting):
    for model in existing_meeting:
        if new_meeting.start_time > model.start_time and new_meeting.start_time < model.end_time:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Another meeting is scheduled for this time and your meeting have conflicts with that meeting")
        elif new_meeting.start_time < model.start_time and new_meeting.end_time > model.start_time:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "Another meeting is scheduled for this time and your meeting have conflicts with that meeting")

@app.post('/schedule_meeting', response_model= schemas.Meeting, status_code= status.HTTP_201_CREATED)
def create_meeting(new_meeting: schemas.MeetingCreate, db: Session= Depends(get_db)):
    if new_meeting.seats_required <= CONFERENCE_ROOM_TOTAL_SEATS:
        existing_meeting = crud.get_meetings(db= db)
        possible_conflicts(existing_meeting= existing_meeting, new_meeting= new_meeting)
        new_meeting = crud.create_meeting(db= db, new_meeting= new_meeting)
        return new_meeting
    else:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= f"required number of seats for your meeting sould be less than or equal to the number of conferece room total seats which is {CONFERENCE_ROOM_TOTAL_SEATS}")

