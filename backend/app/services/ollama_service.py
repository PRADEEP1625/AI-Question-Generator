import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_questions(topic: str, difficulty: str, count: int, model: str):

    prompt = f"""
Generate exactly {count} multiple-choice questions.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY valid JSON.

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

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(URL, headers=headers, json=body)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    print("\n===== AI RESPONSE =====")
    print(content)
    print("=======================\n")

    # --- JSON cleaning safety net ---
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    match = re.search(r"\[.*\]", content, re.DOTALL)
    if match:
        content = match.group(0)

    try:
        questions = json.loads(content)
    except Exception as e:
        print("JSON ERROR:", e)
        print(content)
        raise Exception(f"AI returned invalid JSON:\n\n{content}")

    # --- fill in missing optional fields ---
    for q in questions:
        if "explanation" not in q:
            q["explanation"] = "No explanation available."

    return questions
