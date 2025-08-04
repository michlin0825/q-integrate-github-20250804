import pytest
import json
from app import app, tasks

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def clear_tasks():
    """Clear tasks before each test"""
    tasks.clear()
    yield
    tasks.clear()

class TestAddTask:
    """Test cases for adding tasks"""
    
    def test_add_task_success(self, client, clear_tasks):
        """Test successful task creation"""
        response = client.post('/tasks', 
                             data=json.dumps({'description': 'Test task'}),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert data['description'] == 'Test task'
        assert data['completed'] == False
        assert 'created_at' in data
    
    def test_add_task_missing_description(self, client, clear_tasks):
        """Test adding task without description"""
        response = client.post('/tasks', 
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Description is required' in data['error']
    
    def test_add_task_empty_description(self, client, clear_tasks):
        """Test adding task with empty description"""
        response = client.post('/tasks', 
                             data=json.dumps({'description': ''}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'non-empty string' in data['error']
    
    def test_add_task_invalid_json(self, client, clear_tasks):
        """Test adding task with invalid JSON"""
        response = client.post('/tasks', 
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_task_no_body(self, client, clear_tasks):
        """Test adding task with no request body"""
        response = client.post('/tasks', content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

class TestGetAllTasks:
    """Test cases for retrieving all tasks"""
    
    def test_get_all_tasks_empty(self, client, clear_tasks):
        """Test getting all tasks when list is empty"""
        response = client.get('/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tasks' in data
        assert data['tasks'] == []
    
    def test_get_all_tasks_with_data(self, client, clear_tasks):
        """Test getting all tasks with existing data"""
        # Add a task first
        client.post('/tasks', 
                   data=json.dumps({'description': 'Test task 1'}),
                   content_type='application/json')
        client.post('/tasks', 
                   data=json.dumps({'description': 'Test task 2'}),
                   content_type='application/json')
        
        response = client.get('/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tasks' in data
        assert len(data['tasks']) == 2
        assert data['tasks'][0]['description'] == 'Test task 1'
        assert data['tasks'][1]['description'] == 'Test task 2'

class TestUpdateTaskStatus:
    """Test cases for updating task status"""
    
    def test_update_task_status_success(self, client, clear_tasks):
        """Test successful task status update"""
        # Add a task first
        response = client.post('/tasks', 
                             data=json.dumps({'description': 'Test task'}),
                             content_type='application/json')
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        # Update task status
        response = client.put(f'/tasks/{task_id}', 
                            data=json.dumps({'completed': True}),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['completed'] == True
        assert 'updated_at' in data
    
    def test_update_task_status_not_found(self, client, clear_tasks):
        """Test updating non-existent task"""
        response = client.put('/tasks/nonexistent-id', 
                            data=json.dumps({'completed': True}),
                            content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Task not found' in data['error']
    
    def test_update_task_status_missing_completed(self, client, clear_tasks):
        """Test updating task without completed field"""
        # Add a task first
        response = client.post('/tasks', 
                             data=json.dumps({'description': 'Test task'}),
                             content_type='application/json')
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        # Update without completed field
        response = client.put(f'/tasks/{task_id}', 
                            data=json.dumps({}),
                            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'completed field is required' in data['error']
    
    def test_update_task_status_invalid_type(self, client, clear_tasks):
        """Test updating task with invalid completed type"""
        # Add a task first
        response = client.post('/tasks', 
                             data=json.dumps({'description': 'Test task'}),
                             content_type='application/json')
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        # Update with invalid type
        response = client.put(f'/tasks/{task_id}', 
                            data=json.dumps({'completed': 'invalid'}),
                            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'must be a boolean' in data['error']

class TestDeleteTask:
    """Test cases for deleting tasks"""
    
    def test_delete_task_success(self, client, clear_tasks):
        """Test successful task deletion"""
        # Add a task first
        response = client.post('/tasks', 
                             data=json.dumps({'description': 'Test task'}),
                             content_type='application/json')
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        # Delete the task
        response = client.delete(f'/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'deleted successfully' in data['message']
        
        # Verify task is deleted
        response = client.get('/tasks')
        data = json.loads(response.data)
        assert len(data['tasks']) == 0
    
    def test_delete_task_not_found(self, client, clear_tasks):
        """Test deleting non-existent task"""
        response = client.delete('/tasks/nonexistent-id')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Task not found' in data['error']

class TestGetTaskById:
    """Test cases for getting a specific task by ID"""
    
    def test_get_task_by_id_success(self, client, clear_tasks):
        """Test successful retrieval of task by ID"""
        # Add a task first
        response = client.post('/tasks', 
                             data=json.dumps({'description': 'Test task'}),
                             content_type='application/json')
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        # Get the task by ID
        response = client.get(f'/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['description'] == 'Test task'
        assert data['completed'] == False
    
    def test_get_task_by_id_not_found(self, client, clear_tasks):
        """Test getting non-existent task by ID"""
        response = client.get('/tasks/nonexistent-id')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Task not found' in data['error']

class TestErrorHandlers:
    """Test cases for error handlers"""
    
    def test_404_error_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-endpoint')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Endpoint not found' in data['error']
    
    def test_405_error_handler(self, client):
        """Test 405 error handler"""
        response = client.patch('/tasks')  # PATCH method not allowed
        
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Method not allowed' in data['error']

class TestIntegration:
    """Integration test cases"""
    
    def test_full_task_lifecycle(self, client, clear_tasks):
        """Test complete task lifecycle: create, read, update, delete"""
        # Create a task
        response = client.post('/tasks', 
                             data=json.dumps({'description': 'Integration test task'}),
                             content_type='application/json')
        assert response.status_code == 201
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        # Read all tasks
        response = client.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 1
        
        # Read specific task
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['completed'] == False
        
        # Update task status
        response = client.put(f'/tasks/{task_id}', 
                            data=json.dumps({'completed': True}),
                            content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['completed'] == True
        
        # Delete task
        response = client.delete(f'/tasks/{task_id}')
        assert response.status_code == 200
        
        # Verify task is deleted
        response = client.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 0