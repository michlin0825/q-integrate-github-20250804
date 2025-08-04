#!/usr/bin/env python3
"""
Demo script to showcase the Flask Todo API functionality.
This script demonstrates all the API endpoints and their usage.
"""

import requests
import json
import time

def demo_api():
    """Demonstrate the Flask Todo API functionality"""
    base_url = "http://localhost:5000"
    
    print("🚀 Flask Todo API Demo")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/tasks")
        if response.status_code != 200:
            print("❌ Server is not running. Please start the Flask app first with: python app.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Flask app first with: python app.py")
        return
    
    print("✅ Server is running!")
    print()
    
    # 1. Get all tasks (should be empty initially)
    print("1️⃣  Getting all tasks (should be empty initially):")
    response = requests.get(f"{base_url}/tasks")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # 2. Add some tasks
    print("2️⃣  Adding new tasks:")
    tasks_to_add = [
        "Buy groceries",
        "Learn Flask",
        "Write documentation",
        "Deploy to production"
    ]
    
    created_tasks = []
    for task_desc in tasks_to_add:
        response = requests.post(f"{base_url}/tasks", 
                               json={"description": task_desc})
        print(f"Added task: '{task_desc}' - Status: {response.status_code}")
        if response.status_code == 201:
            created_tasks.append(response.json())
    print()
    
    # 3. Get all tasks again
    print("3️⃣  Getting all tasks after adding:")
    response = requests.get(f"{base_url}/tasks")
    print(f"Status: {response.status_code}")
    all_tasks = response.json()
    print(f"Total tasks: {len(all_tasks['tasks'])}")
    for i, task in enumerate(all_tasks['tasks'], 1):
        status = "✅" if task['completed'] else "⏳"
        print(f"  {i}. {status} {task['description']} (ID: {task['id'][:8]}...)")
    print()
    
    # 4. Get a specific task by ID
    if created_tasks:
        task_id = created_tasks[0]['id']
        print(f"4️⃣  Getting specific task by ID ({task_id[:8]}...):")
        response = requests.get(f"{base_url}/tasks/{task_id}")
        print(f"Status: {response.status_code}")
        print(f"Task: {response.json()['description']}")
        print()
    
    # 5. Update task status
    if created_tasks:
        task_id = created_tasks[0]['id']
        print(f"5️⃣  Updating task status to completed ({task_id[:8]}...):")
        response = requests.put(f"{base_url}/tasks/{task_id}", 
                              json={"completed": True})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            updated_task = response.json()
            print(f"Task '{updated_task['description']}' marked as completed ✅")
        print()
    
    # 6. Get all tasks to see the update
    print("6️⃣  Getting all tasks after update:")
    response = requests.get(f"{base_url}/tasks")
    all_tasks = response.json()
    for i, task in enumerate(all_tasks['tasks'], 1):
        status = "✅" if task['completed'] else "⏳"
        print(f"  {i}. {status} {task['description']}")
    print()
    
    # 7. Delete a task
    if created_tasks and len(created_tasks) > 1:
        task_id = created_tasks[1]['id']
        task_desc = created_tasks[1]['description']
        print(f"7️⃣  Deleting task '{task_desc}' ({task_id[:8]}...):")
        response = requests.delete(f"{base_url}/tasks/{task_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Task deleted successfully 🗑️")
        print()
    
    # 8. Final state
    print("8️⃣  Final state of all tasks:")
    response = requests.get(f"{base_url}/tasks")
    all_tasks = response.json()
    print(f"Total tasks remaining: {len(all_tasks['tasks'])}")
    for i, task in enumerate(all_tasks['tasks'], 1):
        status = "✅" if task['completed'] else "⏳"
        print(f"  {i}. {status} {task['description']}")
    print()
    
    # 9. Error handling demonstration
    print("9️⃣  Demonstrating error handling:")
    
    # Try to get non-existent task
    print("  - Getting non-existent task:")
    response = requests.get(f"{base_url}/tasks/nonexistent-id")
    print(f"    Status: {response.status_code}, Error: {response.json()['error']}")
    
    # Try to add task without description
    print("  - Adding task without description:")
    response = requests.post(f"{base_url}/tasks", json={})
    print(f"    Status: {response.status_code}, Error: {response.json()['error']}")
    
    # Try to update with invalid data
    if created_tasks:
        task_id = created_tasks[0]['id']
        print("  - Updating task with invalid completed value:")
        response = requests.put(f"{base_url}/tasks/{task_id}", 
                              json={"completed": "invalid"})
        print(f"    Status: {response.status_code}, Error: {response.json()['error']}")
    
    print()
    print("🎉 Demo completed! The Flask Todo API is working correctly.")

if __name__ == "__main__":
    demo_api()