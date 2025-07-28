import os
import json
import httpx
import asyncpg
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def build_headers():
    return {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

async def interpret_query(prompt: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=build_headers(),
                json={
                    "model": "gpt-3.5-turbo",  # you can change to "gpt-4o" later
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "Extract medication and protocol from this question. "
                                "Reply ONLY as JSON: {\"medication\": \"Epinephrine\", \"protocol\": \"Trauma Protocol\"}"
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0
                }
            )

        result = response.json()

        # DEBUGGING HELP
        if "choices" not in result:
            return f"OpenAI returned no choices. Full response:\n{result}"

        message = result["choices"][0]["message"]["content"].strip()

        try:
            parsed = json.loads(message)
            medication = parsed.get("medication")
            protocol = parsed.get("protocol")
        except Exception:
            return f"Could not parse JSON. GPT said:\n{message}"

        if not medication or not protocol:
            return f"OpenAI response missing keys. Got:\n{message}"

        return await query_dose_by_med_and_protocol(medication, protocol)

    except Exception as e:
        return f"Error contacting OpenAI: {str(e)}"

async def query_dose_by_med_and_protocol(medication: str, protocol: str) -> str:
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    rows = await conn.fetch("""
        SELECT m.name AS medication, p.name AS protocol, md.dose_info
        FROM medicationdose md
        JOIN medication m ON md.medication_id = m.id
        JOIN protocol p ON md.protocol_id = p.id
        WHERE LOWER(m.name) = LOWER($1)
          AND LOWER(p.name) = LOWER($2)
    """, medication, protocol)
    await conn.close()

    if not rows:
        return f"No doses found for '{medication}' in '{protocol}'."

    return rows[0]["dose_info"]