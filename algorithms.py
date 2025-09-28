# algorithms.py

# ------------------ Sorting ------------------
def bubble_sort_steps(arr):
    arr = arr[:]
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            steps.append({"array": list(arr), "highlight": [j, j+1], "action": "compare"})
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append({"array": list(arr), "highlight": [j, j+1], "action": "swap"})
    steps.append({"array": list(arr), "highlight": [], "action": "done"})
    return arr, steps


def merge_sort_steps(arr):
    steps = []

    def merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a)//2
        left = merge_sort(a[:mid])
        right = merge_sort(a[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            steps.append({"array": merged + left[i:] + right[j:], "action": "merge"})
        merged += left[i:] + right[j:]
        return merged

    merge_sort(arr[:])
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
    steps = []
    for op in ops:
        parts = op.strip().split()
        if parts[0].lower() == "enqueue" and len(parts) > 1:
            val = parts[1]
            queue.append(val)
            steps.append({"queue": list(queue), "action": "enqueue", "value": val})
        elif parts[0].lower() == "dequeue":
            val = queue.pop(0) if queue else None
            steps.append({"queue": list(queue), "action": "dequeue", "value": val})
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
