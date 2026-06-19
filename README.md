# ---
# title: TaskFlow API
# description: Reference implementation of a FastAPI task management API
# ---

# TaskFlow API

A production-ready FastAPI application demonstrating best practices for building RESTful APIs. This project is structured as a reference implementation showcasing modern Python web development patterns.

## 📋 Project Overview

**TaskFlow API** is a task management REST API that implements:
- Full CRUD operations
- Data validation using Pydantic
- SQLite database integration
- Proper layered architecture (Routes → Services → Database)
- Professional error handling
- API documentation
- Type hints throughout

## 🏗️ Architecture

The project follows a clean, layered architecture pattern:

```
app/
├── main.py              # FastAPI application entry point
├── core/
│   ├── config.py        # Configuration and settings management
│   └── __init__.py
├── db/
│   ├── database.py      # Database connection and operations
│   └── __init__.py
├── models/
│   ├── task.py          # Task model (ORM-like representation)
│   └── __init__.py
├── schemas/
│   ├── task.py          # Pydantic models for validation
│   └── __init__.py
├── routers/
│   ├── tasks.py         # API endpoint definitions
│   └── __init__.py
├── services/
│   ├── task_service.py  # Business logic layer
│   └── __init__.py
└── __init__.py
```

### Architecture Layers Explained

1. **Routes Layer** (`routers/`)
   - Handles HTTP requests/responses
   - Request validation via Pydantic schemas
   - Error handling and status codes
   - Example: `POST /tasks` receives TaskCreate schema

2. **Service Layer** (`services/`)
   - Contains business logic
   - Coordinates between routes and database
   - No direct HTTP concerns
   - Example: TaskService.create_task()

3. **Model Layer** (`models/`)
   - Represents database records
   - Converts between database rows and Python objects
   - Example: Task.from_db_row()

4. **Database Layer** (`db/`)
   - Direct database operations
   - Connection management
   - Raw SQL queries
   - Example: Database.add_task()

5. **Configuration Layer** (`core/`)
   - Settings management
   - Environment variables
   - Application constants

6. **Schema Layer** (`schemas/`)
   - Pydantic models for request/response validation
   - Type hints and field constraints
   - Example: TaskCreate, TaskResponse

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
cd /home/prath/projects/taskflow-api
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Tasks Management

#### GET `/tasks`
Retrieve all tasks with optional filtering and pagination.

**Parameters:**
- `status` (query): Filter by status (pending, in_progress, done)
- `priority` (query): Filter by priority (low, medium, high)
- `skip` (query): Number of tasks to skip (default: 0)
- `limit` (query): Max tasks to return (default: 10, max: 100)

**Example:**
```bash
curl "http://localhost:8000/tasks?status=pending&priority=high&limit=5"
```

#### GET `/tasks/{task_id}`
Retrieve a specific task by ID.

**Parameters:**
- `task_id` (path): Task ID
- `verbose` (query): Include debug information (default: false)

**Example:**
```bash
curl "http://localhost:8000/tasks/1?verbose=true"
```

#### POST `/tasks`
Create a new task.

**Request Body:**
```json
{
  "title": "Complete project",
  "description": "Finish the TaskFlow API",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2027-01-31T23:59:59",
  "tags": ["work", "important"]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the TaskFlow API",
    "priority": "high",
    "due_date": "2027-01-31T23:59:59"
  }'
```

#### PUT `/tasks/{task_id}`
Update an entire task.

#### PATCH `/tasks/{task_id}`
Partially update a task (only provided fields are updated).

#### DELETE `/tasks/{task_id}`
Delete a task.

#### GET `/tasks/stats`
Get task statistics grouped by status.

**Response:**
```json
{
  "total": 10,
  "pending": 3,
  "in_progress": 5,
  "done": 2
}
```

## Key Concepts

- **Layered Architecture:** Routes handle HTTP concerns; services contain business logic; database layer manages persistence.
- **Pydantic Validation:** Models in `app/schemas/task.py` enforce input validation and serialization.
- **Database Operations:** `app/db/database.py` provides connection management and parameterized SQL for CRUD.
- **Service Layer Pattern:** `app/services/task_service.py` coordinates data flow between routes and the database.
- **FastAPI Features:** Implemented in `app/main.py` and `app/routers/tasks.py` (dependencies, lifecycle, docs).

### Quick Start Files

- `app/main.py` — FastAPI application and lifecycle
- `app/routers/tasks.py` — HTTP endpoints
- `app/schemas/task.py` — Request/response models
- `app/services/task_service.py` — Business logic
- `app/models/task.py` — Data representation
- `app/db/database.py` — Database operations
- `app/core/config.py` — Configuration

## Common Maintenance Tasks

### Add a New Field to Tasks
1. Update `app/db/database.py` — modify CREATE TABLE and migrations
2. Update `app/models/task.py` — add to data representation
3. Update `app/schemas/task.py` — add to Pydantic models
4. Update `app/services/task_service.py` — handle new field

### Add a New Endpoint
1. Add method to `TaskService` in `app/services/task_service.py`
2. Add route in `app/routers/tasks.py`
3. Add/update schema in `app/schemas/task.py`

### Add Input Validation
1. Edit `app/schemas/task.py`
2. Add `Field` constraints and validators as needed

## 🧪 Testing the API

### Using curl
```bash
# Create a task
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "high", "due_date": "2027-01-31T23:59:59"}'

# Get all tasks
curl "http://localhost:8000/tasks"

# Get specific task
curl "http://localhost:8000/tasks/1"

# Update task
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'

# Delete task
curl -X DELETE "http://localhost:8000/tasks/1"
```

### Using Python
```python
import requests

BASE_URL = "http://localhost:8000"

# Create task
response = requests.post(
    f"{BASE_URL}/tasks",
    json={
        "title": "Learn FastAPI",
        "priority": "high",
        "due_date": "2027-01-31T23:59:59"
    }
)
print(response.json())

# Get all tasks
response = requests.get(f"{BASE_URL}/tasks")
print(response.json())
```

## Project Benefits

- Modularity: Each layer has a single responsibility
- Testability: Easy to test each layer independently
- Maintainability: Changes are localized to specific layers

## Configuration

Edit `.env` file to change settings:
```
APP_NAME=TaskFlow API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=app/db/sqlite3.db
```

## External References

- FastAPI Docs: https://fastapi.tiangolo.com/
- Pydantic Docs: https://docs.pydantic.dev/
- SQLite Docs: https://www.sqlite.org/docs.html

## License

Use this project according to your needs. No specific license is declared in this repository.
