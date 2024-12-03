from flask import Flask, request, jsonify, render_template
import json
app = Flask(__name__)



@app.route("/tasks", methods = ["GET"])
def json_get_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)

        if len(tasks) == 0:
            return jsonify({"error": "No tasks found"}), 404

        return jsonify({
            "message": "List of all tasks",
            "tasks": tasks,
            "total_tasks": len(tasks)
        }), 200

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Error parsing JSON"}), 500
    
TASKS_FILE = 'tasks.json'

def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)
        
@app.route("/add_task/place_in_category", methods = ["POST"])
def json_addtasks():
   
    
    if not request.is_json:
        return jsonify({"error": "Invalid input, please submit valid JSON"}), 400
    
    addtask = request.json
    
   
    task_name = addtask.get("name")
    category = addtask.get("category")
    status = addtask.get("status", "pending")

    
    if not task_name or not category:
        return jsonify({"error": "Invalid input, please submit valid task name and category!"}), 400
    

    
    tasks=load_tasks()
    

    new_task = {
        "id": len(tasks) + 1, 
        "name": task_name,
        "category": category,
        "status": status
    }
    
    
    tasks.append(new_task)
    
    
    save_tasks(tasks)
    
    return jsonify({"msg": f"name '{task_name}' added under category '{category}' with status '{status}'"}), 201


    
@app.route("/delete_task/<int:task_id>", methods = ["DELETE"])
def json_delete_task(task_id):
    
    tasks = load_tasks()
    task_to_delete = next((task for task in tasks if task["id"] == task_id), None)
    
    if task_to_delete is None:
        return jsonify({"error": "Task not found"}), 404
    tasks.remove(task_to_delete)
    save_tasks(tasks)
    
    return jsonify({"msg": "Task was removed successfully"}), 200


@app.route("/task/<int:task_id>", methods=["GET"])
def json_get_task(task_id):
    
    tasks = load_tasks()
    
    task = next((task for task in tasks if task["id"] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify({
        "message": f"Task with ID {task_id}",
        "task": task
    }), 200
    
@app.route("/update_task/<int:task_id>", methods=["PUT"])
def json_update_task(task_id):
    
    tasks=load_tasks()
    
    task = next((task for task in tasks if task["id"] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    if not request.is_json:
        return jsonify({"error": "Invalid input, please submit valid JSON"}), 400
    
    updated_task = request.json
    task_name = updated_task.get("task")
    status = updated_task.get("status")
    
    if task_name:
        task["task"] = task_name
    if status:
        task["status"] = status
    
    
    return jsonify({"msg": f"Task with ID {task_id} has been updated.", "task": task}), 200

@app.route("/update_task/<int:task_id>/complete", methods = ["PUT"])
def json_update_task_complete(task_id):
    
    tasks = load_tasks()
    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error":"Task not found!"}), 404
    
    task ["status"] = "complete"
    
    return jsonify({"msg": f"Task with ID {task_id} has been marked as Complete.", "task": task}), 200

@app.route("/tasks/categories", methods=["GET"])
def json_get_categories():
    
      
    tasks = load_tasks()
    
   
    categories = set()

   
    for task in tasks:
        categories.add(task["category"])
    
    
    return jsonify(list(categories))

@app.route("/tasks/categories/<string:category_name>", methods=["GET"])
def json_get_tasks_by_category(category_name):
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if category_name in task["category"]]
    return jsonify(filtered_tasks)

@app.route("/")
def json_index():
    tasks = load_tasks()
    return render_template("To do list.html", title = "To Do List", Task_list = tasks)



if __name__ == "__main__":
    app.run(debug=True)
