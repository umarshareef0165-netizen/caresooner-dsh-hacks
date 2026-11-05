"""Generate the one-page project description PDF using only the stdlib.

Writes a single-page A4 PDF with Helvetica. No external tools needed.
The script fails loudly if the content would overflow one page, so the
submitted PDF is genuinely one page.
"""
import os
import textwrap

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "project-description.pdf")
W, H, MARGIN = 595, 842, 48
BODY_W = W - 2 * MARGIN


def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build():
    # (kind, text) — kind: title, h, body, bullet
    blocks = [
        ("title", "CareSooner — Early Health Concern Explainer"),
        ("sub", "DSH Hacks V2 — AI x Healthcare  |  By Umar Shareef (solo)  |  General information only — not a diagnosis"),
        ("h", "Problem"),
        ("body", "When a health concern appears, people often do not know what to notice, what counts as urgent, or what to ask a clinician. That confusion delays care, and a first appointment is often spent trying to describe a pattern from memory instead of discussing it."),
        ("h", "Solution"),
        ("body", "CareSooner is a web app that turns a confusing concern into plain-language general information in four steps: (1) choose up to three concern topics; (2) run a red-flag safety check, shown first if any red flag applies; (3) track dated observations in the browser to spot a repeating or worsening pattern early; (4) generate a printable visit-prep note with questions for a clinician."),
        ("h", "How it works — and why it is honest"),
        ("body", "The engine is a transparent rule set (rules R1-R6, shown in the app). No machine-learning model, no external API, no black-box score. Red flags always come first. The app never names a cause, never predicts a disease, and never says what a user has. Every result carries the same disclaimer, and the tracker stores data only in the visitor's own browser; the server is stateless and stores nothing."),
        ("h", "What was built"),
        ("body", "A working prototype: Python standard library server, plain HTML/CSS/JavaScript front end, eight concern topics, a ten-item red-flag check, a browser-only change tracker, and a visit-note generator. Tests cover the safety rules, including red-flag priority, invalid inputs, and a ban on diagnosis wording in all output."),
        ("h", "Limits and next steps"),
        ("body", "Limits: general information only; not validated on patients or medical records; English only for now. Next: clinician review of the information text, more languages, and accessibility testing with real users — before any claim beyond general information is ever made."),
        ("h", "Built with"),
        ("body", "Python (standard library only), HTML, CSS, JavaScript. No accounts, no database, no API keys."),
    ]
    lines = []  # (font_size, bold, text)
    for kind, text in blocks:
        if kind == "title":
            lines.append((16, True, text)); lines.append((4, False, ""))
        elif kind == "sub":
            lines.append((9, False, text)); lines.append((6, False, ""))
        elif kind == "h":
            lines.append((11, True, text))
        elif kind == "bullet":
            for w in textwrap.wrap(text, 88):
                lines.append((10, False, "•  " + w))
        else:
            for w in textwrap.wrap(text, 92):
                lines.append((10, False, w))
        if kind in ("body",):
            lines.append((4, False, ""))
    # Layout: 10pt font, 13.5pt leading; title 20pt; headings 15pt.
    y = H - 52
    content = ["BT"]
    for size, bold, text in lines:
        leading = 20 if size == 16 else 15 if size == 11 else 13.5 if size == 10 else size
        y -= leading
        if y < 48:
            raise SystemExit("PDF overflow: content exceeds one page — shorten the text.")
        if text:
            content.append(f"/F{'B' if bold else ''} {size} Tf 1 0 0 1 {MARGIN} {y:.1f} Tm ({esc(text)}) Tj")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", "replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F /F1 /FB /F2 >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    ]
    # Font objects are 5 and 6; page references them as /F and /FB — fix mapping:
    objects[2] = (b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                  b"/Resources << /Font << /F 5 0 R /FB 6 0 R >> >> /Contents 4 0 R >>")
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref_pos = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n").encode()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(out)
    print(f"Wrote {OUT} ({len(out)} bytes, 1 page, {len(lines)} laid-out lines)")


if __name__ == "__main__":
    build()
