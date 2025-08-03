from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

def bubble_sort(arr):
    return sorted_arr

def merge_sort(arr):
    return sorted_arr

def quick_sort(arr):
    return sorted_arr

def simulate_stack(arr):
    return operations

def simulate_queue(arr):
    return operations

def binary_search(arr):
    return steps


@app.route('/')
def index():
    return render_template('index.html')    #To send index.html to browser when user visits root URL

@app.route('/process', methods=['POST'])
def process_algorithm():                    #Collects data from frontend and runs required algorithm
    data = request.json
    algorithm = data['algorithm']
    array = data['array']

    if algorithm == 'bubble':
        result = bubble_sort(array)
    elif algorithm == 'merge':
        result = merge_sort(array)
    elif algorithm == 'quick':
        result = quick_sort(array)
    elif algorithm == 'stack':
        result = simulate_stack(array)
    elif algorithm == 'queue':
        result = simulate_queue(array)
    elif algorithm == 'bst':
        result = simulate_bst(array)
    elif algorithm == 'binary':
        target = data.get('target', None)
        result = binary_search(array, target)
    else:
        result = "Invalid Algorithm"


    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)