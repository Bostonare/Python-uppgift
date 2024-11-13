from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

tasks = [{"id": 1, "name": "throw garbage", "category": ["house_task"], "status": "pending"}, {"id": 2, "name": "Do homework","category": ["education"], "status": "pending"}]

@app.route("/tasks", methods = ["GET"])
def get_tasks():
    if len(tasks) == 0:
        return jsonify({"error": "No tasks found"}), 404
    
    return jsonify({
        "message": "List of all tasks",
        "tasks": tasks,
        "total_tasks": len(tasks)
    }), 200
    

@app.route("/add_task/place_in_category", methods = ["POST"])
def json_addtasks():
   
    if not request.is_json:
        return jsonify({"error":"invalid input, please submit valid JSON"}), 400
    
    addtask = request.json
    task = addtask.get("task")
    category = addtask.get("category")
    status = addtask.get("status", "pending")
    
    if not task or not category:
        return jsonify({"error":"invalid input, please submit valid taskname and status!"}), 400
    
    new_task = {"id": len(tasks) + 1, "task": task, "status": status}
    tasks.append(new_task)
    
    return ({"msg" : f"task: {task} added with status :{status}"})


    
@app.route("/delete_task/<int:task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task_to_delete = next((task for task in tasks if task["id"] == task_id), None)
    
    if task_to_delete is None:
        return jsonify({"error":"Task not found"}), 404
    
    tasks.remove(task_to_delete)
    
    return jsonify({"msg": "Task was removed succesfully"})

@app.route("/task/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify({
        "message": f"Task with ID {task_id}",
        "task": task
    }), 200
    
@app.route("/update_task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
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
def update_task_complete(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error":"Task not found!"}), 404
    
    task ["status"] = "complete"
    
    return jsonify({"msg": f"Task with ID {task_id} has been marked as Complete.", "task": task}), 200

@app.route("/tasks/categories", methods=["GET"])
def get_categories():
    # Skapa en uppsättning (set) för att hålla unika kategorier
    categories = set()

    # Gå igenom alla uppgifter och lägg till kategorierna i setet
    for task in tasks:
        for category in task["category"]:
            categories.add(category)

    # Konvertera setet till en lista och returnera som JSON
    return jsonify(list(categories))

@app.route("/tasks/categories/<string:category_name>", methods=["GET"])
def get_tasks_by_category(category_name):
    filtered_tasks = [task for task in tasks if category_name in task["category"]]
    return jsonify(filtered_tasks)

@app.route("/")
def index():
    return render_template("To do list.html")



if __name__ == "__main__":
    app.run(debug=True)
