from flask import Flask, render_template, jsonify, request
# Removed: from flask_cors import CORS 
import algorithms
import json

app = Flask(__name__, template_folder="templates")
# Removed: CORS(app) 

# -------------------- ROUTES ------------------

@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/visualize")
def visualize():
    topic = request.args.get("topic")  # example: ?topic=linear
    # Assuming visualize.html handles generic visualization based on 'topic'
    return render_template("visualize.html", current_topic=topic)


@app.route("/linear_search")
def linear_search_page():
    return render_template("linear_search.html")


@app.route("/binary_search")
def binary_search_page():
    return render_template("binary_search.html")

@app.route("/merge_sort")
def merge_sort_page():
    # This serves the specific visualization requested
    return render_template("merge_sort.html")

@app.route("/bubble_sort")
def bubble_sort_page():
    # This serves the specific visualization requested
    return render_template("bubble_sort.html")


@app.route("/stack")
def stack_page():
    return render_template("stack.html")


@app.route("/queue")
def queue_page():
    return render_template("queue.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


@app.route("/quiz-data")
def quiz_data():
    algorithm = request.args.get("algorithm", "").lower()
    try:
        # NOTE: If 'quiz_questions.json' is not available, this will raise a FileNotFoundError.
        with open("quiz_questions.json") as f:
            all_questions = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Failed to load quiz questions: {e}"}), 500
    return jsonify(all_questions.get(algorithm, []))


# -------------------- RUN ALGORITHM (API Endpoint) --------------------
# This endpoint handles the merge sort steps request from merge_sort.html
@app.route("/run-algo", methods=["POST"])
def run_algo():
    data = request.get_json(force=True)
    algo = data.get("algo")
    arr = data.get("arr") or []          # for sorting / search
    target = data.get("target")          # for search
    ops = data.get("ops") or []          # for stack / queue
    graph = data.get("graph") or {}      # for BFS / DFS
    start = data.get("start")            # starting node
    try:
        if algo == "bubble":
            _, steps = algorithms.bubble_sort_steps(arr)
        elif algo == "merge":
            steps = algorithms.merge_sort_steps(arr) # <-- This calls the core logic
        elif algo == "quick":
            _, steps = algorithms.quick_sort_steps(arr)
        elif algo == "linear":
            steps = algorithms.linear_search_steps(arr, target)
        elif algo == "binary":
            steps = algorithms.binary_search_steps(arr, target)
        elif algo == "stack":
            steps = algorithms.stack_steps(ops)
        elif algo == "queue":
            steps = algorithms.queue_steps(ops)
        elif algo == "bst":
            steps = algorithms.bst_insert_steps(arr)
        elif algo == "dfs":
            steps = algorithms.dfs_steps(graph, start)
        elif algo == "bfs":
            steps = algorithms.bfs_steps(graph, start)
        else:
            return jsonify({"error": f"Unknown algorithm: {algo}"}), 400
        
        return jsonify({"steps": steps})
    except Exception as e:
        # Use simple error message for frontend display
        print(f"Algorithm execution failed for {algo}: {e}") 
        return jsonify({"error": "Algorithm execution failed. Check console for details."}), 500


# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
