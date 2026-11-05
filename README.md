# CareSooner — Early Health Concern Explainer

**DSH Hacks V2 — AI × Healthcare · By Umar Shareef (solo)**
**Deadline: Nov 14, 2026, 11:45pm PST · Winners: Nov 23, 2026 · Devpost draft ID 1270897 (NOT submitted)**

> **General information only. This tool does not diagnose, treat, or replace a clinician.**
> If a red-flag concern applies, seek emergency care now.

## The idea in one sentence

CareSooner turns a confusing health concern into plain-language general
information, a red-flag safety check, and a printable visit-prep note —
so people reach real care sooner, with better questions.

It covers two DSH theme directions at once: **Faster care** (clear next
steps + a note you can take to an appointment) and **Early detection**
(a dated change tracker that makes a repeating or worsening pattern
visible). It deliberately does **not** claim the third direction
(diagnostic tool): it names no cause and makes no diagnosis.

## How it works

1. **Choose a concern (up to 3)** — 8 topics: chest discomfort, breathing
   difficulty, fever, headache, stomach/abdominal pain, a new or changing
   skin mark, tiredness/low energy, low mood or stress.
2. **Red-flag safety check** — 10-item checklist. Any ticked red flag puts
   emergency safety information first, before anything else. No ticked box
   does *not* rule anything out — the app says so explicitly.
3. **Change tracker** — dated observations stored **in the visitor's own
   browser only** (localStorage). Nothing is sent to the server unless the
   user presses "Generate visit note", and even then the note is built
   once and not stored.
4. **Visit-prep note** — plain text from the selections + tracker entries:
   concerns, duration, pattern, red flags, and questions for a clinician.
   Copy it or print it and take it to an appointment.

## Why the "AI" here is honest

The engine is a **transparent rule set (R1–R6)**, shown in the app as a
visible trace for every result. There is no machine-learning model, no
external API, and no black-box score — and the app never pretends
otherwise. That is a deliberate safety choice for health information:
a judge (or a user) can read exactly why each section was shown.

## Run it locally

```bash
cd ~/workspace/dsh-hacks
python3 src/server.py
# open http://localhost:8004/
# PORT env var overrides the port (hosting uses $PORT)
```

No install step, no database, no API keys. Python 3.12 standard library
only + plain HTML/CSS/JavaScript.

## Tests

```bash
cd ~/workspace/dsh-hacks
python3 -m unittest discover -s tests -v
```

11 tests, all passing at last run (2026-10-29). They cover red-flag
priority, the worsening-pattern path, the routine path, empty input,
unknown topic/flag rejection, duration/pattern validation, topic
completeness (8 topics, 10 red flags), and — most importantly — a ban
on diagnosis wording ("you have …", "you likely have", "diagnosis is")
in every topic summary, priority text, disclaimer, and visit note.

Server smoke test (also run 2026-10-29): `/api/health` OK,
`/api/topics` returned 8 topics + 10 red flags, a red-flag explain call
returned `seek-emergency-care-now` with trace R1 first, and an unknown
topic correctly returned a 400 error. Home page served HTML.

## What is real, and what is not

- **Real:** the working prototype, the rule engine, the tracker, the
  visit-note generator, the tests, the one-page PDF in `docs/`.
- **Labelled demo only:** the "Try the labelled demo example" button
  pre-fills fever / a few days / getting worse / no red flags. It is
  explicitly labelled as a demo, not a real person.
- **Not claimed:** no patients, no statistics, no user counts, no
  clinical validation, no accuracy numbers. None exist in this repo,
  and none are invented for the submission.
- **Not done yet:** demo video (user records a real screen capture),
  public GitHub repo push, Devpost submission (needs Umar's final
  approval), live hosted demo URL.

## Safety limits (also stated in the app)

- General information only; not a diagnosis, treatment recommendation,
  or replacement for a clinician or emergency care.
- Not validated on patients or medical records.
- English only for now; no local emergency numbers are listed, to avoid
  inventing one — the app says to contact local emergency services.
- If anything here conflicts with a clinician's advice, the clinician
  wins.

## Files

```
src/explainer.py      Rule engine + topics + red flags + visit notes
src/server.py         Stdlib HTTP server, stateless, /api/health|topics|explain|visit-note
src/make_pdf.py       Stdlib-only one-page PDF generator
public/index.html     Full UI (concerns, red flags, tracker, visit note)
tests/test_explainer.py  11 safety + logic tests
docs/project-description.pdf   One-page description (for Devpost file upload)
docs/DEVPOST-DRAFT.md  Name, pitch, and About text ready to paste
docs/DEMO-SCRIPT.md    Timed script for the user-recorded demo video
docs/SUBMISSION-CHECKLIST.md   What is done vs. what remains
Dockerfile            Python 3.12-slim, stdlib only, honours $PORT
```

## Licence

MIT — see `LICENSE`.
