# Interactive Mathematics Lab — v0.1 (GCD topic working end-to-end)

## What's working right now
- `POST /api/solve` — detects topic by keyword, and if it's a GCD/Euclidean
  Algorithm question, returns a full step-by-step solution (division trace
  + Bézout coefficients as a bonus).
- `public/index.html` — a minimal frontend that calls `/api/solve` and
  renders the steps.
- The other 5 topics are detected but return a "coming soon" placeholder —
  this keeps the API response shape stable while we build them out next.

## Project structure
```
mathlab/
├── api/
│   └── solve.py           <- Vercel serverless function (POST /api/solve)
├── index.html             <- static frontend
├── requirements.txt
└── README.md
```

Note: Vercel treats `.py` files as serverless entrypoints. The entrypoint handler is configured in `pyproject.toml` under `[tool.vercel]`: `entrypoint = "api.solve:handler"`. Shared helper modules should be placed in a root `/lib` directory rather than directly inside `api/`.

## Deploying to Vercel

1. Push this folder to a GitHub repo (or run from the CLI directly).
2. Install the Vercel CLI if you don't have it: `npm i -g vercel`
3. From inside the `mathlab/` folder: `vercel` (then `vercel --prod` once
   you're happy with the preview).
4. Vercel automatically uses `pyproject.toml` to configure `api.solve:handler` as the Python serverless entrypoint.

No environment variables or database are needed yet — this version has no
storage, history, or accounts.

## Testing locally without deploying
```bash
cd api
python3 -c "
from _topic_detector import detect_topic, extract_integers
from _gcd_solver import solve_gcd_question
q = 'Find gcd(252, 105) using the Euclidean algorithm'
topic, label, conf = detect_topic(q)
nums = extract_integers(q)
print(solve_gcd_question(nums[0], nums[1]))
"
```
(Vercel's local dev server, `vercel dev`, will also run the actual HTTP
endpoint if you want to test the real request/response cycle.)

## Known limitation: OCR
The app summary mentions scanning questions from a photo. Tesseract OCR
needs a system binary that Vercel's Python serverless runtime does not
provide — `pip install pytesseract` alone will NOT work there. Options
for later:
- Bundle a static-linked tesseract binary (fragile, adds complexity)
- Use a cloud OCR API (Google Cloud Vision, AWS Textract, or a vision-
  capable LLM API) called from the serverless function instead
- Run OCR on a separate always-on server (Render/Railway/a small VM)
  and have Vercel call that server

## Next steps (in order)
1. Add the remaining 5 topic solvers (`_complex_solver.py`,
   `_demoivre_solver.py`, `_permcomb_solver.py`, `_functions_solver.py`,
   `_limits_solver.py`) following the same pattern as `_gcd_solver.py`,
   and wire each into `solve.py`.
2. Add image upload + OCR endpoint (`api/ocr.py`) — decide OCR approach
   from the list above before building.
3. Add persistence: Vercel KV or a Postgres DB (e.g. Supabase, Neon) for
   save/history/share-by-link. Serverless functions are stateless, so
   this can't be done with just local files.
4. Add PDF/DOCX/image export (`reportlab` for PDF, `python-docx` for
   DOCX — both pure Python, no system binaries needed, so these DO work
   fine on Vercel).
5. Add visualizations/calculators/quizzes as additional frontend pages
   and, where math is involved, additional `/api/` endpoints.
