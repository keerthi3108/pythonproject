"""
Offline study question generator — no API key required.
Uses topic-aware templates and built-in question banks.
"""

import random
from typing import Any

# ---------------------------------------------------------------------------
# Question banks (expandable per topic keyword)
# ---------------------------------------------------------------------------

PYTHON_BANK = {
    "MCQs": [
        {
            "question": "What is the output of `len([1, 2, 3])` in Python?",
            "options": ["3", "2", "1", "Error"],
            "correct_answer": "3",
            "explanation": "`len()` returns the number of items in a sequence.",
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["def", "func", "function", "define"],
            "correct_answer": "def",
            "explanation": "Functions are defined with the `def` keyword.",
        },
        {
            "question": "What does a `for` loop iterate over in Python?",
            "options": ["Any iterable", "Only integers", "Only strings", "Only lists"],
            "correct_answer": "Any iterable",
            "explanation": "`for` loops work with lists, ranges, strings, and other iterables.",
        },
        {
            "question": "Which data type is mutable in Python?",
            "options": ["list", "tuple", "str", "int"],
            "correct_answer": "list",
            "explanation": "Lists can be changed after creation; tuples and strings cannot.",
        },
        {
            "question": "What does `range(3)` produce when converted to a list?",
            "options": ["[0, 1, 2]", "[1, 2, 3]", "[0, 1, 2, 3]", "[3]"],
            "correct_answer": "[0, 1, 2]",
            "explanation": "`range(n)` yields integers from 0 up to (but not including) n.",
        },
    ],
    "True/False": [
        {
            "question": "In Python, indentation is used to define code blocks.",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Python uses indentation instead of braces for blocks.",
        },
        {
            "question": "A Python tuple can be modified after it is created.",
            "options": ["True", "False"],
            "correct_answer": "False",
            "explanation": "Tuples are immutable sequences.",
        },
    ],
    "Short Answers": [
        {
            "question": "Explain the difference between a list and a tuple in Python.",
            "options": [],
            "correct_answer": "Lists are mutable; tuples are immutable. Both store ordered sequences.",
            "explanation": "Use lists when data may change; tuples for fixed collections.",
        },
    ],
}

MATH_BANK = {
    "MCQs": [
        {
            "question": "What is the value of 7 × 8?",
            "options": ["56", "54", "58", "48"],
            "correct_answer": "56",
            "explanation": "7 multiplied by 8 equals 56.",
        },
        {
            "question": "Which of these is a prime number?",
            "options": ["13", "15", "21", "27"],
            "correct_answer": "13",
            "explanation": "13 has only two factors: 1 and 13.",
        },
        {
            "question": "What is 25% of 80?",
            "options": ["20", "25", "30", "40"],
            "correct_answer": "20",
            "explanation": "25% of 80 = 0.25 × 80 = 20.",
        },
    ],
    "True/False": [
        {
            "question": "The sum of angles in a triangle is 180 degrees.",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "This is true in Euclidean geometry.",
        },
    ],
    "Short Answers": [
        {
            "question": "State the Pythagorean theorem.",
            "options": [],
            "correct_answer": "In a right triangle, a² + b² = c² where c is the hypotenuse.",
            "explanation": "Relates the sides of a right-angled triangle.",
        },
    ],
}

SCIENCE_BANK = {
    "MCQs": [
        {
            "question": "What gas do plants absorb during photosynthesis?",
            "options": ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"],
            "correct_answer": "Carbon dioxide",
            "explanation": "Plants use CO₂ and water to produce glucose and oxygen.",
        },
        {
            "question": "What is the chemical symbol for water?",
            "options": ["H₂O", "CO₂", "O₂", "NaCl"],
            "correct_answer": "H₂O",
            "explanation": "Water consists of two hydrogen atoms and one oxygen atom.",
        },
    ],
    "True/False": [
        {
            "question": "The Sun is a star.",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "The Sun is the closest star to Earth.",
        },
    ],
    "Short Answers": [
        {
            "question": "What is photosynthesis in one sentence?",
            "options": [],
            "correct_answer": "Plants convert light energy into chemical energy (glucose) using CO₂ and water.",
            "explanation": "Core process in plant biology and ecosystems.",
        },
    ],
}

HISTORY_BANK = {
    "MCQs": [
        {
            "question": "World War II ended in which year?",
            "options": ["1945", "1939", "1918", "1950"],
            "correct_answer": "1945",
            "explanation": "The war in Europe ended in May 1945; Japan surrendered in August 1945.",
        },
    ],
    "True/False": [
        {
            "question": "The American Declaration of Independence was signed in 1776.",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Adopted on July 4, 1776.",
        },
    ],
    "Short Answers": [
        {
            "question": "Name one major cause of World War I.",
            "options": [],
            "correct_answer": "Militarism, alliances, imperialism, or nationalism (any valid cause).",
            "explanation": "Multiple political and economic factors led to the conflict.",
        },
    ],
}

JAVA_BANK = {
    "MCQs": [
        {
            "question": "Which keyword starts a loop that runs while a condition is true in Java?",
            "options": ["while", "for", "loop", "repeat"],
            "correct_answer": "while",
            "explanation": "`while` evaluates the condition before each iteration.",
        },
        {
            "question": "In a Java enhanced for-loop, what does `for (int x : arr)` iterate over?",
            "options": ["Elements of arr", "Indexes only", "Keys of arr", "Nothing"],
            "correct_answer": "Elements of arr",
            "explanation": "The enhanced for-each loop iterates over each element in a collection or array.",
        },
        {
            "question": "How many times does `for (int i = 0; i < 3; i++)` run the loop body?",
            "options": ["3", "2", "4", "0"],
            "correct_answer": "3",
            "explanation": "i takes values 0, 1, 2 — three iterations.",
        },
    ],
    "True/False": [
        {
            "question": "A Java `for` loop can include initialization, condition, and update in its header.",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Classic for-loop syntax: for (init; condition; update).",
        },
    ],
    "Short Answers": [
        {
            "question": "Explain the difference between `while` and `do-while` loops in Java.",
            "options": [],
            "correct_answer": "`do-while` runs the body at least once; `while` may never run if the condition is false initially.",
            "explanation": "Use do-while when the first execution must happen regardless of the condition.",
        },
    ],
}

# Order matters: more specific topics first (java before generic "loop")
KEYWORD_BANKS: list[tuple[list[str], dict]] = [
    (["java", "jdk", "jvm"], JAVA_BANK),
    (["python", "pythonic"], PYTHON_BANK),
    (["math", "algebra", "geometry", "calculus", "equation"], MATH_BANK),
    (["science", "biology", "chemistry", "physics", "photosynthesis", "cell"], SCIENCE_BANK),
    (["history", "war", "world", "ancient", "civilization"], HISTORY_BANK),
]


def _detect_bank(topic: str) -> dict | None:
    t = topic.lower()
    for keywords, bank in KEYWORD_BANKS:
        if any(kw in t for kw in keywords):
            return bank
    return None


def _difficulty_prefix(difficulty: str) -> str:
    d = difficulty.lower()
    if d == "easy":
        return "(Easy) "
    if d == "hard":
        return "(Hard) "
    return ""


def _generic_mcq(topic: str, difficulty: str, n: int) -> dict:
    prefix = _difficulty_prefix(difficulty)
    return {
        "question": f"{prefix}Which statement best describes an important idea in {topic}?",
        "options": [
            f"A fundamental concept of {topic}",
            f"{topic} has no structured concepts",
            f"{topic} applies only in one narrow case with no rules",
            "None of the above",
        ],
        "correct_answer": f"A fundamental concept of {topic}",
        "explanation": f"Core ideas in {topic} build understanding step by step at {difficulty} level.",
    }


def _generic_tf(topic: str, difficulty: str, n: int) -> dict:
    prefix = _difficulty_prefix(difficulty)
    return {
        "question": f"{prefix}Studying {topic} helps build knowledge at the {difficulty} level.",
        "options": ["True", "False"],
        "correct_answer": "True",
        "explanation": f"Structured study of {topic} improves understanding.",
    }


def _generic_short(topic: str, difficulty: str, n: int) -> dict:
    prefix = _difficulty_prefix(difficulty)
    return {
        "question": f"{prefix}In 2–3 sentences, explain one key concept of {topic}.",
        "options": [],
        "correct_answer": (
            f"A clear explanation of a main idea in {topic}, "
            f"using vocabulary appropriate for {difficulty} difficulty."
        ),
        "explanation": "Good answers name the concept and give a short accurate description.",
    }


def _vary_question(q: dict, topic: str, index: int) -> dict:
    """Personalize bank questions with topic mention where helpful."""
    out = dict(q)
    if topic.lower() not in out["question"].lower() and index > 0:
        out["question"] = f"{out['question']} (Topic: {topic})"
    return out


def generate_local_questions(
    topic: str,
    difficulty: str,
    num_questions: int,
    q_type: str,
) -> list[dict[str, Any]]:
    """
    Generate study questions entirely offline.
    Uses curated banks when topic matches; otherwise smart templates.
    """
    n = max(1, min(int(num_questions), 20))
    topic_label = topic.strip() or "General Studies"
    bank = _detect_bank(topic_label)

    pool: list[dict] = []
    if bank and q_type in bank:
        pool = [dict(q) for q in bank[q_type]]
        random.shuffle(pool)

    questions: list[dict[str, Any]] = []
    used = 0

    while len(questions) < n:
        if pool and used < len(pool):
            questions.append(_vary_question(pool[used], topic_label, used))
            used += 1
            continue

        idx = len(questions) + 1
        if q_type == "True/False":
            questions.append(_generic_tf(topic_label, difficulty, idx))
        elif q_type == "Short Answers":
            questions.append(_generic_short(topic_label, difficulty, idx))
        else:
            questions.append(_generic_mcq(topic_label, difficulty, idx))

    return questions[:n]


# Backward compatibility
generate_demo_questions = generate_local_questions
