"""CareSooner — explainable, rule-based health-concern explainer.

Safety contract (read before changing this file):
- This module NEVER diagnoses, NEVER predicts a disease, and NEVER says
  what a user "has" or "likely has".
- It only returns general information, red-flag safety information, and
  questions a person can take to a real clinician.
- Red-flag output is general safety information, not a medical decision:
  if any red flag is selected, the emergency information is shown first
  and the user is told to seek emergency care now.
- No patient data, no statistics, and no user counts are invented here.
  The only "demo" is an explicitly labelled example flow in the UI.
"""

TOPICS = [
    {
        "id": "chest-discomfort",
        "title": "Chest discomfort or pressure",
        "summary": "People describe chest discomfort in many different ways, and the same "
                   "words can be used for very different situations. This section does "
                   "not try to name a cause. It helps you notice details that are "
                   "useful to describe to a clinician.",
        "notice": ["When it started, and whether it came on suddenly or gradually",
                   "What it feels like in your own words, and where you feel it",
                   "Whether it changes with rest, movement, or breathing",
                   "Anything else happening at the same time, such as sweating or nausea"],
        "questions": ["Can you help me understand what details matter most here?",
                      "What should I watch for before my appointment?",
                      "What information should I bring with me?"],
        "red_flags": ["Chest pain or pressure, especially with sweating, nausea, or pain spreading to an arm, jaw, or back"],
    },
    {
        "id": "breathing-difficulty",
        "title": "Difficulty breathing",
        "summary": "Breathing difficulty is described very differently by different people. "
                   "This section does not name a cause. It helps you describe the "
                   "pattern clearly to a clinician.",
        "notice": ["When it started, and whether it is worse at rest or with activity",
                   "Whether you can speak in full sentences comfortably",
                   "Any cough, wheeze, or change in breathing pattern you notice",
                   "Anything that seems to make it better or worse"],
        "questions": ["How should I describe my breathing pattern to a clinician?",
                      "What should I watch for before my appointment?",
                      "What information should I bring with me?"],
        "red_flags": ["Difficulty breathing or shortness of breath at rest",
                      "Lips or face looking blue or grey"],
    },
    {
        "id": "fever",
        "title": "Fever",
        "summary": "Fever is a raised body temperature, and people experience it with very "
                   "different accompanying concerns. This section does not name a "
                   "cause. It helps you track the pattern to describe to a clinician.",
        "notice": ["How long the fever has been present, and how it changes over the day",
                   "Any other concerns present at the same time, such as cough or rash",
                   "How you are eating, drinking, and resting",
                   "Any recent travel, contact with illness, or new medicines you want to mention"],
        "questions": ["How should I track this pattern before my appointment?",
                      "What should I watch for before my appointment?",
                      "What information should I bring with me?"],
        "red_flags": ["Fever with difficulty breathing, chest pain, confusion, or a stiff neck",
                      "Fever that keeps returning after improving, with a worse cough"],
    },
    {
        "id": "headache",
        "title": "Headache",
        "summary": "Headaches vary a great deal in pattern and intensity. This section does "
                   "not name a cause. It helps you describe the pattern clearly to "
                   "a clinician.",
        "notice": ["When it started, and whether it came on suddenly or gradually",
                   "Where you feel it, and how it changes over hours or days",
                   "Anything happening at the same time, such as vision changes or nausea",
                   "Any recent injury, illness, or change you want to mention"],
        "questions": ["How should I describe this headache pattern to a clinician?",
                      "What should I watch for before my appointment?",
                      "What information should I bring with me?"],
        "red_flags": ["A sudden, very severe headache described as the worst of your life",
                      "Headache with sudden vision changes, weakness, confusion, or difficulty speaking"],
    },
    {
        "id": "stomach-pain",
        "title": "Stomach or abdominal pain",
        "summary": "Abdominal pain is described in many ways and can change over time. This "
                   "section does not name a cause. It helps you describe the pattern "
                   "clearly to a clinician.",
        "notice": ["Where you feel it, and whether it moves or stays in one place",
                   "When it started, and whether it is steady, comes and goes, or worsening",
                   "Anything happening at the same time, such as vomiting or fever",
                   "How eating, drinking, and resting relate to the pattern"],
        "questions": ["How should I describe this pain pattern to a clinician?",
                      "What should I watch for before my appointment?",
                      "What information should I bring with me?"],
        "red_flags": ["Severe abdominal pain, especially if sudden",
                      "Vomiting blood, or coughing up blood",
                      "Uncontrolled bleeding"],
    },
    {
        "id": "skin-change",
        "title": "A new or changing skin mark",
        "summary": "Skin marks change for many reasons, and a photograph or a note about "
                   "change over time can help a clinician. This section does not "
                   "judge whether a mark is serious. It helps you record change.",
        "notice": ["When you first noticed it, and how it has changed since then",
                   "Its size, colour, shape, and border, in your own words",
                   "Whether it itches, hurts, bleeds, or has changed quickly",
                   "Any new products, sun exposure, or injuries you want to mention"],
        "questions": ["What kind of record of this change would be most useful?",
                      "What should I watch for before my appointment?",
                      "What information should I bring with me?"],
        "red_flags": ["A mark that is changing very quickly, bleeding heavily, or spreading with fever"],
    },
    {
        "id": "tiredness",
        "title": "Tiredness or low energy",
        "summary": "Tiredness can build gradually and affect daily life in different ways. "
                   "This section does not name a cause. It helps you describe the "
                   "pattern and its effect on daily activities to a clinician.",
        "notice": ["When it started, and whether it is steady or comes and goes",
                   "How it affects sleep, work, study, and daily activities",
                   "Anything happening at the same time, such as weight change or low mood",
                   "Any recent illness, life change, or new medicines you want to mention"],
        "questions": ["How should I describe this pattern and its effect on my day?",
                      "What should I watch for before my appointment?",
                      "What information should I bring with me?"],
        "red_flags": ["Tiredness with chest pain, difficulty breathing, fainting, or confusion"],
    },
    {
        "id": "low-mood",
        "title": "Low mood or stress",
        "summary": "Low mood and stress affect people in different ways and can change over "
                   "time. This section does not diagnose a mental-health condition. "
                   "It helps you describe what you are experiencing so you can seek "
                   "support from a clinician or a trusted support service.",
        "notice": ["When it started, and whether it is steady or comes and goes",
                   "How it affects sleep, appetite, work, study, and daily activities",
                   "What support you already have, and what feels hardest right now",
                   "Anything you want to be able to say clearly at an appointment"],
        "questions": ["How can I describe what I am experiencing clearly?",
                      "What support options can we talk about?",
                      "What information should I bring with me?"],
        "red_flags": ["Thoughts of harming yourself, or feeling you may act on them"],
    },
]

TOPIC_BY_ID = {t["id"]: t for t in TOPICS}

RED_FLAGS = [
    "Chest pain or pressure",
    "Difficulty breathing or shortness of breath at rest",
    "Sudden face drooping, arm weakness, or difficulty speaking",
    "A sudden, very severe headache",
    "Fainting, confusion, or sudden dizziness",
    "Uncontrolled bleeding",
    "Coughing or vomiting blood",
    "Severe abdominal pain",
    "Swelling of the lips or face with difficulty breathing (possible severe allergic reaction)",
    "Thoughts of harming yourself",
]

DURATIONS = ["today", "a few days", "a few weeks", "a few months", "not sure"]
PATTERNS = ["sudden", "gradual", "comes and goes", "getting worse", "getting better", "not sure"]

DISCLAIMER = ("General information only. This tool does not diagnose, treat, or "
              "replace a clinician. If a red-flag concern applies, seek emergency "
              "care now. Otherwise, a clinician decides what any concern means.")

BANNED_PHRASES = ["you have ", "you likely have", "diagnosis is", "you are suffering from"]


def explain(topic_ids, red_flags, duration="not sure", pattern="not sure"):
    """Return the explainable result for the given selections.

    Rules are applied in order and returned as a visible trace, so a judge
    can see exactly why each section was shown. No rule ever outputs a
    diagnosis.
    """
    if not isinstance(topic_ids, list):
        raise ValueError("topic_ids must be a list")
    if len(topic_ids) > 3:
        raise ValueError("choose at most 3 concern topics")
    unknown = [t for t in topic_ids if t not in TOPIC_BY_ID]
    if unknown:
        raise ValueError("unknown topic id: " + ", ".join(unknown))
    if not isinstance(red_flags, list):
        raise ValueError("red_flags must be a list")
    unknown_flags = [f for f in red_flags if f not in RED_FLAGS]
    if unknown_flags:
        raise ValueError("unknown red flag: " + ", ".join(unknown_flags))
    if duration not in DURATIONS:
        raise ValueError("unknown duration: " + repr(duration))
    if pattern not in PATTERNS:
        raise ValueError("unknown pattern: " + repr(pattern))

    trace = []
    topics = [TOPIC_BY_ID[t] for t in topic_ids]
    if red_flags:
        priority = "seek-emergency-care-now"
        priority_text = ("Seek emergency care now. This is general safety "
                         "information for a red-flag concern, not a diagnosis. "
                         "Do not wait to see whether it passes.")
        trace.append("R1: a red flag was selected, so emergency information is shown first.")
    elif pattern == "getting worse":
        priority = "contact-a-clinician-promptly"
        priority_text = ("General information: a concern that is getting worse is "
                         "worth raising with a clinician promptly. A clinician "
                         "decides how urgent it is.")
        trace.append("R2: pattern is 'getting worse', so prompt clinician contact information is shown.")
    elif not topics:
        priority = "choose-a-topic"
        priority_text = ("Choose at least one concern topic above to see general "
                         "information, red flags, and questions for a clinician.")
        trace.append("R3: no topic selected, so a starter prompt is shown instead of a result.")
    else:
        priority = "prepare-and-book-routine-care"
        priority_text = ("General information: prepare the questions below and book "
                         "routine care if the concern persists or worries you. "
                         "A clinician decides what it means.")
        trace.append("R4: no red flag and no worsening pattern, so routine preparation information is shown.")
    if topics:
        trace.append("R5: one information section is shown per selected topic, in the order selected.")
    if duration != "not sure" or pattern != "not sure":
        trace.append("R6: duration and pattern are copied into the visit note only; they do not change any diagnosis, because this tool makes none.")

    questions = []
    for t in topics:
        for q in t["questions"]:
            if q not in questions:
                questions.append(q)

    return {
        "disclaimer": DISCLAIMER,
        "priority": priority,
        "priority_text": priority_text,
        "topics": topics,
        "selected_red_flags": red_flags,
        "duration": duration,
        "pattern": pattern,
        "questions_for_clinician": questions,
        "trace": trace,
        "all_red_flags": RED_FLAGS,
    }


def visit_note(topic_ids, red_flags, duration="not sure", pattern="not sure",
                observations=None):
    """Build a plain-text visit-prep note. Nothing is stored server-side."""
    result = explain(topic_ids, red_flags, duration, pattern)
    lines = ["CareSooner — Visit-prep note (for a clinician appointment)",
             DISCLAIMER, "",
             "Concerns selected: " + (", ".join(t["title"] for t in result["topics"]) or "none"),
             "Duration: " + duration + " | Pattern: " + pattern,
             "Red flags selected: " + (", ".join(red_flags) or "none"),
             "Priority information shown: " + result["priority_text"], "",
             "Questions I want to ask:"]
    for q in result["questions_for_clinician"]:
        lines.append("- " + q)
    lines.append("")
    if observations:
        lines.append("My own observations (dates and notes I entered):")
        for obs in observations:
            if not isinstance(obs, dict):
                raise ValueError("each observation must be an object with date, topic and note")
            lines.append("- " + str(obs.get("date", "")) + " | " +
                         str(obs.get("topic", "")) + " | " + str(obs.get("note", ""))[:200])
        lines.append("")
    lines.append("This note is general information only. It is not a diagnosis, "
                 "and it does not replace a clinician's assessment.")
    text = "\n".join(lines)
    for phrase in BANNED_PHRASES:
        assert phrase not in text.lower(), "banned diagnosis phrase in visit note"
    return text
