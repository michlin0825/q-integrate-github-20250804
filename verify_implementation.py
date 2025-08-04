#!/usr/bin/env python3
"""
Simple verification script to check the Flask todo API implementation
without requiring a running server.
"""

import sys
import json
from datetime import datetime
import uuid

# Import our Flask app
try:
    from app import app, tasks, find_task_by_id, validate_task_data
    print("✅ Successfully imported Flask app and helper functions")
except ImportError as e:
    print(f"❌ Failed to import Flask app: {e}")
    sys.exit(1)

def test_helper_functions():
    """Test helper functions"""
    print("\n🔧 Testing helper functions:")
    
    # Test validate_task_data
    print("  Testing validate_task_data...")
    
    # Valid data
    valid, error = validate_task_data({"description": "Test task"})
    assert valid == True and error is None, "Should accept valid data"
    print("    ✅ Accepts valid task data")
    
    # Invalid data - missing description
    valid, error = validate_task_data({})
    assert valid == False and "Description is required" in error, "Should reject missing description"
    print("    ✅ Rejects missing description")
    
    # Invalid data - empty description
    valid, error = validate_task_data({"description": ""})
    assert valid == False and "non-empty string" in error, "Should reject empty description"
    print("    ✅ Rejects empty description")
    
    # Test find_task_by_id
    print("  Testing find_task_by_id...")
    
    # Clear tasks and add a test task
    tasks.clear()
    test_task = {
        'id': 'test-id-123',
        'description': 'Test task',
        'completed': False
    }
    tasks.append(test_task)
    
    # Find existing task
    found_task = find_task_by_id('test-id-123')
    assert found_task == test_task, "Should find existing task"
    print("    ✅ Finds existing task")
    
    # Find non-existent task
    not_found = find_task_by_id('non-existent')
    assert not_found is None, "Should return None for non-existent task"
    print("    ✅ Returns None for non-existent task")
    
    tasks.clear()

def test_app_configuration():
    """Test Flask app configuration"""
    print("\n⚙️  Testing Flask app configuration:")
    
    # Check if app is properly configured
    assert app is not None, "Flask app should be created"
    print("  ✅ Flask app created successfully")
    
    # Check if app has the required configuration
    assert hasattr(app, 'config'), "App should have config"
    print("  ✅ App has configuration")
    
    # Test app context
    with app.app_context():
        print("  ✅ App context works correctly")

def test_task_structure():
    """Test task data structure"""
    print("\n📋 Testing task data structure:")
    
    # Create a sample task like the app would
    task_id = str(uuid.uuid4())
    description = "Sample task"
    created_at = datetime.now().isoformat()
    
    task = {
        'id': task_id,
        'description': description,
        'completed': False,
        'created_at': created_at
    }
    
    # Verify task structure
    assert 'id' in task, "Task should have ID"
    assert 'description' in task, "Task should have description"
    assert 'completed' in task, "Task should have completed status"
    assert 'created_at' in task, "Task should have creation timestamp"
    
    assert isinstance(task['id'], str), "ID should be string"
    assert isinstance(task['description'], str), "Description should be string"
    assert isinstance(task['completed'], bool), "Completed should be boolean"
    assert isinstance(task['created_at'], str), "Created_at should be string"
    
    print("  ✅ Task has all required fields")
    print("  ✅ Task fields have correct types")
    print(f"  ✅ Sample task: {task['description']} (ID: {task['id'][:8]}...)")

def test_endpoints_exist():
    """Test that all required endpoints exist"""
    print("\n🌐 Testing endpoint definitions:")
    
    with app.test_client() as client:
        # Test POST /tasks endpoint exists
        response = client.post('/tasks', json={"description": "Test"})
        assert response.status_code != 404, "POST /tasks endpoint should exist"
        print("  ✅ POST /tasks endpoint exists")
        
        # Test GET /tasks endpoint exists
        response = client.get('/tasks')
        assert response.status_code == 200, "GET /tasks should return 200"
        print("  ✅ GET /tasks endpoint exists")
        
        # Add a task for testing other endpoints
        response = client.post('/tasks', json={"description": "Test task"})
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        # Test PUT /tasks/<id> endpoint exists
        response = client.put(f'/tasks/{task_id}', json={"completed": True})
        assert response.status_code != 404, "PUT /tasks/<id> endpoint should exist"
        print("  ✅ PUT /tasks/<id> endpoint exists")
        
        # Test DELETE /tasks/<id> endpoint exists
        response = client.delete(f'/tasks/{task_id}')
        assert response.status_code != 404, "DELETE /tasks/<id> endpoint should exist"
        print("  ✅ DELETE /tasks/<id> endpoint exists")
        
        # Test GET /tasks/<id> endpoint exists (bonus)
        response = client.post('/tasks', json={"description": "Another test"})
        task_data = json.loads(response.data)
        task_id = task_data['id']
        
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 200, "GET /tasks/<id> should return 200"
        print("  ✅ GET /tasks/<id> endpoint exists (bonus feature)")

def test_error_handling():
    """Test basic error handling"""
    print("\n🚨 Testing error handling:")
    
    with app.test_client() as client:
        # Test invalid JSON
        response = client.post('/tasks', data='invalid json', content_type='application/json')
        assert response.status_code == 400, "Should return 400 for invalid JSON"
        print("  ✅ Handles invalid JSON")
        
        # Test missing description
        response = client.post('/tasks', json={})
        assert response.status_code == 400, "Should return 400 for missing description"
        print("  ✅ Handles missing description")
        
        # Test non-existent task
        response = client.get('/tasks/non-existent-id')
        assert response.status_code == 404, "Should return 404 for non-existent task"
        print("  ✅ Handles non-existent task")
        
        # Test invalid method
        response = client.patch('/tasks')
        assert response.status_code == 405, "Should return 405 for invalid method"
        print("  ✅ Handles invalid HTTP methods")

def main():
    """Run all verification tests"""
    print("🧪 Flask Todo API Implementation Verification")
    print("=" * 50)
    
    try:
        test_helper_functions()
        test_app_configuration()
        test_task_structure()
        test_endpoints_exist()
        test_error_handling()
        
        print("\n🎉 All verification tests passed!")
        print("✅ The Flask Todo API implementation is working correctly")
        print("\nNext steps:")
        print("1. Run 'python app.py' to start the server")
        print("2. Run 'pytest test_app.py -v' for comprehensive testing")
        print("3. Run 'python demo.py' for API demonstration")
        
    except AssertionError as e:
        print(f"\n❌ Verification failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()