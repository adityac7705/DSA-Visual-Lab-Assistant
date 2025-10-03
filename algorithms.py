# algorithms.py

# ------------------ Sorting ------------------
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

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

def merge_sort_steps(arr):
    # A list of all steps/snapshots for the visualization
    steps = []
    
    # Global state container for the tree
    # This list of lists will hold the sub-arrays at each level and will be updated during merging.
    global_tree_state = []

    # ------------------ Helper Functions ------------------
    
    def build_initial_tree(a, branches, level=0):
        """
        Builds the static initial structure for the visualization (the 'Split' phase).
        """
        # Ensure the branches list has an entry for the current level
        while len(branches) < level + 1:
            branches.append([])
        
        # Store the current sub-array
        branches[level].append(a[:])
        
        if len(a) > 1:
            mid = len(a) // 2
            build_initial_tree(a[:mid], branches, level + 1)
            build_initial_tree(a[mid:], branches, level + 1)
        
    def snapshot(info, active=None, done=None):
        """
        Captures a deep-copy of the current global_tree_state for a step.
        """
        snap = []
        for lvl in global_tree_state:
            snap.append([sub[:] for sub in lvl])
        return {
            "tree": snap,
            "active": active or [],
            "done": done or [],
            "info": info
        }
        
    def do_sort_recursive(a, base_level=0, base_idx=0):
        """
        The main recursive function that performs sorting and generates steps.
        It updates the global_tree_state in place when a merge is complete.
        """
        n = len(a)
        if n <= 1:
            return a[:]

        mid = n // 2
        
        # Recursive calls
        left = do_sort_recursive(a[:mid], base_level + 1, base_idx * 2)
        right = do_sort_recursive(a[mid:], base_level + 1, base_idx * 2 + 1)
        
        # --- Merging Starts (Conquer & Combine Phase) ---
        
        child1 = {"level": base_level + 1, "idx": base_idx * 2}
        child2 = {"level": base_level + 1, "idx": base_idx * 2 + 1}
        parent = {"level": base_level, "idx": base_idx}

        # Step: Highlight the two sub-lists that are about to be merged
        steps.append(snapshot(
            info=f"Merging sub-lists: {left} and {right}",
            active=[child1, child2]
        ))
        
        # Perform the actual merge (standard merge sort logic)
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])

        # Step: Update the parent node in the global state with the merged result
        global_tree_state[base_level][base_idx] = merged
        
        # Step: Show the sorted result, marking the children as 'done' (merged)
        steps.append(snapshot(
            info=f"Merged and sorted result: {merged}",
            done=[child1, child2, parent] # Mark children as merged, and parent as the newly sorted list
        ))
        
        return merged
    
    # ------------------ Execution Start ------------------
    
    # 1. Initialize the global state by splitting the array completely
    build_initial_tree(arr[:], global_tree_state)
    
    # Step 1: Show the complete split tree (Matches the Divide phase in the image)
    steps.append(snapshot(info="Steps 1-2: Split array into sub-lists recursively down to individual elements/pairs."))

    # Step 2: Call the recursive function to start the merging process
    do_sort_recursive(arr[:])
    
    # Step 3: Final step showing the completed list
    steps.append(snapshot(info="Merge Sort Complete. Full list is sorted.", done=[{"level": 0, "idx": 0}]))
    
    return steps

    do_sort(arr[:])
    return steps


def quick_sort_steps(arr):
    steps = []
    arr = arr[:]

    def quick_sort(a, low, high):
        if low < high:
            p = partition(a, low, high)
            quick_sort(a, low, p-1)
            quick_sort(a, p+1, high)

    def partition(a, low, high):
        pivot = a[high]
        i = low-1
        for j in range(low, high):
            steps.append({"array": list(a), "highlight": [j, high], "action": "compare"})
            if a[j] < pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                steps.append({"array": list(a), "highlight": [i, j], "action": "swap"})
        a[i+1], a[high] = a[high], a[i+1]
        steps.append({"array": list(a), "highlight": [i+1, high], "action": "swap"})
        return i+1

    quick_sort(arr, 0, len(arr)-1)
    steps.append({"array": list(arr), "highlight": [], "action": "done"})
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
def dfs_steps(graph, start):
    visited = set()
    stack = [start]
    steps = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            steps.append({"visited": sorted(list(visited)), "current": node, "action": "visit"})
            stack.extend(reversed(graph.get(node, [])))
    steps.append({"visited": sorted(list(visited)), "current": None, "action": "done"})
    return steps


def bfs_steps(graph, start):
    visited = set()
    queue = [start]
    steps = [{"visited": [], "current": start, "action": "visit"}]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            steps.append({"visited": sorted(list(visited)), "current": node, "action": "visit"})
            queue.extend(graph.get(node, []))
    steps.append({"visited": sorted(list(visited)), "current": None, "action": "done"})
    return steps
