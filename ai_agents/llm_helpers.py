import os
from openai import OpenAI
from typing import Tuple
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def analyze_log(log_text: str, build_data: dict) -> Tuple[str, str]:
    job = build_data.get("job_name")
    build_num = build_data.get("build_number")

    prompt = f"""
You are a DevOps assistant. A Jenkins job named '{job}' failed (build #{build_num}).
Here is a portion of the Jenkins console output:

--- BEGIN LOG ---
{log_text[:3500]}
--- END LOG ---

1. What is the likely cause of failure? Be concise.
2. Suggest a fix or retry instruction in 1–2 lines.
Reply using this format:

Reason: <explanation>
Suggestion: <action>
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Basic parsing
    lines = content.splitlines()
    reason = ""
    suggestion = ""

    for line in lines:
        if line.lower().startswith("reason:"):
            reason = line.partition(":")[2].strip()
        elif line.lower().startswith("suggestion:"):
            suggestion = line.partition(":")[2].strip()

    return reason, suggestion


if __name__ == "__main__":
    from pathlib import Path

    log = Path("sample_console_log.txt").read_text()
    data = {"job_name": "my-job", "build_number": 7}
    cause, solution = analyze_log(log, data)
    print(f"Reason: {cause}")
    print(f"Suggestion: {solution}")
