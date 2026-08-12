/**
 * MathMate — Core Application Logic
 */

// Application State
const state = {
  activeTab: 'dashboard',
  currentSolution: null,
  savedSolutions: JSON.parse(localStorage.getItem('mathmate_saved') || '[]'),
  history: JSON.parse(localStorage.getItem('mathmate_history') || '[]'),
  stats: JSON.parse(localStorage.getItem('mathmate_stats') || '{"solved": 0, "quizScore": 85}'),
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  updateStatsUI();
  renderSavedList();
  initArgandCanvas();
});

// Tab Navigation
function initTabs() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      switchTab(target);
    });
  });
}

function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tabId));
  document.querySelectorAll('.tab-view').forEach(v => v.classList.toggle('active', v.id === `tab-${tabId}`));
}

function updateStatsUI() {
  document.querySelectorAll('.stat-solved').forEach(el => el.textContent = state.stats.solved);
  document.querySelectorAll('.stat-saved').forEach(el => el.textContent = state.savedSolutions.length);
  document.querySelectorAll('.stat-score').forEach(el => el.textContent = `${state.stats.quizScore}%`);
}

function fillQuestion(text) {
  switchTab('solver');
  const textarea = document.getElementById('question-input');
  if (textarea) {
    textarea.value = text;
    textarea.focus();
  }
}

// Toast Helper
function showToast(msg) {
  const existing = document.querySelector('.toast-msg');
  if (existing) existing.remove();
  
  const toast = document.createElement('div');
  toast.className = 'toast-msg';
  toast.innerHTML = `✨ ${msg}`;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2500);
}

// Core Math Solver Handler
async function solveQuestion() {
  const inputEl = document.getElementById('question-input');
  const question = inputEl.value.trim();
  const solutionPage = document.getElementById('solution-page');

  if (!question) {
    showToast('Please enter a math question first!');
    return;
  }

  solutionPage.style.display = 'block';
  solutionPage.innerHTML = '<div class="glass-card"><span class="topic-badge">🧮 Solving Math Problem...</span></div>';

  try {
    const res = await fetch('/api/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    const data = await res.json();

    if (!data.ok) {
      solutionPage.innerHTML = `
        <div class="glass-card" style="border-color: var(--accent-rose);">
          <h3 style="color: var(--accent-rose);">⚠️ Calculation Error</h3>
          <p style="margin-top: 0.5rem;">${data.error || 'Could not process this question.'}</p>
        </div>`;
      return;
    }

    state.currentSolution = {
      id: `MM-${Math.random().toString(36).substr(2, 6).toUpperCase()}`,
      question,
      data,
      timestamp: new Date().toLocaleString(),
    };

    // Update Stats & History
    state.stats.solved += 1;
    localStorage.setItem('mathmate_stats', JSON.stringify(state.stats));
    state.history.unshift(state.currentSolution);
    if (state.history.length > 50) state.history.pop();
    localStorage.setItem('mathmate_history', JSON.stringify(state.history));
    updateStatsUI();

    renderSolutionPage(state.currentSolution);
  } catch (err) {
    solutionPage.innerHTML = `<div class="glass-card" style="color:var(--accent-rose)">Network error: ${err.message}</div>`;
  }
}

// Solution Page Rendering
function renderSolutionPage(solutionItem) {
  const data = solutionItem.data;
  const page = document.getElementById('solution-page');

  let stepsHtml = '';
  (data.explanation || []).forEach((step, idx) => {
    stepsHtml += `<div class="step-card">${formatLaTeXText(step)}</div>`;
  });

  let bonusHtml = '';
  if (data.bonus_bezout) {
    bonusHtml = `<div class="step-card" style="border-color:var(--accent-purple)">
      <strong>Bézout's Identity:</strong> ${formatLaTeXText(data.bonus_bezout.equation)}
    </div>`;
  }

  page.innerHTML = `
    <div class="glass-card" id="printable-solution">
      <div class="solution-header">
        <div>
          <span class="topic-badge">${data.topic_label || 'Math Solution'}</span>
          <h2 style="margin-top:0.5rem; font-family:'Outfit';">${escapeHtml(solutionItem.question)}</h2>
        </div>
        <div class="action-bar">
          <button class="btn-secondary" onclick="copyText()"><i class="far fa-copy"></i> Copy</button>
          <button class="btn-secondary" onclick="copyLaTeX()"><i class="fas fa-code"></i> LaTeX</button>
          <button class="btn-secondary" onclick="openEditModal()"><i class="far fa-edit"></i> Edit</button>
          <button class="btn-secondary" onclick="saveSolution()"><i class="far fa-bookmark"></i> Save</button>
          <button class="btn-secondary" onclick="shareSolution()"><i class="fas fa-share-alt"></i> Share</button>
          <button class="btn-primary" onclick="downloadPDF()"><i class="fas fa-file-pdf"></i> Download PDF</button>
        </div>
      </div>

      <h4 style="color:var(--text-muted); margin-bottom:0.75rem;">Step-by-Step Derivation:</h4>
      ${stepsHtml}
      ${bonusHtml}

      <div class="final-answer-box">
        Final Answer: ${formatLaTeXText(data.answer)}
      </div>
    </div>
  `;

  // Render KaTeX if available
  if (window.renderMathInElement) {
    renderMathInElement(page, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false},
        {left: '\\(', right: '\\)', display: false},
        {left: '\\[', right: '\\]', display: true}
      ]
    });
  }
}

// LaTeX and Math Text Formatting Helper
function formatLaTeXText(text) {
  if (!text) return '';
  // Convert standard math symbols to clean display strings if KaTeX not active
  return escapeHtml(text)
    .replace(/\\times|×/g, '×')
    .replace(/\\sqrt/g, '√')
    .replace(/\\theta/g, 'θ');
}

function escapeHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Action Handlers
function copyText() {
  if (!state.currentSolution) return;
  const data = state.currentSolution.data;
  const text = `Question: ${state.currentSolution.question}\n\nSteps:\n${(data.explanation || []).join('\n')}\n\nAnswer: ${data.answer}`;
  navigator.clipboard.writeText(text);
  showToast('Copied solution to clipboard!');
}

function copyLaTeX() {
  if (!state.currentSolution) return;
  const data = state.currentSolution.data;
  const latex = `\\begin{equation}\n  \\text{Question: } ${state.currentSolution.question}\n  \\quad \\Rightarrow \\quad ${data.answer}\n\\end{equation}`;
  navigator.clipboard.writeText(latex);
  showToast('Copied LaTeX formula to clipboard!');
}

function saveSolution() {
  if (!state.currentSolution) return;
  const exists = state.savedSolutions.some(item => item.id === state.currentSolution.id);
  if (!exists) {
    state.savedSolutions.unshift(state.currentSolution);
    localStorage.setItem('mathmate_saved', JSON.stringify(state.savedSolutions));
    updateStatsUI();
    renderSavedList();
    showToast('Saved solution to your library!');
  } else {
    showToast('Solution is already saved!');
  }
}

function shareSolution() {
  if (!state.currentSolution) return;
  const shareUrl = `${window.location.origin}/#${state.currentSolution.id}`;
  navigator.clipboard.writeText(shareUrl);
  showToast(`Share Link Generated: ${state.currentSolution.id} (Copied link)`);
}

function downloadPDF() {
  window.print();
}

function openEditModal() {
  if (!state.currentSolution) return;
  const modal = document.getElementById('edit-modal');
  const textarea = document.getElementById('edit-steps-input');
  textarea.value = (state.currentSolution.data.explanation || []).join('\n');
  modal.classList.add('active');
}

function closeEditModal() {
  document.getElementById('edit-modal').classList.remove('active');
}

function saveEditedSolution() {
  const newSteps = document.getElementById('edit-steps-input').value.split('\n').filter(s => s.trim());
  if (state.currentSolution) {
    state.currentSolution.data.explanation = newSteps;
    renderSolutionPage(state.currentSolution);
    closeEditModal();
    showToast('Updated solution steps!');
  }
}

function renderSavedList() {
  const listEl = document.getElementById('saved-list');
  if (!listEl) return;

  if (state.savedSolutions.length === 0) {
    listEl.innerHTML = '<p style="color:var(--text-muted)">No saved solutions yet. Click "Save" on any solution page!</p>';
    return;
  }

  listEl.innerHTML = state.savedSolutions.map((item, idx) => `
    <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <span class="topic-badge">${item.data.topic_label || 'Math'}</span>
        <h4 style="margin-top:0.3rem;">${escapeHtml(item.question)}</h4>
        <small style="color:var(--text-muted)">Saved on ${item.timestamp}</small>
      </div>
      <div>
        <button class="btn-secondary" onclick="viewSavedItem(${idx})">Open</button>
        <button class="btn-secondary" onclick="removeSavedItem(${idx})" style="color:var(--accent-rose)"><i class="far fa-trash-alt"></i></button>
      </div>
    </div>
  `).join('');
}

function viewSavedItem(idx) {
  state.currentSolution = state.savedSolutions[idx];
  switchTab('solver');
  renderSolutionPage(state.currentSolution);
}

function removeSavedItem(idx) {
  state.savedSolutions.splice(idx, 1);
  localStorage.setItem('mathmate_saved', JSON.stringify(state.savedSolutions));
  updateStatsUI();
  renderSavedList();
  showToast('Removed from saved items.');
}

// Argand Plane Complex Visualizer for Complex Lab
function initArgandCanvas() {
  const canvas = document.getElementById('argand-canvas');
  if (!canvas) return;
  drawArgandPlane(3, 4);
}

function updateArgandFromInputs() {
  const r = parseFloat(document.getElementById('argand-real').value) || 0;
  const i = parseFloat(document.getElementById('argand-imag').value) || 0;
  drawArgandPlane(r, i);
}

function drawArgandPlane(real, imag) {
  const canvas = document.getElementById('argand-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  const cx = w / 2;
  const cy = h / 2;
  const scale = 25;

  ctx.clearRect(0, 0, w, h);

  // Draw Grid & Axes
  ctx.strokeStyle = '#1e293b';
  ctx.lineWidth = 1;
  for (let x = 0; x < w; x += scale) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
  }
  for (let y = 0; y < h; y += scale) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
  }

  // Axes
  ctx.strokeStyle = '#475569';
  ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(w, cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, h); ctx.stroke();

  // Target Vector
  const px = cx + real * scale;
  const py = cy - imag * scale;

  // Circle Modulus
  const radius = Math.hypot(real, imag) * scale;
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
  ctx.stroke();

  // Vector Line
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(px, py);
  ctx.stroke();

  // Point Dot
  ctx.fillStyle = '#a855f7';
  ctx.beginPath();
  ctx.arc(px, py, 6, 0, 2 * Math.PI);
  ctx.fill();

  // Text Label
  ctx.fillStyle = '#f1f5f9';
  ctx.font = '12px Inter';
  ctx.fillText(`z = ${real} + ${imag}i`, px + 8, py - 8);
}
