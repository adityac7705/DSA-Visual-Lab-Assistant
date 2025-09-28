document.getElementById("algo-select").addEventListener("change", function() {
    const algo = this.value;
    const area = document.getElementById("input-area");
    const vizArea = document.getElementById("visualization-area");

    if (["bubble", "quick", "linear", "binary", "bst"].includes(algo)) {
        area.innerHTML = 'Array (comma-separated): <input id="arr-input" type="text" value="5,3,8,4,2"/>';
        vizArea.innerHTML = "";
        if (["linear", "binary"].includes(algo)) {
            area.innerHTML += ' Target: <input id="target-input" type="number" value="4"/>';
        }
        enableVisualizeButton(true);
    }
    else if (algo === "merge") {
        area.innerHTML = 'Array (comma-separated): <input id="arr-input" type="text" value="6,5,12,10,9,1"/>';
        vizArea.innerHTML = "";
        enableVisualizeButton(true);
    }
    else if (algo === "stack") {
        area.innerHTML = `
            <input id="stack-value-input" type="number" placeholder="Enter value" />
            <button id="stack-push-btn" class="btn btn-primary btn-sm ms-2">Push</button>
            <button id="stack-pop-btn" class="btn btn-danger btn-sm ms-2">Pop</button>
            <button id="stack-reset-btn" class="btn btn-secondary btn-sm ms-2">Reset</button>
        `;
        vizArea.innerHTML = "";
        setupLiveStackVisualization();
        enableVisualizeButton(false);
    }
    else if (algo === "queue") {
        area.innerHTML = `
            <input id="queue-value-input" type="number" placeholder="Enter value" />
            <button id="queue-enqueue-btn" class="btn btn-primary btn-sm ms-2">Enqueue</button>
            <button id="queue-dequeue-btn" class="btn btn-danger btn-sm ms-2">Dequeue</button>
            <button id="queue-reset-btn" class="btn btn-secondary btn-sm ms-2">Reset</button>
        `;
        vizArea.innerHTML = "";
        setupLiveQueueVisualization();
        enableVisualizeButton(false);
    }
    else if (["dfs", "bfs"].includes(algo)) {
        area.innerHTML = `Graph JSON (e.g. {"A":["B","C"],"B":["D"],"C":[]}): <input id="graph-input" type="text" value='{"A":["B","C"],"B":["D"],"C":[],"D":[]}'/>
                          Start Node: <input id="start-input" type="text" value="A"/>`;
        vizArea.innerHTML = "";
        enableVisualizeButton(true);
    }
    else {
        area.innerHTML = '';
        vizArea.innerHTML = '';
        enableVisualizeButton(true);
    }
});

function enableVisualizeButton(enable) {
    const btn = document.querySelector("button.btn-success");
    if (btn) btn.disabled = !enable;
}

function setupLiveStackVisualization() {
    const pushBtn = document.getElementById("stack-push-btn");
    const popBtn = document.getElementById("stack-pop-btn");
    const resetBtn = document.getElementById("stack-reset-btn");
    const input = document.getElementById("stack-value-input");
    const vizArea = document.getElementById("visualization-area");

    let stack = [];

    pushBtn.onclick = () => {
        const val = input.value.trim();
        if (val === '') return alert("Enter value to push");
        stack.push(parseInt(val));
        input.value = '';
        renderStack(vizArea, {stack: stack, action: 'push', value: val});
    };

    popBtn.onclick = () => {
        if (stack.length === 0) return alert("Stack is empty!");
        const val = stack.pop();
        renderStack(vizArea, {stack: stack, action: 'pop', value: val});
    };

    resetBtn.onclick = () => {
        stack = [];
        vizArea.innerHTML = "";
    };
}

function setupLiveQueueVisualization() {
    const enqueueBtn = document.getElementById("queue-enqueue-btn");
    const dequeueBtn = document.getElementById("queue-dequeue-btn");
    const resetBtn = document.getElementById("queue-reset-btn");
    const input = document.getElementById("queue-value-input");
    const vizArea = document.getElementById("visualization-area");

    let queue = [];

    enqueueBtn.onclick = () => {
        const val = input.value.trim();
        if (val === '') return alert("Enter value to enqueue");
        queue.push(parseInt(val));
        input.value = '';
        renderQueue(vizArea, {queue: queue, action: 'enqueue', value: val});
    };

    dequeueBtn.onclick = () => {
        if (queue.length === 0) return alert("Queue is empty!");
        const val = queue.shift();
        renderQueue(vizArea, {queue: queue, action: 'dequeue', value: val});
    };

    resetBtn.onclick = () => {
        queue = [];
        vizArea.innerHTML = "";
    };
}

function runAlgorithm() {
    const algo = document.getElementById("algo-select").value;
    let arr = [], target, ops = [], graph = {}, start;
    if (document.getElementById("arr-input"))
        arr = document.getElementById("arr-input").value.split(",").map(x => parseInt(x));
    if (document.getElementById("target-input"))
        target = parseInt(document.getElementById("target-input").value);
    if (algo === "stack")
        ops = window['stackOps'] || [];
    else if (algo === "queue")
        ops = window['queueOps'] || [];
    else if (document.getElementById("ops-input"))
        ops = document.getElementById("ops-input").value.split(",");
    if (document.getElementById("graph-input"))
        try { graph = JSON.parse(document.getElementById("graph-input").value); } catch (e) { graph = {}; }
    if (document.getElementById("start-input"))
        start = document.getElementById("start-input").value;

    fetch("/run-algo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algo, arr, target, ops, graph, start })
    })
        .then(res => res.json())
        .then(data => {
            if (algo === "merge") {
                renderMergeSortTree(document.getElementById("visualization-area"), data.steps);
            } else {
                visualizeSteps(algo, data.steps);
            }
        });
}

function visualizeSteps(algo, steps) {
    const area = document.getElementById("visualization-area");
    area.innerHTML = "";

    if (["bubble", "quick", "linear", "binary", "bst"].includes(algo)) {
        let i = 0;
        function show() {
            if (i >= steps.length) return;
            const step = steps[i];
            renderArrayBoxes(area, step.array, step.highlight, step.action, step.target);
            i++;
            setTimeout(show, 700);
        }
        show();
    }
    else if (algo === "stack") {
        let i = 0;
        function show() {
            if (i >= steps.length) return;
            renderStack(area, steps[i]);
            i++;
            setTimeout(show, 700);
        }
        show();
    }
    else if (algo === "queue") {
        let i = 0;
        function show() {
            if (i >= steps.length) return;
            renderQueue(area, steps[i]);
            i++;
            setTimeout(show, 700);
        }
        show();
    }
    else if (algo === "bst") {
        let i = 0;
        function show() {
            if (i >= steps.length) return;
            renderBST(area, steps[i]);
            i++;
            setTimeout(show, 700);
        }
        show();
    }
    else if (["dfs", "bfs"].includes(algo)) {
        let i = 0;
        function show() {
            if (i >= steps.length) return;
            renderGraphVisit(area, steps[i]);
            i++;
            setTimeout(show, 700);
        }
        show();
    }
    else {
        area.innerHTML = "<em>Visualization not implemented for this algorithm.</em>";
    }
}

// Build and render merge sort tree recursively
function buildMergeSortTree(steps) {
    let nodes = {};
    steps.forEach(step => nodes[step.id] = step);
    let root = steps.find(step => step.parent === null);

    function buildNode(step) {
        let nodeDiv = document.createElement("div");
        nodeDiv.style.display = "flex";
        nodeDiv.style.flexDirection = "column";
        nodeDiv.style.alignItems = "center";
        nodeDiv.style.margin = "12px";

        // Array display box
        let arrDiv = document.createElement("div");
        arrDiv.textContent = step.array.join(" ");
        arrDiv.style.border = "2px solid #0d6efd";
        arrDiv.style.backgroundColor = "#e7f1ff";
        arrDiv.style.padding = "8px";
        arrDiv.style.borderRadius = "6px";
        arrDiv.style.fontWeight = "bold";
        nodeDiv.appendChild(arrDiv);

        // Recursive children in horizontal flex container
        if (step.children && step.children.length > 0) {
            let childrenDiv = document.createElement("div");
            childrenDiv.style.display = "flex";
            childrenDiv.style.justifyContent = "center";
            childrenDiv.style.gap = "24px";
            step.children.forEach(childId => {
                childrenDiv.appendChild(buildNode(nodes[childId]));
            });
            nodeDiv.appendChild(childrenDiv);
        }
        return nodeDiv;
    }
    return buildNode(root);
}

function renderMergeSortTree(container, steps) {
    container.innerHTML = "";
    let treeDiv = buildMergeSortTree(steps);
    container.appendChild(treeDiv);
}

function renderArrayBoxes(container, arr, highlightIndices = [], action = "", target = null) {
    container.innerHTML = "";
    arr.forEach((val, idx) => {
        const box = document.createElement("div");
        box.textContent = val;
        box.style.display = "inline-block";
        box.style.margin = "5px";
        box.style.padding = "15px 25px";
        box.style.border = "2px solid #0d6efd";
        box.style.borderRadius = "6px";
        box.style.fontSize = "1.2rem";
        box.style.backgroundColor = "#e7f1ff";
        box.style.transition = "background-color 0.4s ease";
        if (highlightIndices.includes(idx)) {
            if (action === "swap")
                box.style.backgroundColor = "#d6336c";
            else if (action === "compare")
                box.style.backgroundColor = "#f59e0b";
            else if (action === "found")
                box.style.backgroundColor = "#198754";
            box.style.color = "#fff";
            box.style.fontWeight = "bold";
        }
        container.appendChild(box);
    });
    if (action) {
        const desc = document.createElement("p");
        desc.style.marginTop = "10px";
        desc.style.fontWeight = "bold";
        if (action === "compare")
            desc.textContent = `Comparing indices ${highlightIndices.join(" and ")}`;
        else if (action === "swap")
            desc.textContent = `Swapping indices ${highlightIndices.join(" and ")}`;
        else if (action === "found")
            desc.textContent = `Found target value ${target} at index ${highlightIndices[0]}`;
        else if (action === "done")
            desc.textContent = "Operation complete!";
        container.appendChild(desc);
    }
}

function renderStack(container, step) {
    container.innerHTML = "<h5>Stack Operations: " + (step.action || "") + "</h5>";
    if (step.action === "push" || step.action === "pop") {
        const move = document.createElement("p");
        move.textContent = `Value: ${step.value}`;
        container.appendChild(move);
    }

    const stackDiv = document.createElement("div");
    stackDiv.style.display = "flex";
    stackDiv.style.flexDirection = "column-reverse";  // vertical stack with bottom as top
    stackDiv.style.justifyContent = "flex-start";
    stackDiv.style.alignItems = "center";
    stackDiv.style.border = "2px solid #0d6efd";
    stackDiv.style.borderRadius = "6px";
    stackDiv.style.padding = "10px";
    stackDiv.style.minHeight = "150px";
    stackDiv.style.width = "100px";
    stackDiv.style.margin = "auto";
    stackDiv.style.backgroundColor = "#f0f8ff";

    (step.stack || []).forEach(val => {
        const box = document.createElement("div");
        box.textContent = val;
        box.style.border = "2px solid #0d6efd";
        box.style.backgroundColor = "#e7f1ff";
        box.style.margin = "5px 0";
        box.style.padding = "10px 20px";
        box.style.borderRadius = "6px";
        box.style.fontWeight = "bold";
        box.style.width = "60px";
        box.style.textAlign = "center";
        stackDiv.appendChild(box);
    });

    container.appendChild(stackDiv);
}

function renderQueue(container, step) {
    container.innerHTML = "<h5>Queue Operations: " + (step.action || "") + "</h5>";
    if (step.action === "enqueue" || step.action === "dequeue") {
        const move = document.createElement("p");
        move.textContent = `Value: ${step.value}`;
        container.appendChild(move);
    }
    const queueDiv = document.createElement("div");
    queueDiv.style.display = "flex";
    queueDiv.style.justifyContent = "center";
    queueDiv.style.alignItems = "center";
    (step.queue || []).forEach(val => {
        const box = document.createElement("div");
        box.textContent = val;
        box.style.border = "2px solid #0d6efd";
        box.style.backgroundColor = "#e7f1ff";
        box.style.margin = "5px";
        box.style.padding = "15px 25px";
        box.style.borderRadius = "6px";
        box.style.fontWeight = "bold";
        queueDiv.appendChild(box);
    });
    container.appendChild(queueDiv);
}

function renderBST(container, step) {
    container.innerHTML = "<h5>BST In-Order Traversal</h5>";
    const bstArray = step.bst || [];
    const bstDiv = document.createElement("div");
    bstDiv.style.display = "flex";
    bstDiv.style.justifyContent = "center";
    bstDiv.style.alignItems = "center";
    bstDiv.style.flexWrap = "wrap";
    bstArray.forEach(val => {
        const box = document.createElement("div");
        box.textContent = val;
        box.style.border = "2px solid #0d6efd";
        box.style.backgroundColor = "#e7f1ff";
        box.style.margin = "5px";
        box.style.padding = "15px 25px";
        box.style.borderRadius = "6px";
        box.style.fontWeight = "bold";
        bstDiv.appendChild(box);
    });
    container.appendChild(bstDiv);
    if (step.action === "done") {
        const msg = document.createElement("p");
        msg.textContent = "BST build complete";
        msg.style.fontWeight = "bold";
        msg.style.marginTop = "10px";
        container.appendChild(msg);
    }
}

function renderGraphVisit(container, step) {
    container.innerHTML = `<h5>Current Node: ${step.current ?? "None"}</h5>`;
    const visitedDiv = document.createElement("div");
    visitedDiv.textContent = "Visited Nodes: " + (step.visited || []).join(", ");
    visitedDiv.style.padding = "10px";
    visitedDiv.style.backgroundColor = "#e7f1ff";
    visitedDiv.style.border = "2px solid #0d6efd";
    visitedDiv.style.borderRadius = "6px";
    container.appendChild(visitedDiv);
    if (step.action === "done") {
        const msg = document.createElement("p");
        msg.textContent = step.action.toUpperCase();
        msg.style.fontWeight = "bold";
        msg.style.marginTop = "10px";
        container.appendChild(msg);
    }
}
