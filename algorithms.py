def bubble_sort_steps(arr):
    arr = arr[:]
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            steps.append({"array": list(arr), "highlight": [j, j + 1], "action": "compare"})
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append({"array": list(arr), "highlight": [j, j + 1], "action": "swap"})
    steps.append({"array": list(arr), "highlight": [], "action": "done"})
    return arr, steps

def merge_sort_steps(arr):
    steps = []
    node_id = [0]  # mutable counter for unique node IDs

    def merge_sort(arr, depth=0, parent=None):
        my_id = node_id[0]
        node_id[0] += 1
        steps.append({'id': my_id, 'parent': parent, 'array': list(arr), 'depth': depth, 'type': 'split'})
        if len(arr) <= 1:
            return arr, my_id
        mid = len(arr) // 2
        left_sorted, left_id = merge_sort(arr[:mid], depth + 1, my_id)
        right_sorted, right_id = merge_sort(arr[mid:], depth + 1, my_id)
        merged = merge(left_sorted, right_sorted)
        steps.append({'id': my_id, 'parent': parent, 'array': list(merged), 'depth': depth, 'type': 'merge', 'children': [left_id, right_id]})
        return merged, my_id

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

    merge_sort(arr)
    return steps

def quick_sort_steps(arr):
    steps = []
    arr = arr[:]
    def quick_sort(arr, low, high):
        if low < high:
            p = partition(arr, low, high)
            quick_sort(arr, low, p - 1)
            quick_sort(arr, p + 1, high)
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            steps.append({"array": list(arr), "highlight": [j, high], "action": "compare"})
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append({"array": list(arr), "highlight": [i, j], "action": "swap"})
        arr[i+1], arr[high] = arr[high], arr[i+1]
        steps.append({"array": list(arr), "highlight": [i+1, high], "action": "swap"})
        return i+1
    quick_sort(arr, 0, len(arr)-1)
    steps.append({"array": list(arr), "highlight": [], "action": "done"})
    return arr, steps

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
    
    # --- Input Conversion (Important for stability) ---
    try:
        # Convert all elements to integers
        arr = [int(x) for x in arr]
        target = int(target)
    except (ValueError, TypeError):
        return [{'status': 'error', 'message': 'Invalid array or target input.'}]
    # --- End Input Conversion ---

    # --- NEW: Array Sorting ---
    # Binary Search requires the array to be sorted.
    # We sort it here to ensure the algorithm works as expected.
    arr.sort() 
    # --- End Array Sorting ---

    l, r = 0, len(arr) - 1
    
    while l <= r:
        # Calculate mid index
        m = (l + r) // 2
        
        # 1. Record the current state before comparison
        # We also include the current array state (which is sorted)
        steps.append({
            "array": list(arr), 
            "highlight": [m], 
            "action": "compare", 
            "target": target,
            "value": arr[m], # Added current value for better message display in frontend
            "low": l,        # Low pointer index
            "mid": m,        # Mid pointer index
            "high": r        # High pointer index
        })
        
        # 2. Compare and adjust pointers
        if arr[m] == target:
            # Found! Record the final step and break
            steps.append({
                "array": list(arr), 
                "highlight": [m], 
                "action": "found", 
                "target": target,
                "value": arr[m],
                "low": l, 
                "mid": m, 
                "high": r 
            })
            return steps
        elif arr[m] < target:
            # Target is in the upper half. Move low pointer.
            l = m + 1
        else:
            # Target is in the lower half. Move high pointer.
            r = m - 1
            
    # Not found after loop terminates (l > r)
    steps.append({
        "array": list(arr), 
        "highlight": [], 
        "action": "not_found", 
        "target": target,
        "value": None,
        "low": l,  # Final position of low (where it crossed high)
        "mid": -1, # Reset mid
        "high": r  # Final position of high (where it was crossed by low)
    })
    return steps

# Example usage with unsorted input:
# steps = binary_search_steps([10, 5, 1, 12, 16, 20], 12)
# print(steps[0]['array']) # Output will be the sorted array: [1, 5, 10, 12, 16, 20]

def stack_steps(ops):
    stack = []
    steps = []
    for op in ops:
        parts = op.strip().split()
        if parts[0] == "push" and len(parts) > 1:
            val = int(parts[1])
            stack.append(val)
            steps.append({"stack": list(stack), "action": "push", "value": val})
        elif parts[0] == "pop" and stack:
            val = stack.pop()
            steps.append({"stack": list(stack), "action": "pop", "value": val})
        else:
            steps.append({"stack": list(stack), "action": "noop"})
    return steps

def queue_steps(ops):
    queue = []
    steps = []
    for op in ops:
        parts = op.strip().split()
        if parts[0] == "enqueue" and len(parts) > 1:
            val = int(parts[1])
            queue.append(val)
            steps.append({"queue": list(queue), "action": "enqueue", "value": val})
        elif parts[0] == "dequeue" and queue:
            val = queue.pop(0)
            steps.append({"queue": list(queue), "action": "dequeue", "value": val})
        else:
            steps.append({"queue": list(queue), "action": "noop"})
    return steps

def bst_insert_steps(arr):
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
    steps = []
    root = None

    def insert(node, val):
        if node is None:
            new_node = Node(val)
            steps.append({"bst": tree_snapshot(root), "action": "insert", "value": val})
            return new_node
        if val < node.val:
            node.left = insert(node.left, val)
        else:
            node.right = insert(node.right, val)
        return node

    for val in arr:
        root = insert(root, val)
    steps.append({"bst": tree_snapshot(root), "action": "done"})
    return steps

def tree_snapshot(node):
    res = []
    def inorder(nd):
        if nd:
            inorder(nd.left)
            res.append(nd.val)
            inorder(nd.right)
    inorder(node)
    return res

def dfs_steps(graph, start):
    visited = set()
    stack = [start]
    steps = []
    while stack:
        node = stack.pop()
        steps.append({"visited": sorted(list(visited)), "current": node, "action": "visit"})
        if node not in visited:
            visited.add(node)
            stack.extend(reversed(graph.get(node, [])))
    steps.append({"visited": sorted(list(visited)), "current": None, "action": "done"})
    return steps

def bfs_steps(graph, start):
    visited = set()
    queue = [start]
    steps = []
    while queue:
        node = queue.pop(0)
        steps.append({"visited": sorted(list(visited)), "current": node, "action": "visit"})
        if node not in visited:
            visited.add(node)
            queue.extend(graph.get(node, []))
    steps.append({"visited": sorted(list(visited)), "current": None, "action": "done"})
    return steps