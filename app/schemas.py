from pydantic import BaseModel
from typing import Optional, List, Any


class TrialResponseSchema(BaseModel):
    trial_id: int
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


class SessionResponse(BaseModel):
    id: int
    session_id: str
    participant_id: str
    start_time: int
    completed: bool
    trial_responses: List[TrialResponseSchema] = []

    class Config:
        from_attributes = True


class TrialResponseCreate(BaseModel):
    session_id: str
    trial_id: int
    selected_option: str
    stimulus_start_time: int
    answer_time: int
    next_clicked_time: int
    cross_start_time: int
    cross_end_time: int
    response_time: int
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
