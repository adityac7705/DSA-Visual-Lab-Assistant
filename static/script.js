document.addEventListener("DOMContentLoaded", () => {
    const visualizeBtn = document.getElementById("visualizeBtn");
    const resetBtn = document.getElementById("resetBtn");
    const arrayInput = document.getElementById("arrayInput");
    const targetInput = document.getElementById("targetInput");
    const arrayContainer = document.getElementById("arrayContainer");
    const resultMessage = document.getElementById("resultMessage");
    const arrowSvg = document.getElementById("arrowSvgContainer");

    let array = [];
    let target = null;
    let currentIndex = 0;

    // ✅ Draw arrow between boxes
    function drawArrow(fromBox, toBox) {
        const svgNS = "http://www.w3.org/2000/svg";
        arrowSvg.innerHTML = ""; // clear previous arrows

        const startX = fromBox.offsetLeft + fromBox.offsetWidth / 2;
        const startY = fromBox.offsetTop - 5;
        const endX = toBox.offsetLeft + toBox.offsetWidth / 2;
        const endY = toBox.offsetTop - 5;

        const path = document.createElementNS(svgNS, "path");
        const midX = (startX + endX) / 2;
        const curveHeight = -50;
        const d = `M ${startX},${startY} Q ${midX},${curveHeight} ${endX},${endY}`;

        path.setAttribute("d", d);
        path.setAttribute("stroke", "#FBBF24"); // yellow
        path.setAttribute("stroke-width", "3");
        path.setAttribute("fill", "transparent");
        path.setAttribute("marker-end", "url(#arrowhead)");

        arrowSvg.appendChild(path);
    }

    // ✅ Create array boxes
    function createArrayBoxes(arr) {
        arrayContainer.innerHTML = "";
        arr.forEach((num, idx) => {
            const box = document.createElement("div");
            box.classList.add("array-box");
            box.setAttribute("id", "box-" + idx);
            box.textContent = num;
            arrayContainer.appendChild(box);
        });
    }

    // ✅ Visualization logic
    visualizeBtn.addEventListener("click", () => {
        const arrStr = arrayInput.value.trim();
        if (!arrStr) {
            resultMessage.textContent = "⚠️ Please enter an array!";
            return;
        }

        array = arrStr.split(",").map(x => parseInt(x.trim(), 10));
        target = parseInt(targetInput.value.trim(), 10);

        if (isNaN(target)) {
            resultMessage.textContent = "⚠️ Please enter a valid target!";
            return;
        }

        createArrayBoxes(array);
        arrowSvg.innerHTML = "";
        currentIndex = 0;
        resultMessage.textContent = `Searching for ${target}...`;

        function step() {
            if (currentIndex >= array.length) {
                resultMessage.textContent = `❌ Target ${target} not found!`;
                return;
            }

            let box = document.getElementById("box-" + currentIndex);
            box.classList.add("checking"); // highlight current

            if (array[currentIndex] === target) {
                box.classList.remove("checking");
                box.classList.add("found");
                resultMessage.textContent = `✅ Target ${target} found at index ${currentIndex}`;
                return;
            } else {
                if (currentIndex < array.length - 1) {
                    let nextBox = document.getElementById("box-" + (currentIndex + 1));
                    drawArrow(box, nextBox);
                }
                currentIndex++;
                setTimeout(step, 1200); // continue
            }
        }

        step();
    });

    // ✅ Reset
    resetBtn.addEventListener("click", () => {
        arrayContainer.innerHTML = "";
        arrowSvg.innerHTML = "";
        resultMessage.textContent = "Enter an array and target to visualize.";
    });
});
