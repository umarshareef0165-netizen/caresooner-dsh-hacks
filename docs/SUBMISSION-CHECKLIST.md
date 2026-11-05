# Submission checklist — CareSooner, DSH Hacks V2

Deadline: **Nov 14, 2026, 11:45pm PST** · Winners: Nov 23, 2026
Devpost draft: ID 1270897 ("Untitled", 1/5 steps) — **NOT submitted**

## Done

- [x] Working prototype: `src/server.py` + `public/index.html`, runs on http://localhost:8004/
- [x] 8 concern topics, 10-item red-flag check, browser-only tracker, visit-note generator
- [x] Visible rule trace (R1–R6) in every result
- [x] Tests: 11/11 pass (`python3 -m unittest discover -s tests -v`)
- [x] Server smoke test: health OK, topics OK, red-flag priority OK, bad input → 400
- [x] One-page project description PDF: `docs/project-description.pdf` (1 page, verified)
- [x] Devpost draft text: name 43/60 chars, pitch 199/200 chars (`docs/DEVPOST-DRAFT.md`)
- [x] Demo script, timed 2:30 (`docs/DEMO-SCRIPT.md`)
- [x] README with honest limits, Dockerfile, MIT LICENSE, .gitignore

## Still needed (in order)

1. **Deploy a live demo URL** — localhost does not qualify. Card-free host
   preferred (same rule as Qloo: if any host asks for a card, STOP and report).
   The `Dockerfile` honours `$PORT` and needs no env vars.
2. **Push the public repo** — verify no secrets first (there are none: no
   keys, no data files). Then paste the repo URL into the Devpost draft.
3. **Record the demo video** — user records a real screen capture per
   `docs/DEMO-SCRIPT.md`, uploads it publicly, link goes into the draft.
   Video demo link is required on the Devpost form.
4. **Thumbnail** — JPG/PNG/GIF, 5 MB max, 3:2 recommended (not yet made;
   take a clean screenshot of the home page with the disclaimer visible).
5. **File upload** — `docs/project-description.pdf` (required, 35 MB limit).
6. **Sponsor/special prize selection** — confirm eligibility before ticking
   Tin Computer Growth Plan / Best Research-Oriented Project (YRI).
7. **Final approval from Umar**, then submit the completed draft well
   before Nov 14, 11:45pm PST — never in the final hour.
8. **Date discrepancy note (from the registration report):** Devpost's
   separate Rules page lists different dates (submission to Nov 8,
   winners Nov 17) vs. the overview widget + dshhacks.org (Nov 14 /
   Nov 23). This checklist uses Nov 14 / Nov 23, but confirm with the
   hackathon manager on Devpost before submitting if that discrepancy
   is still live.

## Never do

- Never submit without Umar's final approval.
- Never claim a diagnosis, a patient result, a statistic, or a user count.
- Never enter a card on any host without his explicit decision for that item.
- Never use the "Paperwork Autopilot" project or any other hackathon's
  project for this submission.
