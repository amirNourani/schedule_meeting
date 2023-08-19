from pydantic import BaseModel
from datetime import time


class MeetingBase(BaseModel):
    start_time: time 
    end_time: time
    seats_required: int 

class MeetingCreate(MeetingBase):
    pass

class MeetingUpdate(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    seats_required: int | None =None

class Meeting(MeetingBase):
    id: int
    class Config:
        orm_mode = True