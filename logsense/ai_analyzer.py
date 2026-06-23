import json, os
from typing import List
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """You are a senior Linux systems engineer triaging log excerpts.
Given raw flagged log lines, identify the root cause, severity (low/medium/high/critical),
a suggested fix, and a one-sentence summary.
Respond ONLY with valid JSON in this exact shape, nothing else:
{"root_cause": "...", "severity": "...", "suggested_fix": "...", "summary": "..."}
"""

def analyze_entries(entries: List[str]) -> dict:
    if not GROQ_API_KEY:
        return {
            "root_cause": "No API key set.",
            "severity": "unknown",
            "suggested_fix": "Add GROQ_API_KEY to your .env file.",
            "summary": "AI analysis unavailable.",
        }
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        joined = "\n".join(entries[:50])
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Flagged log lines:\n{joined}"}
            ]
        )
        text = response.choices[0].message.content.strip()
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)
    except Exception as exc:
        return {
            "root_cause": "AI analysis call failed.",
            "severity": "unknown",
            "suggested_fix": f"Error: {exc}",
            "summary": "Could not get an AI summary.",
        }
