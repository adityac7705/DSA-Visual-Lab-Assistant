# algorithms.py

# ------------------ Sorting ------------------
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# ✅ Define helper at very top
def _convert_input(arr):
    """Ensure arr is a list of integers."""
    if isinstance(arr, str):
        arr = [int(x) for x in arr.split(",") if x.strip().isdigit()]
    return [int(x) for x in arr]


def bubble_sort_steps(arr):
    """
    Performs Bubble Sort and records the steps.
    Returns: (final_array, steps_list)
    """
    # Defensive copy and type conversion
    try:
        arr = [int(x) for x in arr]
    except (ValueError, TypeError):
        error_steps = [{"array": arr, "highlight": [], "action": "error", "message": "Non-numeric input detected."}]
        return [], error_steps
        
    current_arr = arr[:]
    steps = []
    n = len(current_arr)

    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            # 1. Record comparison
            steps.append({"array": list(current_arr), "highlight": [j, j+1], "action": "compare"})
            
            if current_arr[j] > current_arr[j+1]:
                # 2. Perform swap
                current_arr[j], current_arr[j+1] = current_arr[j+1], current_arr[j]
                swapped = True
                # 3. Record swap
                steps.append({"array": list(current_arr), "highlight": [j, j+1], "action": "swap"})
        
        if not swapped:
            break
            
    # Final state
    steps.append({"array": list(current_arr), "highlight": [], "action": "done"})
    
    # CRITICAL FIX: Return two values to match '_, steps = ...' in app.py
    return current_arr, steps


# algorithms.py (Modified merge_sort_steps function)

# algorithms.py
def merge_sort_steps(arr):
    """
    Build a visual tree and emit step snapshots for split and merge phases.
    Each snapshot contains:
      - tree: list of levels, each level is a list of arrays (list of ints)
      - active: list of {"level": int, "idx": int} currently being processed
      - done: list of {"level": int, "idx": int} already finished/merged
      - info: short textual description
    """
    # defensive copy / convert
    try:
        arr = [int(x) for x in arr]
    except Exception:
        arr = list(arr)

    steps = []
    # global tree state: list of levels; each level is list of nodes (each node is a list)
    global_tree_state = []

    # Build initial static split tree structure
    def build_initial_tree(a, level=0, idx=0):
        """
        Ensure global_tree_state has levels and nodes placeholders.
        We'll append actual arrays at build-time to represent the split phase.
        Returns nothing; fills global_tree_state[level][idx] = subarray
        """
        # ensure level exists
        while len(global_tree_state) <= level:
            global_tree_state.append([])

        # ensure place for idx (fill with None placeholders until idx exists)
        while len(global_tree_state[level]) <= idx:
            global_tree_state[level].append([])  # placeholder

        # store the current subarray
        global_tree_state[level][idx] = a[:]

        if len(a) > 1:
            mid = len(a) // 2
            build_initial_tree(a[:mid], level + 1, idx * 2)
            build_initial_tree(a[mid:], level + 1, idx * 2 + 1)

    def snapshot(info="", active=None, done=None):
        # deep copy of global tree (list of lists)
        tree_copy = [[node[:] for node in level] for level in global_tree_state]
        return {
            "tree": tree_copy,
            "active": active or [],
            "done": done or [],
            "info": info or ""
        }

    # Recursive merge sort that updates the global tree and emits snapshots
    def sort_and_record(a, level=0, idx=0):
        # base: single element => already present in global_tree_state
        if len(a) <= 1:
            # show the leaf as reached (split snapshot)
            steps.append(snapshot(info=f"Reached leaf: {a}", active=[{"level": level, "idx": idx}]))
            # mark leaf done (optional) — but we wait until merges to mark real done
            return a[:]

        # Split snapshot (highlight current node and its children)
        steps.append(snapshot(
            info=f"Splitting node: {a}",
            active=[{"level": level, "idx": idx},
                    {"level": level + 1, "idx": idx * 2},
                    {"level": level + 1, "idx": idx * 2 + 1}]
        ))

        mid = len(a) // 2
        left = sort_and_record(a[:mid], level + 1, idx * 2)
        right = sort_and_record(a[mid:], level + 1, idx * 2 + 1)

        # Before merging: highlight the two child nodes
        steps.append(snapshot(
            info=f"About to merge {left} and {right}",
            active=[{"level": level + 1, "idx": idx * 2}, {"level": level + 1, "idx": idx * 2 + 1}]
        ))

        # perform merge
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        if i < len(left):
            merged.extend(left[i:])
        if j < len(right):
            merged.extend(right[j:])

        # Place merged into parent's spot in the global state
        global_tree_state[level][idx] = merged[:]

        # After merging snapshot: mark children as done and parent as updated
        steps.append(snapshot(
            info=f"Merged into {merged}",
            done=[
                {"level": level + 1, "idx": idx * 2},
                {"level": level + 1, "idx": idx * 2 + 1},
                {"level": level, "idx": idx}
            ]
        ))
        return merged

    # Initialize tree placeholders by splitting completely
    build_initial_tree(arr[:])  # fills global_tree_state with all nodes and leaves

    # First snapshot: show full split tree
    steps.append(snapshot(info="Initial full split structure (divide phase)"))

    # Start recursion (this will append split & merge snapshots)
    sort_and_record(arr[:], level=0, idx=0)

    # Final snapshot: fully sorted at root
    steps.append(snapshot(info="Merge Sort complete", done=[{"level": 0, "idx": 0}]))

    return steps

def quick_sort_steps(arr):
    arr = _convert_input(arr)
    steps = []

    def record_state(array, low, high, pivot_index, left_ptr, right_ptr, action, message):
        steps.append({
            "array": array.copy(),
            "low": low,
            "high": high,
            "pivot_index": pivot_index,
            "left_ptr": left_ptr,
            "right_ptr": right_ptr,
            "action": action,
            "message": message
        })

    def partition(low, high):
        pivot = arr[low]
        left = low + 1
        right = high

        record_state(arr, low, high, low, left, right, "init", f"Starting partition from index {low} to {high} with pivot {pivot}")

        while True:
            while left <= right and arr[left] < pivot:
                record_state(arr, low, high, low, left, right, "left_stop", f"Left pointer moved right to {left}, value {arr[left]}")
                left += 1

            while left <= right and arr[right] > pivot:
                record_state(arr, low, high, low, left, right, "right_stop", f"Right pointer moved left to {right}, value {arr[right]}")
                right -= 1

            if left > right:
                break

            arr[left], arr[right] = arr[right], arr[left]
            record_state(arr, low, high, low, left, right, "swap", f"Swapped elements at {left} and {right}: {arr[left]} ↔ {arr[right]}")

        arr[low], arr[right] = arr[right], arr[low]
        record_state(arr, low, high, low, left, right, "final_placement", f"Placed pivot {pivot} in correct position at index {right}")

        return right

    def quick_sort(low, high):
        if low < high:
            p = partition(low, high)
            quick_sort(low, p - 1)
            quick_sort(p + 1, high)
        else:
            record_state(arr, low, high, low, None, None, "done", "Subarray of size 1 or empty — already sorted.")

    quick_sort(0, len(arr) - 1)
    return arr, steps





# ------------------ Searching ------------------
def linear_search_steps(arr, target):
    steps = []
    for i, val in enumerate(arr):
        steps.append({"array": list(arr), "highlight": [i], "action": "compare", "target": target})
        if val == target:
            steps.append({"array": list(arr), "highlight": [i], "action": "found", "target": target})
            break
    return steps


def binary_search_steps(arr, target):
    steps = []

    # Convert input to numbers
    try:
        arr = [int(x) for x in arr]
        target = int(target)
    except:
        return [{"action": "error", "message": "Invalid input"}]

    arr.sort()
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        steps.append({
            "array": arr.copy(),
            "low": low,
            "mid": mid,
            "high": high,
            "value": arr[mid],
            "target": target,
            "action": "compare"
        })

        if arr[mid] == target:
            steps.append({
                "array": arr.copy(),
                "low": low,
                "mid": mid,
                "high": high,
                "value": arr[mid],
                "target": target,
                "action": "found"
            })
            return steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    steps.append({
        "array": arr.copy(),
        "low": low,
        "mid": -1,
        "high": high,
        "value": None,
        "target": target,
        "action": "not_found"
    })
    return steps



# ------------------ Stack ------------------
def stack_steps(ops):
    stack = []
    steps = []
    for op in ops:
        parts = op.strip().split()
        if parts[0].lower() == "push" and len(parts) > 1:
            val = parts[1]
            stack.append(val)
            steps.append({"stack": list(stack), "action": "push", "value": val})
        elif parts[0].lower() == "pop":
            val = stack.pop() if stack else None
            steps.append({"stack": list(stack), "action": "pop", "value": val})
    return steps


# ------------------ Queue ------------------
def queue_steps(ops):
    queue = []
    steps = [{
        "queue": [],
        "action": "empty queue",
        "value": None,
        "rawOp": "Start"
    }]

    for op in ops:
        if not isinstance(op, str) or not op.strip():
            steps.append({
                "queue": list(queue),
                "action": "noop",
                "value": None,
                "rawOp": str(op) + " (Unknown Op)"
            })
            continue

        parts = op.strip().split()
        action = parts[0].lower()
        op_text = op.strip()

        if action == "enqueue" and len(parts) > 1:
            val = ' '.join(parts[1:])
            queue.append(val)
            steps.append({
                "queue": list(queue),
                "action": "enqueue",
                "value": val,
                "rawOp": op_text
            })
        elif action == "dequeue":
            if queue:
                val = queue.pop(0)
                steps.append({
                    "queue": list(queue),
                    "action": "dequeue",
                    "value": val,
                    "rawOp": op_text
                })
            else:
                steps.append({
                    "queue": list(queue),
                    "action": "dequeue (error)",
                    "value": None,
                    "rawOp": op_text + " (Queue Empty)"
                })
        else:
            steps.append({
                "queue": list(queue),
                "action": "noop",
                "value": None,
                "rawOp": op_text + " (Unknown Op)"
            })

    return steps


# ------------------ BST ------------------
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def bst_insert_steps(arr):
    steps = []
    root = None

    def insert(node, val):
        if node is None:
            steps.append({"bst": tree_snapshot(root), "action": "insert", "value": val})
            return TreeNode(val)
        if val < node.val:
            node.left = insert(node.left, val)
        else:
            node.right = insert(node.right, val)
        return node

    def tree_snapshot(node):
        res = []
        def inorder(nd):
            if nd:
                inorder(nd.left)
                res.append(nd.val)
                inorder(nd.right)
        inorder(node)
        return res

    for val in arr:
        root = insert(root, val)
    steps.append({"bst": tree_snapshot(root), "action": "done"})
    return steps


# ------------------ DFS / BFS ------------------
# algorithms.py
# Contains the core algorithm logic for various visualizations.

# logic.py

"""
This module contains the step-by-step logic for various algorithms
to be used in a visualization application. Each function returns a list
of 'steps', where each step is a dictionary describing the state of 
the visualization (e.g., array, visited set, stack) at that point.
"""

import math

# --- Graph Algorithms ---

def dfs_steps(graph, start=None):
    """
    Iterative DFS returning steps for visualization.
    Each step includes:
      - current node
      - visited nodes
      - stack state
      - interpretation
    If start is None, pick the first node in the graph automatically.
    """
    if not graph:
        return []

    if start is None:
        start = next(iter(graph.keys()))  # pick first node automatically

    visited = set()
    stack = [start]
    steps = []

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            steps.append({
                "current": current,
                "visited": list(visited),
                "stack": list(stack),
                "interpretation": f"Visiting node {current}, stack contains {list(stack)}"
            })
            # Add neighbors in reversed order to preserve DFS order
            for neighbor in reversed(graph.get(current, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    return steps


def bfs_steps(graph, start=None):
    """
    Iterative BFS returning steps for visualization.
    Each step includes:
      - current node
      - visited nodes
      - queue state
      - interpretation
    If start is None, pick the first node in the graph automatically.
    """
    if not graph:
        return []

    if start is None:
        start = next(iter(graph.keys()))

    visited = set()
    queue = [start]
    steps = []

    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            steps.append({
                "current": current,
                "visited": list(visited),
                "queue": list(queue),
                "interpretation": f"Visiting node {current}, queue contains {list(queue)}"
            })
            # Add neighbors in order
            for neighbor in graph.get(current, []):
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
    return steps


# algorithms.py (Heap Sort addition with inner helper functions)

# algorithms.py (Modified Heap Sort Logic)
import math

# --- PYTHON MIN-HEAP LOGIC INSIDE HEAP SORT ---
# heap_logic.py
def heap_sort_steps(arr, heap_type="max"):
    """
    Generates a list of steps for visualizing the Heap Sort algorithm.
    Each step is a dictionary containing the array state, heap size,
    highlighted indices, and the action taken.

    Args:
        arr (list): The array to be sorted (modified in place for tracking).
        heap_type (str): "max" for max-heap (ascending sort), "min" for min-heap (descending sort).

    Returns:
        list: A sequence of step dictionaries.
    """
    steps = []
    n = len(arr)

    def compare(a, b):
        """Custom comparison function based on heap_type."""
        return a > b if heap_type == "max" else a < b

    def heapify(arr, heap_size, i):
        """
        Performs heapify operation at index i and logs the steps.
        heap_size 'n' is the current boundary of the heap within the array.
        """
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        # 1. Log the state at the start of heapify (to check property)
        highlights = [i]
        if l < heap_size: highlights.append(l)
        if r < heap_size: highlights.append(r)
        
        steps.append({
            "array": arr.copy(),
            "heap_size": heap_size,
            "highlight": highlights,
            "action": "compare_check",
            "info": f"Check heap property for node {i} (val: {arr[i]})"
        })

        # 2. Determine largest/smallest index
        if l < heap_size and compare(arr[l], arr[largest]):
            largest = l
        if r < heap_size and compare(arr[r], arr[largest]):
            largest = r

        # 3. If the largest/smallest is not the root, swap and recurse
        if largest != i:
            # Perform swap
            arr[i], arr[largest] = arr[largest], arr[i]
            
            # Log the swap action
            steps.append({
                "array": arr.copy(),
                "heap_size": heap_size,
                "highlight": [i, largest],
                "action": "swap_fix_heap",
                "info": f"Swap index {i} and {largest} to fix heap property"
            })
            
            # Recursively heapify the affected sub-tree
            heapify(arr, heap_size, largest)
        else:
            # FIX: Log successful heap property (no swap needed)
            steps.append({
                "array": arr.copy(),
                "heap_size": heap_size,
                "highlight": [i],
                "action": "heapify_end_ok",
                "info": f"Heap property holds at index {i}. Subtree is a valid heap."
            })

    # --- 1. Build Heap Phase ---
    # The heap starts from the first non-leaf node (n // 2 - 1) up to the root (0)
    steps.append({
        "array": arr.copy(),
        "heap_size": n,
        "highlight": [],
        "action": "start_build_heap",
        "info": f"Starting Build Heap phase ({heap_type}-heap)"
    })

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # --- 2. Extract Elements and Sort Phase ---
    steps.append({
        "array": arr.copy(),
        "heap_size": n,
        "highlight": [],
        "action": "start_sort_phase",
        "info": "Starting Sort Phase (Extracting elements)"
    })

    for i in range(n - 1, 0, -1):
        # Swap root (max/min element) with the last element of the unsorted region
        arr[0], arr[i] = arr[i], arr[0]
        
        # Log the extraction swap. The new heap size is i.
        steps.append({
            "array": arr.copy(),
            "heap_size": i, # The new heap size for the next heapify
            "highlight": [0, i],
            "action": "swap_root_extract",
            "info": f"Swap root (0) with index {i}. Element at {i} is now sorted."
        })
        
        # Call heapify on the reduced heap
        heapify(arr, i, 0)

    # --- 3. Final Step ---
    steps.append({
        "array": arr.copy(),
        "heap_size": 0,
        "highlight": list(range(n)),
        "action": "sorted",
        "info": "Array sorted successfully."
    })

    return steps

# Example Usage (optional, for testing):
# array_to_sort = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
# steps = heap_sort_steps(array_to_sort.copy())
# print(steps)
