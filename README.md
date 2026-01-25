# Pupil Study API

FastAPI backend for the POCUS Medical Study application.

## Setup

1. Install MySQL server if not already installed

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Update the `.env` file with your MySQL database credentials:
```
DATABASE_URL=mysql://user:password@localhost:3306/pupil_study
CORS_ORIGINS=http://localhost:3000
```

5. Create the MySQL database:
```sql
CREATE DATABASE pupil_study CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Run the API

### Development mode with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Sessions
- `POST /api/sessions` - Create a new session
- `GET /api/sessions/{session_id}` - Get session details
- `PUT /api/sessions/{session_id}` - Update session
- `GET /api/sessions/{session_id}/responses` - Get all responses for a session

### Responses
- `POST /api/trial-responses` - Save trial response
- `POST /api/feedback-responses` - Save feedback response

## Database Schema

### Sessions Table
- session_id (String, unique)
- participant_id (String)
- start_time (BigInteger)
- completed (Boolean)
- diagnosis_response (JSON)
- sam_response (JSON)
- nasa_tlx_response (JSON)

### Trial Responses Table
- session_id (FK)
- trial_id
- question_id
- selected_option_index
- stimulus_start_time
- answer_time
- next_clicked_time
- cross_start_time
- cross_end_time
- response_time

### Feedback Responses Table
- session_id (FK)
- trial_id
- question_id
- mental_effort
- confidence
- familiarity

## Development

The API uses:
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **MySQL** - Database

## Testing

You can test the API using:
- The Swagger UI at `/docs`
- curl commands
- Python requests library
- Postman or similar tools
