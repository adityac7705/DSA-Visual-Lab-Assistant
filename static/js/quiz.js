// Elements
const quizAlgoSelect = document.getElementById('quiz-algo');
const startQuizBtn = document.getElementById('start-quiz-btn');
const quizContainerDiv = document.getElementById('quiz-container');
const submitBtn = document.getElementById('submit-quiz-btn');
const quizSelectionArea = document.getElementById('quiz-selection-area');
const resultsPage = document.getElementById('results-page');

let quizData = {};
let currentQuizTopic = null;
const userAnswers = {};
const MAX_QUESTIONS = 5;

// Shuffle array helper
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Show alert message
function showMessage(message, isError = false) {
    alert(message); // Using original alert to avoid touching design
}

// Start quiz
startQuizBtn.addEventListener('click', async () => {
    const topic = quizAlgoSelect.value;
    if (!topic) {
        showMessage("Please select an algorithm to start the quiz!");
        return;
    }

    try {
        const response = await fetch(`/quiz-data?algorithm=${topic}`);
        if (!response.ok) throw new Error('Network response was not ok');

        const allQuestions = await response.json();
        if (!allQuestions.length) {
            showMessage(`No questions found for ${topic}.`);
            return;
        }

        shuffleArray(allQuestions);
        quizData[topic] = allQuestions.slice(0, MAX_QUESTIONS);
        loadQuiz(topic);
    } catch (err) {
        console.error(err);
        showMessage("Failed to load quiz data. Ensure backend is running.", true);
    }
});

function loadQuiz(topic) {
    currentQuizTopic = topic;
    userAnswers[topic] = {};

    const questions = quizData[topic];
    quizContainerDiv.innerHTML = '';
    quizSelectionArea.classList.add('hidden');
    quizContainerDiv.classList.remove('hidden');
    submitBtn.classList.remove('hidden');

    questions.forEach((q, index) => {
        const card = document.createElement('div');
        card.className = 'card-wrapper';

        const shuffledOptions = shuffleArray([...q.options]);

        card.innerHTML = `
            <div class="animate-flip" data-question-index="${index}">
                <div class="card-face front quiz-card-bg">
                    <h5 class="text-3xl font-bold text-center z-10">Question ${index + 1}</h5>
                </div>
                <div class="card-face back quiz-card-bg" style="transform: rotateY(180deg); padding:1.5rem;">
                    <h5 class="text-lg font-semibold mb-4">${q.question}</h5>
                    <div class="space-y-3">
                        ${shuffledOptions.map(opt => `<button class="w-full py-2 rounded-full bg-gray-800 text-white border border-gray-700 hover:bg-cyan-700 transition-colors" data-answer="${opt}" data-index="${index}">${opt}</button>`).join('')}
                    </div>
                </div>
            </div>
        `;

        quizContainerDiv.appendChild(card);

        // Handle option click
        card.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation(); // Prevent parent click from flipping

                const selectedOption = e.target.dataset.answer;
                const questionIndex = e.target.dataset.index;
                const parentCard = e.target.closest('.animate-flip');

                if (userAnswers[currentQuizTopic][questionIndex] !== undefined) return;

                userAnswers[currentQuizTopic][questionIndex] = selectedOption;

                // Disable all buttons
                parentCard.querySelectorAll('button').forEach(b => b.disabled = true);

                const correctAnswer = quizData[currentQuizTopic][questionIndex].answer;

                // Highlight selected answer
                e.target.classList.remove('bg-gray-800', 'hover:bg-cyan-700');
                e.target.classList.add(selectedOption === correctAnswer ? 'bg-green-600' : 'bg-red-600');

                // Highlight correct answer if wrong
                if (selectedOption !== correctAnswer) {
                    const correctBtn = Array.from(parentCard.querySelectorAll('button')).find(b => b.dataset.answer === correctAnswer);
                    if (correctBtn) {
                        correctBtn.classList.remove('bg-gray-800');
                        correctBtn.classList.add('bg-green-600');
                    }
                }

                // Flip card once
                if (!parentCard.classList.contains('is-flipped')) {
                    parentCard.classList.add('is-flipped');
                }
            });
        });
    });
}

// Submit quiz
submitBtn.addEventListener('click', () => {
    const questions = quizData[currentQuizTopic];
    let score = 0;
    questions.forEach((q, i) => {
        if (userAnswers[currentQuizTopic][i] === q.answer) score++;
    });

    document.getElementById('score-display').textContent = `${score}/${questions.length}`;
    quizContainerDiv.classList.add('hidden');
    submitBtn.classList.add('hidden');
    resultsPage.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
