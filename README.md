# Flask Todo API

A simple Flask-based REST API for managing a to-do list. This API allows you to create, read, update, and delete tasks with proper error handling.

## Features

- **Add new tasks** with descriptions
- **Retrieve all tasks** or get a specific task by ID
- **Update task status** (completed/not completed)
- **Delete tasks**
- **Comprehensive error handling** for invalid requests
- **In-memory storage** for simplicity
- **Full test coverage** with pytest

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Add a New Task
- **URL:** `POST /tasks`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "description": "Task description"
  }
  ```
- **Success Response:** `201 Created`
  ```json
  {
    "id": "uuid-string",
    "description": "Task description",
    "completed": false,
    "created_at": "2024-01-01T12:00:00.000000"
  }
  ```
- **Error Responses:**
  - `400 Bad Request` - Missing or invalid description
  - `400 Bad Request` - Invalid JSON format

### 2. Get All Tasks
- **URL:** `GET /tasks`
- **Success Response:** `200 OK`
  ```json
  {
    "tasks": [
      {
        "id": "uuid-string",
        "description": "Task description",
        "completed": false,
        "created_at": "2024-01-01T12:00:00.000000"
      }
    ]
  }
  ```

### 3. Get Task by ID
- **URL:** `GET /tasks/<task_id>`
- **Success Response:** `200 OK`
  ```json
  {
    "id": "uuid-string",
    "description": "Task description",
    "completed": false,
    "created_at": "2024-01-01T12:00:00.000000"
  }
  ```
- **Error Response:**
  - `404 Not Found` - Task not found

### 4. Update Task Status
- **URL:** `PUT /tasks/<task_id>`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "completed": true
  }
  ```
- **Success Response:** `200 OK`
  ```json
  {
    "id": "uuid-string",
    "description": "Task description",
    "completed": true,
    "created_at": "2024-01-01T12:00:00.000000",
    "updated_at": "2024-01-01T12:30:00.000000"
  }
  ```
- **Error Responses:**
  - `404 Not Found` - Task not found
  - `400 Bad Request` - Missing or invalid completed field

### 5. Delete Task
- **URL:** `DELETE /tasks/<task_id>`
- **Success Response:** `200 OK`
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```
- **Error Response:**
  - `404 Not Found` - Task not found

## Error Handling

The API includes comprehensive error handling for:
- Invalid JSON format
- Missing required fields
- Invalid data types
- Non-existent resources
- Unsupported HTTP methods
- Invalid endpoints

All error responses follow this format:
```json
{
  "error": "Error description"
}
```

## Testing

Run the test suite using pytest:

```bash
pytest test_app.py -v
```

The test suite includes:
- Unit tests for all endpoints
- Error handling tests
- Integration tests
- Edge case testing

## Task Data Structure

Each task contains the following fields:
- `id`: Unique identifier (UUID string)
- `description`: Task description (string)
- `completed`: Task completion status (boolean)
- `created_at`: Task creation timestamp (ISO format)
- `updated_at`: Task update timestamp (ISO format, added when status is updated)

## Example Usage

### Using curl:

1. **Add a task:**
   ```bash
   curl -X POST http://localhost:5000/tasks \
     -H "Content-Type: application/json" \
     -d '{"description": "Buy groceries"}'
   ```

2. **Get all tasks:**
   ```bash
   curl http://localhost:5000/tasks
   ```

3. **Update task status:**
   ```bash
   curl -X PUT http://localhost:5000/tasks/<task_id> \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
   ```

4. **Delete a task:**
   ```bash
   curl -X DELETE http://localhost:5000/tasks/<task_id>
   ```

### Using Python requests:

```python
import requests
import json

base_url = "http://localhost:5000"

# Add a task
response = requests.post(f"{base_url}/tasks", 
                        json={"description": "Learn Flask"})
task = response.json()
task_id = task["id"]

# Get all tasks
response = requests.get(f"{base_url}/tasks")
print(response.json())

# Update task status
response = requests.put(f"{base_url}/tasks/{task_id}", 
                       json={"completed": True})
print(response.json())

# Delete task
response = requests.delete(f"{base_url}/tasks/{task_id}")
print(response.json())
```

## Development Notes

- The application uses in-memory storage, so data will be lost when the server restarts
- For production use, consider implementing persistent storage (database)
- The API uses UUID4 for task IDs to ensure uniqueness
- All timestamps are in ISO format for consistency
- The application runs in debug mode by default for development