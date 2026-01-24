from sqlalchemy import Column, Integer, String, Boolean, Float, JSON, BigInteger, ForeignKey, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    participant_id = Column(String(100), nullable=False, index=True)
    start_time = Column(BigInteger, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # Relationships
    trial_responses = relationship("TrialResponse", back_populates="session", cascade="all, delete-orphan")
    event_logs = relationship("EventLog", back_populates="session", cascade="all, delete-orphan")
    eye_tracking_data = relationship("EyeTrackingData", back_populates="session", cascade="all, delete-orphan")


class TrialResponse(Base):
    __tablename__ = "trial_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), ForeignKey("study_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    trial_id = Column(Integer, nullable=False, index=True)
    selected_option = Column(String(10), nullable=False)
    stimulus_start_time = Column(BigInteger, nullable=False)
    answer_time = Column(BigInteger, nullable=False)
    next_clicked_time = Column(BigInteger, nullable=False)
    cross_start_time = Column(BigInteger, nullable=False)
    cross_end_time = Column(BigInteger, nullable=False)
    response_time = Column(Integer, nullable=False)
    timestamp = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    session = relationship("StudySession", back_populates="trial_responses")


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), ForeignKey("study_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    event_data = Column(JSON, nullable=True)
    timestamp = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relationships
    session = relationship("StudySession", back_populates="event_logs")


class EyeTrackingData(Base):
    __tablename__ = "eye_tracking_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), ForeignKey("study_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    trial_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(BigInteger, nullable=False)
    gaze_x = Column(Float, nullable=True)
    gaze_y = Column(Float, nullable=True)
    pupil_diameter = Column(Float, nullable=True)
    
    # Relationships
    session = relationship("StudySession", back_populates="eye_tracking_data")


class Trial(Base):
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trial_id = Column(Integer, unique=True, nullable=False)
    stimulus_url = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    correct_answer = Column(String(10), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
