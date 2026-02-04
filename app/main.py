from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session as DBSession
from typing import List, Dict, Any
from pydantic import BaseModel
import logging

from app.config import settings
from app.database import get_db, engine, Base
from app.models import StudySession, TrialResponse, FeedbackResponse, SAMResponse, TLXResponse, EventLog, EyeTrackingData, Trial
from app.schemas import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    TrialResponseCreate,
    TrialResponseSchema,
    FeedbackResponseCreate,
    FeedbackResponseSchema,
    SAMResponseCreate,
    SAMResponseSchema,
    TLXResponseCreate,
    TLXResponseSchema,
    EventLogCreate,
    EventLogSchema,
    EyeTrackingDataCreate,
    EyeTrackingDataSchema,
)


class HealthResponse(BaseModel):
    status: str
    message: str

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pupil Study API",
    description="Backend API for POCUS Medical Study",
    version="1.0.0",
)

# Debug middleware
@app.middleware("http")
async def debug_cors(request: Request, call_next):
    origin = request.headers.get("origin")
    print(f"Incoming request: {request.method} {request.url.path}")
    print(f"Origin: {origin}")
    response = await call_next(request)
    return response

# CORS middleware
# Expanded origins to include IP addresses and 127.0.0.1
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://192.168.100.9:3000",
    "http://0.0.0.0:3000", 
    "https://pupil-study.vercel.app",
]
# Add configured origins
origins.extend(settings.cors_origins_list)
# Remove duplicates
origins = list(set(origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    return {"status": "ok", "message": "Pupil Study API is running"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok", "message": "API is healthy"}


@app.post("/api/sessions", response_model=SessionResponse)
async def create_session(session: SessionCreate, db: DBSession = Depends(get_db)):
    """Create a new study session"""
    # Check if session already exists
    existing_session = db.query(StudySession).filter(StudySession.session_id == session.session_id).first()
    if existing_session:
        return existing_session
    
    db_session = StudySession(
        session_id=session.session_id,
        participant_id=session.participant_id,
        start_time=session.start_time,
        completed=session.completed,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, db: DBSession = Depends(get_db)):
    """Get a session by ID"""
    session = db.query(StudySession).filter(StudySession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.put("/api/sessions/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str, session_update: SessionUpdate, db: DBSession = Depends(get_db)
):
    """Update a session"""
    session = db.query(StudySession).filter(StudySession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session_update.completed is not None:
        session.completed = session_update.completed
    
    if session_update.end_time is not None:
        session.end_time = session_update.end_time
    
    db.commit()
    db.refresh(session)
    return session


@app.post("/api/trial-responses", response_model=TrialResponseSchema)
async def create_trial_response(
    response: TrialResponseCreate, db: DBSession = Depends(get_db)
):
    """Save a trial response"""
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.session_id == response.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_response = TrialResponse(
        session_id=response.session_id,
        participant_id=response.participant_id,
        trial_id=response.trial_id,
        question_number=response.question_number,
        selected_option=response.selected_option,
        stimulus_start_time=response.stimulus_start_time,
        answer_time=response.answer_time,
        next_clicked_time=response.next_clicked_time,
        cross_start_time=response.cross_start_time,
        cross_end_time=response.cross_end_time,
        response_time=response.response_time,
        timestamp=response.timestamp,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


@app.post("/api/feedback-responses", response_model=FeedbackResponseSchema)
async def create_feedback_response(
    response: FeedbackResponseCreate, db: DBSession = Depends(get_db)
):
    """Save a feedback response"""
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.session_id == response.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_response = FeedbackResponse(
        session_id=response.session_id,
        participant_id=response.participant_id,
        trial_id=response.trial_id,
        question_id=response.question_id,
        mental_effort=response.mental_effort,
        confidence=response.confidence,
        familiarity=response.familiarity,
        timestamp=response.timestamp,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


@app.post("/api/sam-responses", response_model=SAMResponseSchema)
async def create_sam_response(
    response: SAMResponseCreate, db: DBSession = Depends(get_db)
):
    """Save a SAM response"""
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.session_id == response.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_response = SAMResponse(
        session_id=response.session_id,
        participant_id=response.participant_id,
        pleasure=response.pleasure,
        arousal=response.arousal,
        dominance=response.dominance,
        timestamp=response.timestamp,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


@app.post("/api/tlx-responses", response_model=TLXResponseSchema)
async def create_tlx_response(
    response: TLXResponseCreate, db: DBSession = Depends(get_db)
):
    """Save a NASA-TLX response"""
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.session_id == response.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_response = TLXResponse(
        session_id=response.session_id,
        participant_id=response.participant_id,
        mental_demand=response.mental_demand,
        physical_demand=response.physical_demand,
        temporal_demand=response.temporal_demand,
        performance=response.performance,
        effort=response.effort,
        frustration=response.frustration,
        timestamp=response.timestamp,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


@app.post("/api/event-logs", response_model=EventLogSchema)
async def create_event_log(
    event: EventLogCreate, db: DBSession = Depends(get_db)
):
    """Save an event log"""
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.session_id == event.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_event = EventLog(
        session_id=event.session_id,
        event_type=event.event_type,
        event_data=event.event_data,
        timestamp=event.timestamp,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.post("/api/eye-tracking", response_model=EyeTrackingDataSchema)
async def create_eye_tracking_data(
    data: EyeTrackingDataCreate, db: DBSession = Depends(get_db)
):
    """Save eye tracking data"""
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.session_id == data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_data = EyeTrackingData(
        session_id=data.session_id,
        trial_id=data.trial_id,
        timestamp=data.timestamp,
        gaze_x=data.gaze_x,
        gaze_y=data.gaze_y,
        pupil_diameter=data.pupil_diameter,
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


@app.get("/api/sessions/{session_id}/responses")
async def get_session_responses(session_id: str, db: DBSession = Depends(get_db)):
    """Get all responses for a session"""
    session = db.query(StudySession).filter(StudySession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    trial_responses = db.query(TrialResponse).filter(
        TrialResponse.session_id == session_id
    ).all()
    
    event_logs = db.query(EventLog).filter(
        EventLog.session_id == session_id
    ).all()
    
    return {
        "session": session,
        "trial_responses": trial_responses,
        "event_logs": event_logs,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
