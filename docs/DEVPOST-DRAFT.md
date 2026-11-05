# Devpost draft — CareSooner (for draft ID 1270897, NOT submitted)

## Project name (43 / 60 characters)

```
CareSooner - Early Health Concern Explainer
```

## Elevator pitch (199 / 200 characters)

```
CareSooner turns a confusing health concern into plain-language information, red-flag checks and a printable visit note, so people reach real care sooner. General information only, never a diagnosis.
```

## Try it out links (fill in at submit time — do NOT invent)

- Demo URL: [LIVE HOSTED URL — to be added after deployment; localhost does not qualify]
- Code: [PUBLIC GITHUB REPO URL — to be added after push; no repo pushed yet]
- Video: [PUBLIC VIDEO LINK — to be added after Umar records it]

## About the project

### Inspiration

When a health concern appears, most people do not know what to notice,
what counts as urgent, or what to ask a clinician — so care gets delayed
and a first appointment is spent reconstructing a pattern from memory.
CareSooner was built to close that gap before the appointment, not to
replace the appointment.

### What it does

CareSooner is a web app with four steps: (1) choose up to three concern
topics in plain language; (2) run a ten-item red-flag safety check, with
emergency information shown first if any red flag applies; (3) track
dated observations in the browser to spot a repeating or worsening
pattern early; (4) generate a printable visit-prep note with questions
for a clinician. It covers the Faster care and Early detection theme
directions, and deliberately does not claim to be a diagnostic tool.

### How I built it

Python standard library only on the server (no database, no API keys,
stateless by design), plain HTML/CSS/JavaScript on the front end. The
"AI" is a transparent rule set (R1–R6) shown to the user as a visible
trace for every result — no black-box model, no external API. The change
tracker uses the visitor's own browser storage only.

### Challenges I ran into

The hardest part was safety wording: making the app genuinely useful
without ever implying a diagnosis. The fix was structural, not cosmetic
— a rule engine that cannot output a cause, plus automated tests that
fail the build if diagnosis wording ("you have …", "you likely have")
appears in any output.

### What I learned

For health information, explainability is a feature, not a footnote:
showing the exact rule that produced a result builds more trust than a
confident-sounding answer ever could — especially when the honest
answer is "a clinician needs to assess this".

## Built with (tags, <= 25)

Python, JavaScript, HTML, CSS, Standard Library, Healthcare,
Accessibility, Privacy, Explainable AI

## Sponsor / Special Prizes selection

- 1st Place, 2nd Place, 3rd Place (judged places — select as applicable at submit time)
- Tin Computer Growth Plan — only if eligible; do not claim without checking
- Best Research-Oriented Project (YRI) — only if eligible; do not claim without checking

## File upload (required, 35 MB limit)

Upload `docs/project-description.pdf` (one page). Do not upload any file
containing personal data — none exists in this project.
