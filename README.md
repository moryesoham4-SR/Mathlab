# MathMate — Your Smart Mathematics Companion 🚀

**MathMate** is an interactive, AI-free mathematical learning and problem-solving application built with Python serverless functions, KaTeX typesetting, and a modern dark glassmorphism web interface.

---

## 🧮 6 Core Mathematical Engines

All 6 math solvers run in pure Python without external paid APIs, providing 100% deterministic, step-by-step derivations:

1. **Euclidean Algorithm & GCD (`lib/solver_gcd.py`)**: Division algorithm traces, quotient/remainder steps, and Bézout identity linear combinations (\(ax + by = \gcd\)).
2. **Complex Numbers & Polar Form (`lib/solver_complex.py`)**: Complex arithmetic (\(z_1 \times z_2\), \(z_1 / z_2\)), modulus \(|z|\), principal argument \(\operatorname{Arg}(z)\), and Cartesian-to-polar conversions (\(r \operatorname{cis} \theta\)).
3. **De Moivre's Theorem & N-th Roots (`lib/solver_demoivre.py`)**: Powers \(z^n\) and De Moivre \(n\)-th roots \(z_k = \sqrt[n]{r} \operatorname{cis}\left(\frac{\theta + 2k\pi}{n}\right)\) evenly distributed on the unit circle.
4. **Permutations & Combinations (`lib/solver_permcomb.py`)**: Factorials \(n!\), permutations \(P(n, r)\), combinations \(C(n, r)\), and multiset anagram arrangements (\(\frac{n!}{n_1! n_2! \dots}\)).
5. **Injective, Surjective & Bijective Functions (`lib/solver_functions.py`)**: Step-by-step mathematical proofs testing Injectivity (One-to-One), Surjectivity (Onto), and Bijectivity classification.
6. **Limits & Continuity (`lib/solver_limits.py`)**: Limits at infinity (\(\lim_{x \to \infty}\)), trigonometric limits (\(\lim_{x \to 0} \frac{\sin x}{x}\)), and \(\frac{0}{0}\) indeterminate rational limits via algebraic factoring.

---

## 🌟 Key Application Features

- **Dashboard**: Quick progress stats (Questions Solved, Practice Score %, Saved Solutions) and shortcut launchers.
- **Step-by-Step Solver UI**: Multi-modal input tabs (`⌨️ Type`, `📋 Paste`, `📷 Scan`), topic auto-detection rules, and KaTeX math typesetting.
- **Solution Action Toolbar**:
  - **Copy**: Copy plain text or raw LaTeX markup (`\gcd(252, 105) = 21`).
  - **Edit**: Interactive modal allowing users to customize step notes before saving.
  - **Save & Share**: Saved solution manager with local storage persistence and share link generator.
  - **Download PDF**: Print-optimized PDF document generation.
- **6 Interactive Math Labs**: Dedicated calculators and live **SVG Argand Plane vector visualizer** for complex numbers.
- **Learn Center**: Structured definitions, formulas, and worked examples for all topics.
- **Algorithmic Practice & Quiz Engine**: Programmatically generates random math problems with instant answer validation and score summaries.
- **Formula Library**: Searchable formula reference sheet with one-click "Try in Calculator" buttons.

---

## 📁 Project Structure

```
mathmate/
├── api/
│   └── solve.py              <- Main Vercel serverless function entrypoint
├── lib/
│   ├── __init__.py           <- Python package initializer
│   ├── solver_gcd.py         <- GCD & Euclidean algorithm engine
│   ├── solver_complex.py     <- Complex numbers & polar converter
│   ├── solver_demoivre.py    <- De Moivre powers & nth roots
│   ├── solver_permcomb.py    <- Permutations, combinations & anagrams
│   ├── solver_functions.py   <- Injectivity / Surjectivity prover
│   ├── solver_limits.py      <- Limits & indeterminate forms solver
│   └── validators.py        <- Input bounds & error validation
├── static/
│   ├── css/
│   │   └── style.css         <- Modern dark glassmorphism design system
│   └── js/
│       ├── app.js            <- Core SPA application & solution renderer
│       └── practice.js       <- Algorithmic practice & quiz engine
├── index.html                <- Self-contained MathMate Single Page Application
├── test_solvers.py           <- Automated test suite across all 6 topics
├── pyproject.toml            <- Vercel Python runtime entrypoint config
├── vercel.json               <- Vercel routing & rewrite settings
└── README.md
```

---

## 🚀 Deploying to Vercel

1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Update MathMate documentation and core engines"
   git push origin main
   ```
2. Vercel automatically detects `pyproject.toml` (`[tool.vercel] entrypoint = "api.solve:handler"`) and builds the Python serverless function.
3. Open `https://<your-app-name>.vercel.app/` to access your live MathMate web application!

---

## 🧪 Local Testing

Run the automated test suite locally:
```bash
python test_solvers.py
```
This executes 15 test cases across all 6 mathematical topics to verify derivations and answer formatting.
