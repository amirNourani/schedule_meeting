from sqlalchemy import Column, Integer, Time
from .database import Base



class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Time, index=True)
    end_time = Column(Time, index=True)
    seats_required = Column(Integer, index=True)

