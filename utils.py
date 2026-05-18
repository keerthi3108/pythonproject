"""
OpenAI API integration and question formatting (no Streamlit imports).
"""

import json
import os
import re
import time
from typing import Any

import requests

OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
# gpt-3.5-turbo often has higher free-tier limits than gpt-4o-mini
DEFAULT_MODELS = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"]
PLACEHOLDER_KEYS = {"", "your_openai_api_key_here", "your_grok_api_key_here"}

# Questions per API call (smaller = less likely to hit rate limits)
BATCH_SIZE = int(os.getenv("OPENAI_BATCH_SIZE", "3"))
MAX_RETRIES = 4
RETRY_BASE_SECONDS = [2, 5, 12, 25]


def get_openai_model() -> str:
    return os.getenv("OPENAI_MODEL", DEFAULT_MODELS[0]).strip() or DEFAULT_MODELS[0]


def _models_to_try() -> list[str]:
    primary = get_openai_model()
    return [primary] + [m for m in DEFAULT_MODELS if m != primary]


def _build_system_prompt(q_type: str) -> str:
    type_rules = {
        "MCQs": (
            'Each question is multiple-choice with exactly 4 options in "options". '
            '"correct_answer" must exactly match one option string.'
        ),
        "Short Answers": (
            '"options" must be []. "correct_answer" is the ideal short answer (1-3 sentences).'
        ),
        "True/False": (
            '"options" must be ["True", "False"]. '
            '"correct_answer" must be exactly "True" or "False".'
        ),
    }
    rules = type_rules.get(q_type, type_rules["MCQs"])
    return f"""You are an expert study question generator.
{rules}

Respond with ONLY valid JSON using this schema:
{{"questions":[{{"question":"...","options":["..."],"correct_answer":"...","explanation":"..."}}]}}

Include exactly the requested number of questions. Match difficulty level. No duplicate questions."""


def _build_user_prompt(topic: str, difficulty: str, num_questions: int, q_type: str) -> str:
    n = int(num_questions)
    return (
        f"Topic: {topic}\n"
        f"Difficulty: {difficulty}\n"
        f"Question type: {q_type}\n"
        f"Generate exactly {n} unique questions."
    )


def _rate_limit_message(detail: str = "") -> str:
    msg = (
        "OpenAI rate limit reached (too many requests or tokens). "
        "Try again in 1–2 minutes, generate **1–3 questions** at a time, "
        "or enable **Demo mode** in the sidebar. "
    )
    if detail:
        msg += f"Details: {detail}"
    return msg


def _extract_api_error(response: requests.Response) -> str:
    try:
        err_body = response.json()
    except json.JSONDecodeError:
        return (response.text or "Unknown API error")[:400]

    if isinstance(err_body, dict):
        err = err_body.get("error")
        if isinstance(err, dict):
            return str(err.get("message") or err.get("code") or err)
        if isinstance(err, str):
            return err
        if err_body.get("message"):
            return str(err_body["message"])
    return (response.text or "Unknown API error")[:400]


def _strip_markdown_json(content: str) -> str:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```\s*$", "", text)
    return text.strip()


def _extract_json_object(text: str) -> str:
    text = _strip_markdown_json(text)
    if text.startswith("{") or text.startswith("["):
        return text
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    return match.group(1) if match else text


def _normalize_question(raw: dict) -> dict[str, Any]:
    return {
        "question": str(raw.get("question", raw.get("Question", "N/A"))),
        "options": raw.get("options") or raw.get("Options") or [],
        "correct_answer": str(
            raw.get("correct_answer", raw.get("correctAnswer", raw.get("answer", "N/A")))
        ),
        "explanation": str(raw.get("explanation", raw.get("Explanation", "N/A"))),
    }


def _parse_questions_payload(content: str) -> list[dict[str, Any]] | None:
    cleaned = _extract_json_object(content)
    data = json.loads(cleaned)

    items: list | None = None
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if isinstance(data.get("questions"), list):
            items = data["questions"]
        else:
            for value in data.values():
                if isinstance(value, list) and value:
                    items = value
                    break
            if items is None:
                items = [data]

    if not items:
        return None
    return [_normalize_question(q) for q in items if isinstance(q, dict)]


def _max_tokens_for_batch(batch_count: int) -> int:
    return min(4096, 350 * batch_count + 400)


def _request_once(model: str, headers: dict, payload: dict) -> requests.Response:
    body = {**payload, "model": model}
    return requests.post(OPENAI_CHAT_URL, headers=headers, json=body, timeout=120)


def _request_with_retry(model: str, headers: dict, payload: dict) -> requests.Response:
    """POST with automatic retry on HTTP 429."""
    response = None
    for attempt in range(MAX_RETRIES):
        response = _request_once(model, headers, payload)
        if response.status_code != 429:
            return response

        retry_after = response.headers.get("Retry-After")
        if retry_after and str(retry_after).isdigit():
            wait = int(retry_after)
        else:
            wait = RETRY_BASE_SECONDS[min(attempt, len(RETRY_BASE_SECONDS) - 1)]

        if attempt < MAX_RETRIES - 1:
            time.sleep(wait)

    return response


def _call_single_batch(
    topic: str,
    difficulty: str,
    batch_count: int,
    q_type: str,
    api_key: str,
) -> tuple[list[dict[str, Any]] | None, str | None]:
    """One API call for up to batch_count questions."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "messages": [
            {"role": "system", "content": _build_system_prompt(q_type)},
            {"role": "user", "content": _build_user_prompt(topic, difficulty, batch_count, q_type)},
        ],
        "temperature": 0.6,
        "max_tokens": _max_tokens_for_batch(batch_count),
        "response_format": {"type": "json_object"},
    }

    last_error = "Unknown error"
    response = None

    for model in _models_to_try():
        try:
            response = _request_with_retry(model, headers, payload)
        except requests.exceptions.Timeout:
            return None, "Request timed out. Try 1–3 questions."
        except requests.exceptions.ConnectionError:
            return None, "Could not reach OpenAI API. Check your internet connection."
        except requests.exceptions.RequestException as exc:
            return None, f"Network error: {exc}"

        if response.status_code == 400 and "model" in response.text.lower():
            last_error = _extract_api_error(response)
            continue

        if response.status_code == 401:
            return None, "Invalid API key. Check OPENAI_API_KEY in .env."
        if response.status_code == 403:
            return None, f"OpenAI access denied: {_extract_api_error(response)}"
        if response.status_code == 429:
            detail = _extract_api_error(response)
            return None, _rate_limit_message(detail)
        if not response.ok:
            return None, f"API error ({response.status_code}): {_extract_api_error(response)}"
        break
    else:
        return None, f"All models failed. Last error: {last_error}"

    try:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, AttributeError):
        return None, "Unexpected API response format."

    try:
        questions = _parse_questions_payload(content)
    except json.JSONDecodeError:
        return None, "Could not parse AI response as JSON. Please try again."

    if not questions:
        return None, "No questions returned. Please try again."

    return questions[:batch_count], None


def call_openai_api(
    topic: str,
    difficulty: str,
    num_questions: int,
    q_type: str,
    api_key: str,
) -> tuple[list[dict[str, Any]] | None, str | None]:
    """
    Generate questions via OpenAI. Uses small batches + retries to reduce rate-limit errors.
    """
    if not api_key or api_key in PLACEHOLDER_KEYS:
        return None, "API key missing. Set OPENAI_API_KEY in study-ai/.env or Streamlit secrets."

    total = max(1, min(int(num_questions), 20))
    all_questions: list[dict[str, Any]] = []
    remaining = total
    batch_size = max(1, min(BATCH_SIZE, 5))

    while remaining > 0:
        chunk = min(batch_size, remaining)
        batch, error = _call_single_batch(topic, difficulty, chunk, q_type, api_key)

        if error:
            if all_questions:
                return all_questions, (
                    f"Partial success: got {len(all_questions)}/{total} questions. {error}"
                )
            return None, error

        all_questions.extend(batch or [])
        remaining = total - len(all_questions)

        if remaining > 0:
            time.sleep(1.5)

    return all_questions[:total], None


call_grok_api = call_openai_api


def format_single_question(index: int, q: dict) -> str:
    lines = [f"Q{index}: {q.get('question', 'N/A')}"]
    for j, opt in enumerate(q.get("options") or []):
        lines.append(f"  {chr(65 + j)}. {opt}")
    lines.append(f"Answer: {q.get('correct_answer', 'N/A')}")
    lines.append(f"Explanation: {q.get('explanation', 'N/A')}")
    return "\n".join(lines)


def format_questions_for_export(
    questions: list[dict],
    topic: str,
    difficulty: str,
    q_type: str,
) -> str:
    lines = [
        "StudyAI — Generated Questions",
        "=" * 44,
        f"Topic: {topic}",
        f"Difficulty: {difficulty}  |  Type: {q_type}",
        f"Count: {len(questions)}",
        "=" * 44,
        "",
    ]
    for i, q in enumerate(questions, start=1):
        lines.append(format_single_question(i, q))
        lines.append("-" * 44)
        lines.append("")
    return "\n".join(lines)
