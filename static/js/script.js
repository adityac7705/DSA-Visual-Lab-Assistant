const arrayInput = document.getElementById('arrayInput');
const targetInput = document.getElementById('targetInput');
const visualizeBtn = document.getElementById('visualizeBtn');
const resetBtn = document.getElementById('resetBtn'); 

const searchTargetLabel = document.getElementById('searchTargetLabel');
const arrayContainer = document.getElementById('arrayContainer');
const searchCursor = document.getElementById('searchCursor');
const arrowSvgContainer = document.getElementById('arrowSvgContainer');
const resultMessage = document.getElementById('resultMessage');
const loadingIndicator = document.getElementById('loadingIndicator');

let animationDelay = 800;

document.addEventListener('DOMContentLoaded', initializeVisualization);

visualizeBtn.addEventListener('click', visualizeLinearSearch);
resetBtn.addEventListener('click', initializeVisualization);

function initializeVisualization() {
    arrayContainer.innerHTML = '';
    arrayContainer.appendChild(searchCursor);
    arrowSvgContainer.innerHTML = `
        <defs>
            <marker id="arrowhead" viewBox="0 0 10 10" refX="5" refY="5"
                markerWidth="6" markerHeight="6" orient="auto">
                <path d="M 0 0 L 10 5 L 0 10 z" />
            </marker>
        </defs>
    `;
    arrayContainer.appendChild(arrowSvgContainer);

    arrayInput.value = '';
    targetInput.value = '';

    resultMessage.textContent = 'Enter an array and a target to visualize.';
    resultMessage.className = 'text-info'; 
    loadingIndicator.style.display = 'none'; 
    searchTargetLabel.textContent = ''; 
    searchCursor.classList.remove('active'); 
}

function renderArray(arr) {
    const existingElements = arrayContainer.querySelectorAll('.array-element');
    existingElements.forEach(el => el.remove());

    arr.forEach((num, index) => {
        const elementDiv = document.createElement('div');
        elementDiv.classList.add('array-element', 'unseen'); 
        elementDiv.dataset.index = index;
        elementDiv.innerHTML = `
            <span class="element-value">${num}</span>
            <span class="element-index">idx ${index}</span>
        `;
        arrayContainer.insertBefore(elementDiv, searchCursor);
    });
}

function drawArrow(startX, startY, endX, endY, elementId) {
    const midX = (startX + endX) / 2;
    const controlPointY = startY - 1;

    const pathData = `M${startX},${startY} C${midX},${controlPointY} ${midX},${controlPointY} ${endX},${endY}`;

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData);
    path.setAttribute("class", "arrow-path current-arrow"); 
    path.setAttribute("id", elementId);
    path.setAttribute("marker-end", `url(#arrowhead)`);

    const length = path.getTotalLength();
    path.style.strokeDasharray = length;
    path.style.strokeDashoffset = length;
    void path.offsetWidth;
    path.style.strokeDashoffset = "0";

    arrowSvgContainer.appendChild(path);
}

async function visualizeLinearSearch() {
    const arrayString = arrayInput.value;
    const targetString = targetInput.value;

    if (!arrayString || !targetString) {
        alert('Please enter both array and target values.'); 
        return;
    }
    const array = arrayString.split(',').map(num => parseInt(num.trim(), 10)).filter(Number.isFinite);
    const target = parseInt(targetString.trim(), 10);

    if (array.length === 0 || isNaN(target)) {
        alert('Invalid array or target input. Use comma-separated numbers.'); 
        return;
    }

    initializeVisualization();
    
    renderArray(array); 

    loadingIndicator.style.display = 'block'; 
    visualizeBtn.disabled = true; 
    searchTargetLabel.textContent = `Search for '${target}' in [${array.join(', ')}]`;

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                algorithm: 'linear_search',
                array: array,
                target: target
            }),
        });

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const errorText = await response.text(); 
            console.error('Server response was not JSON:', errorText);
            resultMessage.textContent = 'Server returned unexpected format. Expected JSON. Check console.';
            resultMessage.classList.remove('text-info');
            resultMessage.classList.add('text-error');
            loadingIndicator.style.display = 'none';
            throw new Error('Server returned unexpected format. Expected JSON. Please ensure your Flask backend is running and the /process endpoint is correctly configured to return JSON. Check your browser\'s console for the server\'s full response (likely an HTML error page).');
        }
        
        const data = await response.json(); 

        if (!response.ok) {
            resultMessage.textContent = data.error || `HTTP Error: ${response.status} ${response.statusText}`;
            resultMessage.classList.remove('text-info');
            resultMessage.classList.add('text-error');
            loadingIndicator.style.display = 'none';
            throw new Error(data.error || `HTTP Error: ${response.status} ${response.statusText}`);
        }

        const steps = data.result;

        if (!Array.isArray(steps) || steps.length === 0) {
            resultMessage.textContent = 'Backend did not return valid steps for visualization.';
            resultMessage.classList.remove('text-info');
            resultMessage.classList.add('text-error');
            loadingIndicator.style.display = 'none';
            return;
        }
        loadingIndicator.style.display = 'none';
        searchCursor.classList.add('active'); 
        let prevElementRect = null; 
        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            const currentElement = arrayContainer.querySelector(`[data-index="${step.index}"]`);
            const prevArrow = arrowSvgContainer.querySelector('.current-arrow');
            if (prevArrow) {
                prevArrow.remove();
            }
            if (currentElement) {
                arrayContainer.querySelectorAll('.array-element').forEach(el => {
                    el.classList.remove('found'); 
                });
                for (let j = 0; j <= step.index; j++) {
                    const elementToReveal = arrayContainer.querySelector(`[data-index="${j}"]`);
                    if (elementToReveal) {
                        elementToReveal.classList.remove('unseen');
                        elementToReveal.style.opacity = '1';
                        elementToReveal.style.filter = 'none'; 
                        elementToReveal.style.transform = 'scale(1)'; 
                    }
                }
                const currentElementRect = currentElement.getBoundingClientRect();
                const containerRect = arrayContainer.getBoundingClientRect(); 
                const cursorTargetX = (currentElementRect.left + currentElementRect.width / 2) - containerRect.left;
                searchCursor.style.left = `${cursorTargetX}px`;
                let arrowStartX_relative, arrowEndX_relative;
                const arrowVerticalCenterY = (currentElementRect.top + currentElementRect.height / 2) - containerRect.top;

                if (i === 0) {
                    const firstElementLeftEdge_relative = currentElementRect.left - containerRect.left;
                    arrowStartX_relative = firstElementLeftEdge_relative - 10; 
                    arrowEndX_relative = firstElementLeftEdge_relative + (currentElementRect.width * 0.2); 
                } else {
                    arrowStartX_relative = prevElementRect.left + prevElementRect.width; 
                    arrowEndX_relative = currentElementRect.left - containerRect.left; 
                }
                if (step.status === 'checking') {
                    if (step.value === target) {
                        resultMessage.textContent = `Checking index ${step.index} (Value: ${step.value})... It's a match! `;
                    } else {
                        resultMessage.textContent = `Checking index ${step.index} (Value: ${step.value})... Not a match. Moving on.`;
                    }
                    resultMessage.className = 'text-info';
                    drawArrow(arrowStartX_relative, arrowVerticalCenterY, arrowEndX_relative, arrowVerticalCenterY, 'current-arrow');

                } else if (step.status === 'found') {
                    await new Promise(resolve => setTimeout(resolve, animationDelay / 2)); 

                    currentElement.classList.add('found');
                    resultMessage.textContent = `Target ${target} found at index ${step.index}! `;
                    resultMessage.className = 'text-success';
                    searchCursor.classList.remove('active'); 
                    const finalArrow = arrowSvgContainer.querySelector('.current-arrow');
                    if (finalArrow) {
                        finalArrow.remove();
                    }
                    break; 
                } else if (step.status === 'not_found' && step.final) {
                    await new Promise(resolve => setTimeout(resolve, animationDelay / 2)); 

                    arrayContainer.querySelectorAll('.array-element').forEach(el => {
                        el.classList.remove('found');
                    });
                    resultMessage.textContent = `Target ${target} not found in the array. `;
                    resultMessage.className = 'text-error';
                    searchCursor.classList.remove('active'); 
                    const finalArrow = arrowSvgContainer.querySelector('.current-arrow');
                    if (finalArrow) {
                        finalArrow.remove();
                    }
                }
                prevElementRect = {
                    left: currentElementRect.left - containerRect.left,
                    width: currentElementRect.width,
                    top: currentElementRect.top - containerRect.top
                };
            }
            if (!step.final) {
                await new Promise(resolve => setTimeout(resolve, animationDelay));
            }
        }
    } catch (error) {
        console.error('Error during visualization:', error);
        resultMessage.textContent = `Error: ${error.message}. Check console.`;
        resultMessage.className = 'text-error';
        loadingIndicator.style.display = 'none';
        searchCursor.classList.remove('active');
    } finally {
        visualizeBtn.disabled = false; 
    }
}