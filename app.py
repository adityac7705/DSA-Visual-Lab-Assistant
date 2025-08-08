from flask import Flask, request, jsonify, render_template
from collections import deque
app = Flask(__name__)

def bubble_sort(arr):
    arr = arr.copy()
    for i in range(len(arr)):
        for j in range(len(arr)-1-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])

    return result

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    sorted_array = quick_sort(left) + middle + quick_sort(right)
    return sorted_array

def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    steps = 0
    
    while left <= right:
        steps += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return steps 
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return steps  


def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited


from collections import deque

def bfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited

def binary_search_tree(arr):
    if not arr:
        return None

    mid = len(arr) // 2
    root = arr[mid]
    left_subtree = binary_search_tree(arr[:mid])
    right_subtree = binary_search_tree(arr[mid+1:])

    return {'value': root, 'left': left_subtree, 'right': right_subtree}


def simulate_stack(arr):
    return operations

def simulate_queue(arr):
    return operations


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
    elif algorithm == 'linear_search':
        result = linear_search(array)
    elif algorithm == 'binary':
        target = data.get('target', None)
        result = binary_search(array, target)
    elif algorithm == 'dfs':
        graph = data.get('graph', {})
        start = data.get('start')
        result = dfs(graph, start)
    elif algorithm == 'bfs':
        graph = data.get('graph', {})
        start = data.get('start')
        result = bfs(graph, start)
    elif algorithm == 'stack':
        result = simulate_stack(array)
    elif algorithm == 'queue':
        result = simulate_queue(array)
    elif algorithm == 'bst':
        result = binary_search_tree(array) 
    else:
        result = "Invalid Algorithm"


    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)