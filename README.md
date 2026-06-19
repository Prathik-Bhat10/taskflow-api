# TaskFlow API - Complete Learning Project

A comprehensive, production-ready FastAPI application demonstrating best practices for building RESTful APIs. This project is structured to serve as an excellent learning resource for understanding modern Python web development patterns.

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

## 🎓 Learning Points

### 1. **Layered Architecture**
The project demonstrates the separation of concerns:
- Routes handle HTTP
- Services handle business logic
- Database layer handles data persistence

### 2. **Pydantic Validation**
See `app/schemas/task.py`:
- Field validation with constraints
- Custom validators using `@field_validator`
- Cross-field validation using `@model_validator`

### 3. **Database Operations**
See `app/db/database.py`:
- Connection management with context managers
- CRUD operations (Create, Read, Update, Delete)
- SQL parameterization to prevent injection

### 4. **Service Layer Pattern**
See `app/services/task_service.py`:
- Coordinates between routes and database
- Handles data transformation
- Centralizes business logic

### 5. **FastAPI Features**
See `app/main.py` and `app/routers/tasks.py`:
- Path parameters and query parameters
- Request/response models
- HTTP status codes
- Dependency injection
- Lifecycle events (startup/shutdown)

## 🔍 Code Study Guide

### Start Here (in order)
1. **`app/main.py`** - Understand the app structure and lifecycle
2. **`app/routers/tasks.py`** - See how routes are defined
3. **`app/schemas/task.py`** - Learn about Pydantic validation
4. **`app/services/task_service.py`** - Understand the service layer
5. **`app/models/task.py`** - See data representation
6. **`app/db/database.py`** - Learn about database operations
7. **`app/core/config.py`** - Understand configuration management

### Key Concepts

**Type Hints** - Used throughout for clarity and IDE support
```python
def add_task(self, title: str, description: Optional[str] = None) -> int:
    # Clear about what types are expected and returned
```

**Pydantic Models** - For validation and serialization
```python
class TaskCreate(BaseModel):
    title: TaskTitle  # Custom validated type
    priority: TaskPriority = TaskPriority.medium  # Default value
```

**Error Handling** - Proper HTTP exceptions
```python
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
```

**Database Connection** - Context manager pattern
```python
with Database("db.sqlite") as db:
    db.create_table()
    task_id = db.add_task(...)
```

## 📝 Common Tasks While Learning

### Add a New Field to Tasks
1. Update `app/db/database.py` - Add to CREATE TABLE
2. Update `app/models/task.py` - Add to Task class
3. Update `app/schemas/task.py` - Add to Pydantic models
4. Update `app/services/task_service.py` - Handle new field

### Add a New Endpoint
1. Add method to `TaskService` in `app/services/task_service.py`
2. Create route in `app/routers/tasks.py`
3. Add corresponding schema in `app/schemas/task.py`

### Add Input Validation
1. Edit `app/schemas/task.py`
2. Add constraints to fields: `Field(min_length=3, max_length=100)`
3. Add custom validators: `@field_validator`

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

## 📦 Project Structure Benefits

- **Modularity**: Each layer has a single responsibility
- **Testability**: Easy to test each layer independently
- **Maintainability**: Changes are localized to specific layers
- **Scalability**: Easy to add new features following the pattern
- **Clarity**: Clear separation makes code easy to understand

## 🔧 Configuration

Edit `.env` file to change settings:
```
APP_NAME=TaskFlow API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=app/db/sqlite3.db
```

## 📚 Further Learning

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **SQLite Docs**: https://www.sqlite.org/docs.html
- **REST API Best Practices**: https://restfulapi.net/

## 🤝 What This Project Teaches

1. ✅ How to structure a FastAPI application
2. ✅ Layered architecture pattern
3. ✅ Data validation with Pydantic
4. ✅ Database operations and management
5. ✅ RESTful API design
6. ✅ Error handling and HTTP status codes
7. ✅ Configuration management
8. ✅ Type hints and Python best practices
9. ✅ API documentation generation
10. ✅ Service layer pattern

## 📄 License

This project is created for educational purposes.
