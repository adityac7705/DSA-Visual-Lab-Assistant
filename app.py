from flask import Flask, render_template, jsonify, request
import algorithms
import json

app = Flask(__name__, template_folder="templates")

# -------------------- ROUTES ------------------

@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/visualize")
def visualize():
    topic = request.args.get("topic")  # example: ?topic=linear
    return render_template("visualize.html", current_topic=topic)


@app.route("/linear_search")
def linear_search_page():
    return render_template("linear_search.html")



@app.route("/bfs")
def bfs_page():
    return render_template("BFS.html")

@app.route("/dfs")
def dfs_page():
    return render_template("DFS.html")

@app.route("/binary_search")
def binary_search_page():
    return render_template("binary_search.html")


@app.route("/merge_sort")
def merge_sort_page():
    return render_template("merge_sort.html")


@app.route("/bubble_sort")
def bubble_sort_page():
    return render_template("bubble_sort.html")


@app.route("/heap_sort")
def heap_sort_page():
    return render_template("heap_sort.html")


@app.route("/quick_sort")
def quick_sort_page():
    return render_template("quick_sort.html")


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
        with open("quiz_questions.json") as f:
            all_questions = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Failed to load quiz questions: {e}"}), 500

    if algorithm not in all_questions:
        return jsonify({"error": f"No questions found for '{algorithm}'"}), 404

    return jsonify(all_questions[algorithm])


# -------------------- RUN ALGORITHM --------------------
# -------------------- RUN ALGORITHM --------------------
@app.route("/run-algo", methods=["POST"])
@app.route("/run-dfs-steps", methods=["POST"])  # alias for compatibility
def run_algo():
    data = request.get_json(force=True)
    algo = data.get("algo")
    arr = data.get("arr") or []
    target = data.get("target")
    ops = data.get("ops") or []
    graph = data.get("graph") or {}
    start = data.get("start")

    try:
        if algo == "bubble":
            _, steps = algorithms.bubble_sort_steps(arr)
        elif algo == "merge":
            steps = algorithms.merge_sort_steps(arr)
        elif algo == "quick":
            _, steps = algorithms.quick_sort_steps(arr)
        elif algo == "heap":
            # Only return steps from heap_sort_steps
            steps = algorithms.heap_sort_steps(arr, heap_type=data.get("heap_type", "max"))
        elif algo == "linear":
            steps = algorithms.linear_search_steps(arr, target)
        elif algo == "binary":
            steps = algorithms.binary_search_steps(arr, target)
        elif algo == "stack":
            steps = algorithms.stack_steps(ops)
        elif algo == "queue":
            steps = algorithms.queue_steps(ops)
        elif algo == "dfs":
            steps = algorithms.dfs_steps(graph, start)
        elif algo == "bfs":
            steps = algorithms.bfs_steps(graph, start)
        else:
            return jsonify({"error": f"Unknown algorithm: {algo}"}), 400

        return jsonify({"steps": steps})

    except Exception as e:
        print(f"Algorithm execution failed for {algo}: {e}")
        return jsonify({"error": "Algorithm execution failed. Check console for details."}), 500


# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
