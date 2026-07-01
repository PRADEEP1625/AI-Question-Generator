import os
import json
import re
import requests
import ollama
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL_MAP = {
    "llama3": "llama3",
    "gpt-4o-mini": "openai/gpt-4o-mini",
}


def build_prompt(topic: str, difficulty: str, count: int) -> str:
    return f"""
Generate exactly {count} multiple-choice questions.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY valid JSON array, no extra text.

Format:
[
  {{
    "question": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    "correct_answer": "A",
    "explanation": "..."
  }}
]
"""


def clean_json(content: str) -> list:
    content = content.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\[.*\]", content, re.DOTALL)
    if match:
        content = match.group(0)

    try:
        questions = json.loads(content)
    except Exception as e:
        print("JSON ERROR:", e)
        print(content)
        raise Exception(f"AI returned invalid JSON:\n\n{content}")

    for q in questions:
        if "explanation" not in q:
            q["explanation"] = "No explanation available."

    return questions


def generate_questions_openrouter(
    topic: str, difficulty: str, count: int, model: str
) -> list:
    prompt = build_prompt(topic, difficulty, count)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=body)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]
    print("\n===== OPENROUTER RESPONSE =====")
    print(content)
    print("================================\n")

    return clean_json(content)


def generate_questions_ollama(topic: str, difficulty: str, count: int) -> list:
    prompt = build_prompt(topic, difficulty, count)

    response = ollama.chat(
        model="llama3", messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]
    print("\n===== OLLAMA RESPONSE =====")
    print(content)
    print("===========================\n")

    return clean_json(content)


def generate_questions(topic: str, difficulty: str, count: int, model: str) -> list:
    mapped_model = MODEL_MAP.get(model, model)

    if mapped_model == "llama3":
        return generate_questions_ollama(topic, difficulty, count)

    return generate_questions_openrouter(topic, difficulty, count, mapped_model)
