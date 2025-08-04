from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import os
from config import config

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    return app

app = create_app()

# In-memory storage for tasks
tasks = []

def find_task_by_id(task_id):
    """Helper function to find a task by ID"""
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

def validate_task_data(data):
    """Helper function to validate task data"""
    if not data:
        return False, "Request body is required"
    
    if 'description' not in data:
        return False, "Description is required"
    
    if not isinstance(data['description'], str) or not data['description'].strip():
        return False, "Description must be a non-empty string"
    
    return True, None

@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task"""
    try:
        data = request.get_json()
        
        # Validate input data
        is_valid, error_message = validate_task_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Create new task
        new_task = {
            'id': str(uuid.uuid4()),
            'description': data['description'].strip(),
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        tasks.append(new_task)
        
        return jsonify(new_task), 201
        
    except Exception as e:
        return jsonify({'error': 'Invalid JSON format'}), 400

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Retrieve all tasks"""
    try:
        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task_status(task_id):
    """Update a task's status"""
    try:
        # Find the task
        task = find_task_by_id(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Validate status field
        if 'completed' not in data:
            return jsonify({'error': 'completed field is required'}), 400
        
        if not isinstance(data['completed'], bool):
            return jsonify({'error': 'completed field must be a boolean'}), 400
        
        # Update task status
        task['completed'] = data['completed']
        task['updated_at'] = datetime.now().isoformat()
        
        return jsonify(task), 200
        
    except Exception as e:
        return jsonify({'error': 'Invalid JSON format'}), 400

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        # Find the task
        task = find_task_by_id(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Remove task from list
        tasks.remove(task)
        
        return jsonify({'message': 'Task deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    """Get a specific task by ID"""
    try:
        task = find_task_by_id(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(task), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)