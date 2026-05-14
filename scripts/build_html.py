#!/usr/bin/env python3
"""Build the quiz HTML file with embedded question data."""
import json
import html

with open("plans/quiz/questions.json") as f:
    data = json.load(f)

# Escape for embedding in JS - we'll use JSON.parse on a string
cmpe260_json = json.dumps(data["cmpe260"])
cmpe256_json = json.dumps(data["cmpe256"])

html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CMPE Exam Quiz</title>
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$','$'],['\\(','\\)']],
    displayMath: [['$$','$$'],['\\[','\\]']]
  },
  startup: {
    ready: () => {
      MathJax.startup.defaultReady();
      window.mathJaxReady = true;
    }
  }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
<style>
:root {
  --bg: #ffffff;
  --bg2: #f5f5f7;
  --bg3: #e8e8ed;
  --text: #1d1d1f;
  --text2: #6e6e73;
  --accent: #0071e3;
  --accent-hover: #0077ed;
  --correct: #34c759;
  --correct-bg: #d4f5dd;
  --wrong: #ff3b30;
  --wrong-bg: #fdd;
  --border: #d2d2d7;
  --card-bg: #ffffff;
  --card-shadow: 0 2px 12px rgba(0,0,0,0.08);
  --radius: 12px;
}
[data-theme="dark"] {
  --bg: #1c1c1e;
  --bg2: #2c2c2e;
  --bg3: #3a3a3c;
  --text: #f5f5f7;
  --text2: #98989d;
  --accent: #0a84ff;
  --accent-hover: #409cff;
  --correct: #30d158;
  --correct-bg: #1a3a24;
  --wrong: #ff453a;
  --wrong-bg: #3a1a1a;
  --border: #48484a;
  --card-bg: #2c2c2e;
  --card-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
  transition: background 0.3s, color 0.3s;
}
.container {
  max-width: 720px;
  margin: 0 auto;
  padding: 20px;
}
/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  margin-bottom: 20px;
}
.header h1 {
  font-size: 1.4rem;
  font-weight: 700;
}
.theme-toggle {
  background: var(--bg3);
  border: none;
  border-radius: 20px;
  padding: 6px 14px;
  cursor: pointer;
  font-size: 1.1rem;
  color: var(--text);
  transition: background 0.2s;
}
.theme-toggle:hover { background: var(--border); }

/* Progress bar */
.progress-container {
  background: var(--bg3);
  border-radius: 8px;
  height: 8px;
  margin-bottom: 8px;
  overflow: hidden;
}
.progress-bar {
  height: 100%;
  background: var(--accent);
  border-radius: 8px;
  transition: width 0.4s ease;
  width: 0%;
}
.progress-text {
  font-size: 0.85rem;
  color: var(--text2);
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

/* Cards */
.card {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--card-shadow);
  padding: 28px;
  margin-bottom: 20px;
  border: 1px solid var(--border);
}

/* Course selection */
.course-select { text-align: center; padding: 40px 20px; }
.course-select h2 { font-size: 1.8rem; margin-bottom: 8px; }
.course-select p { color: var(--text2); margin-bottom: 32px; font-size: 1.05rem; }
.course-btn {
  display: block;
  width: 100%;
  padding: 18px 24px;
  margin-bottom: 14px;
  background: var(--bg2);
  border: 2px solid var(--border);
  border-radius: var(--radius);
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}
.course-btn:hover {
  border-color: var(--accent);
  background: var(--bg3);
  transform: translateY(-1px);
}
.course-btn .course-code { color: var(--accent); }
.course-btn .course-desc {
  display: block;
  font-size: 0.85rem;
  font-weight: 400;
  color: var(--text2);
  margin-top: 4px;
}

/* Mode selection */
.mode-select { text-align: center; }
.mode-select h2 { font-size: 1.4rem; margin-bottom: 6px; }
.mode-select .subtitle { color: var(--text2); margin-bottom: 24px; }
.mode-btn {
  display: block;
  width: 100%;
  padding: 16px 20px;
  margin-bottom: 10px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.mode-btn:hover { background: var(--accent-hover); transform: translateY(-1px); }
.mode-btn.secondary {
  background: var(--bg2);
  color: var(--text);
  border: 2px solid var(--border);
}
.mode-btn.secondary:hover { border-color: var(--accent); }
.back-link {
  display: inline-block;
  margin-top: 16px;
  color: var(--accent);
  cursor: pointer;
  font-size: 0.9rem;
  border: none;
  background: none;
  text-decoration: underline;
}

/* Question */
.q-tier {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  margin-bottom: 12px;
  background: var(--bg3);
  color: var(--text2);
}
.q-number {
  font-size: 0.9rem;
  color: var(--text2);
  margin-bottom: 6px;
}
.q-text {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 20px;
  line-height: 1.5;
  white-space: pre-wrap;
}
.q-text .MathJax { font-size: 1em !important; }

/* Options */
.option-btn {
  display: block;
  width: 100%;
  padding: 14px 18px;
  margin-bottom: 10px;
  background: var(--bg2);
  border: 2px solid var(--border);
  border-radius: 10px;
  font-size: 0.95rem;
  color: var(--text);
  cursor: pointer;
  text-align: left;
  transition: all 0.15s;
  line-height: 1.5;
}
.option-btn:hover:not(.disabled) {
  border-color: var(--accent);
  background: var(--bg3);
}
.option-btn.disabled { cursor: default; opacity: 0.85; }
.option-btn.correct {
  border-color: var(--correct) !important;
  background: var(--correct-bg) !important;
  opacity: 1 !important;
}
.option-btn.wrong {
  border-color: var(--wrong) !important;
  background: var(--wrong-bg) !important;
  opacity: 1 !important;
}
.option-letter {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  border-radius: 50%;
  background: var(--bg3);
  font-weight: 700;
  font-size: 0.85rem;
  margin-right: 12px;
  flex-shrink: 0;
}
.option-btn.correct .option-letter { background: var(--correct); color: #fff; }
.option-btn.wrong .option-letter { background: var(--wrong); color: #fff; }
.option-content { display: flex; align-items: flex-start; }
.option-text { flex: 1; }

/* Feedback */
.feedback {
  margin-top: 16px;
  padding: 16px;
  border-radius: 10px;
  font-size: 0.95rem;
  display: none;
}
.feedback.correct-fb {
  background: var(--correct-bg);
  border: 1px solid var(--correct);
}
.feedback.wrong-fb {
  background: var(--wrong-bg);
  border: 1px solid var(--wrong);
}
.feedback .fb-title {
  font-weight: 700;
  font-size: 1.05rem;
  margin-bottom: 8px;
}
.feedback .fb-explanation {
  color: var(--text);
  line-height: 1.6;
}

/* Next button */
.next-btn {
  display: none;
  width: 100%;
  padding: 14px;
  margin-top: 16px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.next-btn:hover { background: var(--accent-hover); }

/* Summary */
.summary { text-align: center; }
.summary h2 { font-size: 1.6rem; margin-bottom: 8px; }
.score-display {
  font-size: 3rem;
  font-weight: 800;
  color: var(--accent);
  margin: 16px 0;
}
.score-pct {
  font-size: 1.2rem;
  color: var(--text2);
  margin-bottom: 24px;
}
.score-bar-container {
  background: var(--bg3);
  border-radius: 10px;
  height: 14px;
  margin-bottom: 28px;
  overflow: hidden;
}
.score-bar {
  height: 100%;
  border-radius: 10px;
  transition: width 1s ease;
}
.summary-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
}
.summary-actions button {
  flex: 1;
  padding: 14px;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}
.restart-btn { background: var(--accent); color: #fff; }
.restart-btn:hover { background: var(--accent-hover); }
.switch-btn { background: var(--bg2); color: var(--text); border: 2px solid var(--border) !important; }
.switch-btn:hover { border-color: var(--accent) !important; }

/* Review list */
.review-list { text-align: left; }
.review-item {
  padding: 14px;
  border-radius: 10px;
  margin-bottom: 8px;
  background: var(--bg2);
  border: 1px solid var(--border);
}
.review-item.review-correct { border-left: 4px solid var(--correct); }
.review-item.review-wrong { border-left: 4px solid var(--wrong); }
.review-q {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 4px;
}
.review-detail {
  font-size: 0.85rem;
  color: var(--text2);
  line-height: 1.5;
}
.review-detail strong { color: var(--text); }
.review-filter {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  justify-content: center;
}
.filter-btn {
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg2);
  color: var(--text);
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
}
.filter-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

/* Responsive */
@media (max-width: 600px) {
  .container { padding: 12px; }
  .card { padding: 18px; }
  .course-select h2 { font-size: 1.4rem; }
  .q-text { font-size: 1rem; }
  .option-btn { padding: 12px 14px; font-size: 0.9rem; }
  .summary-actions { flex-direction: column; }
  .score-display { font-size: 2.4rem; }
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.3s ease; }

/* Hide screens */
.screen { display: none; }
.screen.active { display: block; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
</head>
<body>
<div class="container">
  <!-- Header -->
  <div class="header">
    <h1>📝 CMPE Quiz</h1>
    <button class="theme-toggle" onclick="toggleTheme()" title="Toggle dark/light mode">🌙</button>
  </div>

  <!-- Screen 1: Course Selection -->
  <div id="screen-course" class="screen active">
    <div class="card course-select fade-in">
      <h2>Choose Your Course</h2>
      <p>Select a course to start practicing</p>
      <button class="course-btn" onclick="selectCourse('cmpe260')">
        <span class="course-code">CMPE 260</span> — Reinforcement Learning
        <span class="course-desc">100 questions · Modules 9–17 · TRPO, PPO, DDPG, SAC, A3C & more</span>
      </button>
      <button class="course-btn" onclick="selectCourse('cmpe256')">
        <span class="course-code">CMPE 256</span> — Recommender Systems
        <span class="course-desc">100 questions · CF, MF, Deep Learning, Fairness, Bandits & more</span>
      </button>
    </div>
  </div>

  <!-- Screen 2: Mode Selection -->
  <div id="screen-mode" class="screen">
    <div class="card mode-select fade-in">
      <h2 id="mode-title"></h2>
      <p class="subtitle" id="mode-subtitle"></p>
      <button class="mode-btn" onclick="startQuiz(100)">📋 All 100 Questions (Shuffled)</button>
      <button class="mode-btn secondary" onclick="startQuiz(25)">⚡ Quick 25 (Random)</button>
      <button class="mode-btn secondary" onclick="startQuiz(10)">🎯 Quick 10 (Random)</button>
      <button class="back-link" onclick="showScreen('screen-course')">← Back to course selection</button>
    </div>
  </div>

  <!-- Screen 3: Quiz -->
  <div id="screen-quiz" class="screen">
    <div class="progress-container">
      <div class="progress-bar" id="progress-bar"></div>
    </div>
    <div class="progress-text">
      <span id="progress-label">Question 1 of 100</span>
      <span id="score-label">Score: 0/0</span>
    </div>
    <div class="card fade-in" id="question-card">
      <span class="q-tier" id="q-tier"></span>
      <div class="q-number" id="q-number"></div>
      <div class="q-text" id="q-text"></div>
      <div id="options-container"></div>
      <div class="feedback" id="feedback">
        <div class="fb-title" id="fb-title"></div>
        <div class="fb-explanation" id="fb-explanation"></div>
      </div>
      <button class="next-btn" id="next-btn" onclick="nextQuestion()">Next Question →</button>
    </div>
  </div>

  <!-- Screen 4: Summary -->
  <div id="screen-summary" class="screen">
    <div class="card summary fade-in">
      <h2>Quiz Complete! 🎉</h2>
      <div class="score-display" id="final-score"></div>
      <div class="score-pct" id="final-pct"></div>
      <div class="score-bar-container">
        <div class="score-bar" id="score-bar"></div>
      </div>
      <div class="summary-actions">
        <button class="restart-btn" onclick="restartQuiz()">🔄 Restart</button>
        <button class="switch-btn" onclick="showScreen('screen-course')">📚 Switch Course</button>
      </div>
      <div class="review-filter">
        <button class="filter-btn active" data-filter="all" onclick="filterReview('all', this)">All</button>
        <button class="filter-btn" data-filter="wrong" onclick="filterReview('wrong', this)">❌ Wrong Only</button>
        <button class="filter-btn" data-filter="correct" onclick="filterReview('correct', this)">✅ Correct Only</button>
      </div>
      <div class="review-list" id="review-list"></div>
    </div>
  </div>
</div>

<script>
// ===== QUESTION DATA =====
const QUESTIONS = {
  cmpe260: ''' + cmpe260_json + ''',
  cmpe256: ''' + cmpe256_json + '''
};

// ===== STATE =====
let state = {
  course: null,
  questions: [],
  currentIndex: 0,
  score: 0,
  answered: 0,
  answers: [], // {qIndex, selected, correct, isCorrect}
  theme: localStorage.getItem('quiz-theme') || 'light'
};

// ===== THEME =====
function initTheme() {
  if (state.theme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    document.querySelector('.theme-toggle').textContent = '☀️';
  }
}
function toggleTheme() {
  state.theme = state.theme === 'light' ? 'dark' : 'light';
  localStorage.setItem('quiz-theme', state.theme);
  if (state.theme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    document.querySelector('.theme-toggle').textContent = '☀️';
  } else {
    document.documentElement.removeAttribute('data-theme');
    document.querySelector('.theme-toggle').textContent = '🌙';
  }
}

// ===== NAVIGATION =====
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

// ===== COURSE SELECTION =====
function selectCourse(course) {
  state.course = course;
  const titles = {
    cmpe260: 'CMPE 260 — Reinforcement Learning',
    cmpe256: 'CMPE 256 — Recommender Systems'
  };
  document.getElementById('mode-title').textContent = titles[course];
  document.getElementById('mode-subtitle').textContent = '100 questions available';
  showScreen('screen-mode');
}

// ===== SHUFFLE =====
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ===== START QUIZ =====
function startQuiz(count) {
  const allQ = QUESTIONS[state.course];
  const shuffled = shuffle(allQ);
  state.questions = shuffled.slice(0, Math.min(count, shuffled.length));
  state.currentIndex = 0;
  state.score = 0;
  state.answered = 0;
  state.answers = [];
  showScreen('screen-quiz');
  renderQuestion();
}

// ===== RENDER QUESTION =====
function renderQuestion() {
  const q = state.questions[state.currentIndex];
  const total = state.questions.length;
  const idx = state.currentIndex;

  // Progress
  document.getElementById('progress-bar').style.width = ((idx / total) * 100) + '%';
  document.getElementById('progress-label').textContent = `Question ${idx + 1} of ${total}`;
  document.getElementById('score-label').textContent = `Score: ${state.score}/${state.answered}`;

  // Question
  document.getElementById('q-tier').textContent = q.tier;
  document.getElementById('q-number').textContent = `Q${q.num}`;
  document.getElementById('q-text').innerHTML = escapeHtml(q.question).replace(/\n/g, '<br>');

  // Options
  const container = document.getElementById('options-container');
  container.innerHTML = '';
  ['A', 'B', 'C', 'D'].forEach(letter => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.innerHTML = `<div class="option-content"><span class="option-letter">${letter}</span><span class="option-text">${escapeHtml(q.options[letter])}</span></div>`;
    btn.onclick = () => selectAnswer(letter);
    btn.dataset.letter = letter;
    container.appendChild(btn);
  });

  // Reset feedback
  const fb = document.getElementById('feedback');
  fb.style.display = 'none';
  fb.className = 'feedback';
  document.getElementById('next-btn').style.display = 'none';

  // Re-render MathJax
  typesetMath();
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function typesetMath() {
  if (window.MathJax && MathJax.typesetPromise) {
    MathJax.typesetPromise().catch(err => console.log('MathJax error:', err));
  }
}

// ===== SELECT ANSWER =====
function selectAnswer(selected) {
  const q = state.questions[state.currentIndex];
  const correct = q.answer;
  const isCorrect = selected === correct;

  state.answered++;
  if (isCorrect) state.score++;

  state.answers.push({
    qIndex: state.currentIndex,
    question: q,
    selected,
    correct,
    isCorrect
  });

  // Disable all options
  const btns = document.querySelectorAll('.option-btn');
  btns.forEach(btn => {
    btn.classList.add('disabled');
    btn.onclick = null;
    const letter = btn.dataset.letter;
    if (letter === correct) btn.classList.add('correct');
    if (letter === selected && !isCorrect) btn.classList.add('wrong');
  });

  // Show feedback
  const fb = document.getElementById('feedback');
  fb.style.display = 'block';
  if (isCorrect) {
    fb.className = 'feedback correct-fb';
    document.getElementById('fb-title').textContent = '✅ Correct!';
  } else {
    fb.className = 'feedback wrong-fb';
    document.getElementById('fb-title').textContent = `❌ Wrong — Correct answer is ${correct}`;
  }
  document.getElementById('fb-explanation').innerHTML = escapeHtml(q.explanation);

  // Update score display
  document.getElementById('score-label').textContent = `Score: ${state.score}/${state.answered}`;

  // Show next button
  const nextBtn = document.getElementById('next-btn');
  if (state.currentIndex < state.questions.length - 1) {
    nextBtn.textContent = 'Next Question →';
  } else {
    nextBtn.textContent = 'View Results →';
  }
  nextBtn.style.display = 'block';

  typesetMath();
}

// ===== NEXT QUESTION =====
function nextQuestion() {
  state.currentIndex++;
  if (state.currentIndex >= state.questions.length) {
    showSummary();
  } else {
    renderQuestion();
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// ===== SUMMARY =====
function showSummary() {
  showScreen('screen-summary');
  const total = state.questions.length;
  const pct = Math.round((state.score / total) * 100);

  document.getElementById('final-score').textContent = `${state.score} / ${total}`;
  document.getElementById('final-pct').textContent = `${pct}% correct`;

  const bar = document.getElementById('score-bar');
  bar.style.width = '0%';
  bar.style.background = pct >= 70 ? 'var(--correct)' : pct >= 50 ? '#ff9f0a' : 'var(--wrong)';
  setTimeout(() => { bar.style.width = pct + '%'; }, 100);

  renderReviewList('all');
}

function renderReviewList(filter) {
  const list = document.getElementById('review-list');
  list.innerHTML = '';

  state.answers.forEach((a, i) => {
    if (filter === 'wrong' && a.isCorrect) return;
    if (filter === 'correct' && !a.isCorrect) return;

    const item = document.createElement('div');
    item.className = `review-item ${a.isCorrect ? 'review-correct' : 'review-wrong'}`;

    let detail = '';
    if (!a.isCorrect) {
      detail = `<div class="review-detail">
        Your answer: <strong>${a.selected}) ${escapeHtml(a.question.options[a.selected])}</strong><br>
        Correct: <strong>${a.correct}) ${escapeHtml(a.question.options[a.correct])}</strong><br>
        <em>${escapeHtml(a.question.explanation)}</em>
      </div>`;
    } else {
      detail = `<div class="review-detail">✅ Answered: ${a.correct}</div>`;
    }

    item.innerHTML = `
      <div class="review-q">${a.isCorrect ? '✅' : '❌'} Q${a.question.num}. ${escapeHtml(a.question.question).substring(0, 120)}${a.question.question.length > 120 ? '...' : ''}</div>
      ${detail}
    `;
    list.appendChild(item);
  });

  typesetMath();
}

function filterReview(filter, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderReviewList(filter);
}

// ===== RESTART =====
function restartQuiz() {
  startQuiz(state.questions.length);
}

// ===== INIT =====
initTheme();
</script>
</body>
</html>'''

# Write the HTML file
with open("plans/quiz/index.html", "w") as f:
    f.write(html_content)

print(f"Generated index.html ({len(html_content)} bytes)")
print(f"CMPE 260: {len(data['cmpe260'])} questions embedded")
print(f"CMPE 256: {len(data['cmpe256'])} questions embedded")
