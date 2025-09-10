from flask import Flask, render_template, jsonify, request
import algorithms
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visualize")
def visualize():
    return render_template("visualize.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/quiz-data")
def quiz_data():
    algorithm = request.args.get("algorithm", "").lower()
    try:
        with open("quiz_questions.json") as f:
            all_questions = json.load(f)
    except Exception as e:
        return jsonify({"error": "Failed to load quiz questions"}), 500

    # Filter questions for requested algorithm; return empty list if missing
    questions = all_questions.get(algorithm, [])
    return jsonify(questions)

@app.route("/run-algo", methods=["POST"])
def run_algo():
    data = request.get_json()
    algo = data.get("algo")
    arr = data.get("arr")
    target = data.get("target")
    ops = data.get("ops")
    graph = data.get("graph")
    start = data.get("start")

    if algo == "bubble":
        _, steps = algorithms.bubble_sort_steps(arr)
        return jsonify({"steps": steps})
    elif algo == "merge":
        steps = algorithms.merge_sort_steps(arr)
        return jsonify({"steps": steps})
    elif algo == "quick":
        _, steps = algorithms.quick_sort_steps(arr)
        return jsonify({"steps": steps})
    elif algo == "linear":
        steps = algorithms.linear_search_steps(arr, target)
        return jsonify({"steps": steps})
    elif algo == "binary":
        steps = algorithms.binary_search_steps(arr, target)
        return jsonify({"steps": steps})
    elif algo == "stack":
        steps = algorithms.stack_steps(ops)
        return jsonify({"steps": steps})
    elif algo == "queue":
        steps = algorithms.queue_steps(ops)
        return jsonify({"steps": steps})
    elif algo == "bst":
        steps = algorithms.bst_insert_steps(arr)
        return jsonify({"steps": steps})
    elif algo == "dfs":
        steps = algorithms.dfs_steps(graph, start)
        return jsonify({"steps": steps})
    elif algo == "bfs":
        steps = algorithms.bfs_steps(graph, start)
        return jsonify({"steps": steps})
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

if __name__ == "__main__":
    app.run(debug=True)
