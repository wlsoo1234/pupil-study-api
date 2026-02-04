from pydantic import BaseModel
from typing import Optional, List, Any


class TrialResponseSchema(BaseModel):
    trial_id: int
    participant_id: str
    question_number: int
    selected_option: str
    stimulus_start_time: int
    answer_time: int
    next_clicked_time: int
    cross_start_time: int
    cross_end_time: int
    response_time: int
    timestamp: int

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    session_id: str
    participant_id: str
    start_time: int
    completed: bool = False


class SessionUpdate(BaseModel):
    completed: Optional[bool] = None
    end_time: Optional[int] = None


class SessionResponse(BaseModel):
    id: int
    session_id: str
    participant_id: str
    start_time: int
    end_time: Optional[int] = None
    completed: bool
    trial_responses: List[TrialResponseSchema] = []

    class Config:
        from_attributes = True


class TrialResponseCreate(BaseModel):
    session_id: str
    participant_id: str
    trial_id: int
    question_number: int
    selected_option: str
    stimulus_start_time: int
    answer_time: int
    next_clicked_time: int
    cross_start_time: int
    cross_end_time: int
    response_time: int
    timestamp: int


class FeedbackResponseSchema(BaseModel):
    id: int
    session_id: str
    participant_id: str
    trial_id: int
    question_id: int
    mental_effort: int
    confidence: int
    familiarity: int
    timestamp: int

    class Config:
        from_attributes = True


class FeedbackResponseCreate(BaseModel):
    session_id: str
    participant_id: str
    trial_id: int
    question_id: int
    mental_effort: int
    confidence: int
    familiarity: int
    timestamp: int


class SAMResponseSchema(BaseModel):
    id: int
    session_id: str
    participant_id: str
    pleasure: int
    arousal: int
    dominance: int
    timestamp: int

    class Config:
        from_attributes = True


class SAMResponseCreate(BaseModel):
    session_id: str
    participant_id: str
    pleasure: int
    arousal: int
    dominance: int
    timestamp: int


class TLXResponseSchema(BaseModel):
    id: int
    session_id: str
    participant_id: str
    mental_demand: int
    physical_demand: int
    temporal_demand: int
    performance: int
    effort: int
    frustration: int
    timestamp: int

    class Config:
        from_attributes = True


class TLXResponseCreate(BaseModel):
    session_id: str
    participant_id: str
    mental_demand: int
    physical_demand: int
    temporal_demand: int
    performance: int
    effort: int
    frustration: int
    timestamp: int


class EventLogCreate(BaseModel):
    session_id: str
    event_type: str
    event_data: Optional[dict] = None
    timestamp: int


class EventLogSchema(BaseModel):
    id: int
    session_id: str
    event_type: str
    event_data: Optional[dict] = None
    timestamp: int

    class Config:
        from_attributes = True


class EyeTrackingDataCreate(BaseModel):
    session_id: str
    trial_id: int
    timestamp: int
    gaze_x: Optional[float] = None
    gaze_y: Optional[float] = None
    pupil_diameter: Optional[float] = None


class EyeTrackingDataSchema(BaseModel):
    id: int
    session_id: str
    trial_id: int
    timestamp: int
    gaze_x: Optional[float] = None
    gaze_y: Optional[float] = None
    pupil_diameter: Optional[float] = None

    class Config:
        from_attributes = True


class TrialCreate(BaseModel):
    trial_id: int
    stimulus_url: str
    question: str
    correct_answer: Optional[str] = None


class TrialSchema(BaseModel):
    id: int
    trial_id: int
    stimulus_url: str
    question: str
    correct_answer: Optional[str] = None

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    message: str
