let currentQuestions = [];

function loadQuiz() {
  const select = document.getElementById("quiz-algo");
  const algorithm = select.value;
  const container = document.getElementById("quiz-area");

  if (!algorithm) {
    container.innerHTML = "<p>Please select an algorithm to start the quiz.</p>";
    return;
  }

  container.innerHTML = `<p>Loading quiz for <strong>${algorithm}</strong>...</p>`;

  fetch(`/quiz-data?algorithm=${encodeURIComponent(algorithm)}`)
    .then(response => {
      if (!response.ok) throw new Error("Network response was not ok");
      return response.json();
    })
    .then(questions => {
      if (!questions.length) {
        container.innerHTML = "<p>No questions available for this algorithm.</p>";
        return;
      }

      currentQuestions = questions;
      container.innerHTML = "";

      questions.forEach((q, i) => {
        const questionDiv = document.createElement("div");
        questionDiv.classList.add("quiz-question", "mb-3");
        questionDiv.innerHTML = `
          <p><strong>Q${i + 1}:</strong> ${q.question}</p>
        `;

        if (q.options && q.options.length) {
          const optionsList = document.createElement("ul");
          optionsList.classList.add("list-unstyled");
          q.options.forEach(opt => {
            const li = document.createElement("li");
            li.innerHTML = `
              <label>
                <input type="radio" name="q${i}" value="${opt}"> ${opt}
              </label>
            `;
            optionsList.appendChild(li);
          });
          questionDiv.appendChild(optionsList);
        }

        container.appendChild(questionDiv);
      });

      // Add Submit Button
      const submitBtn = document.createElement("button");
      submitBtn.textContent = "Submit Quiz";
      submitBtn.classList.add("btn", "btn-primary", "mt-3");
      submitBtn.onclick = submitQuiz;
      container.appendChild(submitBtn);
    })
    .catch(error => {
      container.innerHTML = "<p>Failed to load quiz questions.</p>";
      console.error("Quiz load error:", error);
    });
}

function submitQuiz() {
  let score = 0;
  let total = currentQuestions.length;

  for (let i = 0; i < total; i++) {
    const q = currentQuestions[i];
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    if (selected && q.answer && selected.value === q.answer) {
      score++;
    }
  }

  const container = document.getElementById("quiz-area");
  container.innerHTML = `<h3>Your Score: ${score} / ${total}</h3>`;
}
