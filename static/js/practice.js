/**
 * MathMate — Algorithmic Practice & Quiz Engine
 */

const quizState = {
  activeMode: 'mixed',
  questions: [],
  currentIndex: 0,
  score: 0,
  timerInterval: null,
  timeLeft: 60,
};

// Algorithmic Question Generator across 6 topics
function generateQuestion(topicKey = 'mixed') {
  const topics = ['gcd', 'complex', 'permcomb', 'limits', 'functions'];
  const selectedTopic = topicKey === 'mixed' ? topics[Math.floor(Math.random() * topics.length)] : topicKey;

  if (selectedTopic === 'gcd') {
    const a = (Math.floor(Math.random() * 20) + 5) * 7;
    const b = (Math.floor(Math.random() * 15) + 3) * 7;
    const gcd = (x, y) => (y === 0 ? x : gcd(y, x % y));
    const ans = gcd(a, b);
    return {
      topic: 'gcd',
      topicLabel: 'Euclidean Algorithm & GCD',
      question: `What is the greatest common divisor gcd(${a}, ${b})?`,
      correctAnswer: `${ans}`,
      options: shuffleOptions([`${ans}`, `${ans + 2}`, `${ans * 2}`, `${Math.max(1, ans - 3)}`]),
      explanation: `Repeatedly apply division: gcd(${a}, ${b}) = ${ans}.`,
    };
  }

  if (selectedTopic === 'complex') {
    const a = Math.floor(Math.random() * 5) + 1;
    const b = Math.floor(Math.random() * 5) + 1;
    const mod = Math.sqrt(a * a + b * b);
    const modStr = Number.isInteger(mod) ? `${mod}` : `√${a * a + b * b}`;
    return {
      topic: 'complex',
      topicLabel: 'Complex Numbers',
      question: `Find the modulus |z| of the complex number z = ${a} + ${b}i.`,
      correctAnswer: modStr,
      options: shuffleOptions([modStr, `${a + b}`, `√${a * a + b}`, `${a * b}`]),
      explanation: `Modulus r = √(a² + b²) = √(${a}² + ${b}²) = ${modStr}.`,
    };
  }

  if (selectedTopic === 'permcomb') {
    const n = Math.floor(Math.random() * 5) + 5; // 5 to 9
    const r = Math.floor(Math.random() * 3) + 2; // 2 to 4
    const fact = n => (n <= 1 ? 1 : n * fact(n - 1));
    const comb = (n, r) => fact(n) / (fact(r) * fact(n - r));
    const ans = comb(n, r);
    return {
      topic: 'permcomb',
      topicLabel: 'Permutations & Combinations',
      question: `Calculate the number of combinations C(${n}, ${r}).`,
      correctAnswer: `${ans}`,
      options: shuffleOptions([`${ans}`, `${ans + 10}`, `${ans * 2}`, `${fact(n) / fact(n - r)}`]),
      explanation: `C(${n}, ${r}) = ${n}! / [${r}! × (${n}-${r})!] = ${ans}.`,
    };
  }

  if (selectedTopic === 'limits') {
    const c = Math.floor(Math.random() * 5) + 1;
    const ans = 2 * c;
    return {
      topic: 'limits',
      topicLabel: 'Limits & Continuity',
      question: `Evaluate the limit: lim (x → ${c}) (x² - ${c * c}) / (x - ${c}).`,
      correctAnswer: `${ans}`,
      options: shuffleOptions([`${ans}`, `${c}`, `0`, `∞`]),
      explanation: `Factor numerator (x - ${c})(x + ${c}) / (x - ${c}) = x + ${c}. Substitute x = ${c} ⇒ ${ans}.`,
    };
  }

  // Functions default
  return {
    topic: 'functions',
    topicLabel: 'Functions & Bijectivity',
    question: `Is the function f(x) = 2x + 5 from R to R injective and surjective?`,
    correctAnswer: `Bijective (Both Injective and Surjective)`,
    options: shuffleOptions([
      `Bijective (Both Injective and Surjective)`,
      `Injective only`,
      `Surjective only`,
      `Neither Injective nor Surjective`
    ]),
    explanation: `f(x) is linear with non-zero slope (a=2), so it is both one-to-one (injective) and onto (surjective).`,
  };
}

function shuffleOptions(arr) {
  const set = Array.from(new Set(arr));
  return set.sort(() => Math.random() - 0.5);
}

// Start Quiz Session
function startQuiz(mode = 'mixed') {
  quizState.activeMode = mode;
  quizState.questions = Array.from({ length: 5 }, () => generateQuestion(mode));
  quizState.currentIndex = 0;
  quizState.score = 0;

  renderQuizQuestion();
}

function renderQuizQuestion() {
  const container = document.getElementById('quiz-container');
  if (!container) return;

  if (quizState.currentIndex >= quizState.questions.length) {
    renderQuizResults();
    return;
  }

  const q = quizState.questions[quizState.currentIndex];

  container.innerHTML = `
    <div class="quiz-box">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
        <span class="topic-badge">${q.topicLabel}</span>
        <span style="color:var(--text-muted)">Question ${quizState.currentIndex + 1} of ${quizState.questions.length}</span>
      </div>

      <h3 style="font-family:'Outfit'; margin-bottom:1.5rem;">${q.question}</h3>

      <div class="options-grid">
        ${q.options.map(opt => `
          <button class="option-btn" onclick="submitAnswer('${escapeJs(opt)}')">${escapeJs(opt)}</button>
        `).join('')}
      </div>

      <div id="quiz-feedback" style="margin-top:1.25rem; display:none;"></div>
    </div>
  `;
}

function escapeJs(str) {
  return String(str).replace(/'/g, "\\'");
}

function submitAnswer(selectedOpt) {
  const q = quizState.questions[quizState.currentIndex];
  const feedbackEl = document.getElementById('quiz-feedback');
  const isCorrect = selectedOpt === q.correctAnswer;

  if (isCorrect) {
    quizState.score += 1;
    feedbackEl.innerHTML = `
      <div style="color:var(--accent-emerald); font-weight:600; margin-bottom:0.5rem;">✓ Correct!</div>
      <p style="font-size:0.9rem; color:var(--text-sub);">${q.explanation}</p>
    `;
  } else {
    feedbackEl.innerHTML = `
      <div style="color:var(--accent-rose); font-weight:600; margin-bottom:0.5rem;">✗ Incorrect. Correct answer: ${q.correctAnswer}</div>
      <p style="font-size:0.9rem; color:var(--text-sub);">${q.explanation}</p>
    `;
  }

  feedbackEl.style.display = 'block';

  // Disable option buttons after selection
  document.querySelectorAll('.option-btn').forEach(btn => btn.disabled = true);

  setTimeout(() => {
    quizState.currentIndex += 1;
    renderQuizQuestion();
  }, 2200);
}

function renderQuizResults() {
  const container = document.getElementById('quiz-container');
  const pct = Math.round((quizState.score / quizState.questions.length) * 100);

  // Update App Stats
  state.stats.quizScore = pct;
  localStorage.setItem('mathmate_stats', JSON.stringify(state.stats));
  updateStatsUI();

  container.innerHTML = `
    <div class="quiz-box" style="text-align:center;">
      <div style="font-size:3rem; margin-bottom:0.5rem;">🏆</div>
      <h2 style="font-family:'Outfit';">Quiz Completed!</h2>
      <div style="font-size:2.5rem; font-weight:700; color:var(--accent-cyan); margin:1rem 0;">
        ${quizState.score} / ${quizState.questions.length} (${pct}%)
      </div>
      <p style="color:var(--text-muted); margin-bottom:1.5rem;">
        ${pct >= 80 ? 'Outstanding performance! You have mastered these concepts.' : 'Good effort! Review the Learn tab to boost your score.'}
      </p>

      <button class="btn-primary" onclick="startQuiz('${quizState.activeMode}')">Try Another Quiz</button>
    </div>
  `;
}
