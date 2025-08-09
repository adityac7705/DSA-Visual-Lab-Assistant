from flask import Flask, request, jsonify, render_template
from collections import deque
app = Flask(__name__)

#--------------------Sorting--------------------
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

#--------------------Searching--------------------

def linear_search(arr, target):
    steps = []
    for i in range(len(arr)):
        steps.append({'action': 'check', 'index': i, 'value': arr[i]})
        if arr[i] == target:
            steps.append({'action': 'found','index': i, 'value': arr[i]})
            return steps
    steps.append({'action': 'not_found', 'index': -1, 'value': None})
    return steps

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


def dfs(graph, start):
    visited = set()
    result = []

    def dfs_recursive(node):
        if node not in visited:
            visited.add(node)
            result.append(node)
            for neighbor in graph.get(node, []):
                dfs_recursive(neighbor)

    dfs_recursive(start)
    return result


def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            result.append(node)
            queue.extend(graph.get(node, []))

    return result

#--------------------Data Structures--------------------

def binary_search_tree(arr):
    if not arr:
        return None

    mid = len(arr) // 2
    root = arr[mid]
    left_subtree = binary_search_tree(arr[:mid])
    right_subtree = binary_search_tree(arr[mid+1:])

    return {'value': root, 'left': left_subtree, 'right': right_subtree}

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        return self.items.copy()
    
    def pop(self):
        if not self.is_empty():
            self.items.pop()
        return self.items.copy()
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0

def simulate_stack(operations):
    s = Stack()
    steps = []

    for op, value in operations:
        if op == 'push':
            state = s.push(value)
            steps.append({'operation': f'push({value})', 'stack': state})
        elif op == 'pop':
            if s.is_empty():
                steps.append({'operation': f'pop() -> None', 'stack': s.items.copy()})
            else:
                popped_value = s.peek()
                state = s.pop()
                steps.append({'operation': f'pop() -> {popped_value}', 'stack': state})
        elif op == 'peek':
            peek_value = s.peek()
            state = s.items.copy()
            steps.append({'operation': f'peek() -> {peek_value}', 'stack': state})
    return steps

class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
        return self.items.copy()
    
    def dequeue(self):
        if not self.is_empty():
            self.items.pop(0)
        return self.items.copy()
    
    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None
    
    def rear(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0
        

def simulate_queue(operations):
    q = Queue()
    steps = []

    for op, value in operations:
        if op == 'enqueue':
            state = q.enqueue(value)
            steps.append({'operation': f'enqueue({value})', 'queue': state})
        elif op == 'dequeue':
            if q.is_empty():
                steps.append({'operation': f'dequeue() -> None', 'queue': q.items.copy()})
            else:
                dequeued_value = q.front()
                state = q.dequeue()
                steps.append({'operation': f'dequeue() -> {dequeued_value}', 'queue': state})
        elif op == 'front':
            front_value = q.front()
            state = q.items.copy()
            steps.append({'operation': f'front() -> {front_value}', 'queue': state})
        elif op == 'rear':
            rear_value = q.rear()
            state = q.items.copy()
            steps.append({'operation': f'rear() -> {rear_value}', 'queue': state})
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
    elif algorithm == 'linear_search':
        target = data.get('target', None)
        result = linear_search(array, target)
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


    return jsonify({'steps': result})

if __name__ == '__main__':
    app.run(debug=True)