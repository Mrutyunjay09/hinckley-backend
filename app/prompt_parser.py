import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# Simulate basic NLP matching (replace this with AI later if needed)
def extract_med_and_protocol(prompt: str):
    prompt = prompt.lower()

    meds = ["epinephrine", "ibuprofen"]
    protocols = ["trauma protocol", "fever protocol"]

    medication = next((m for m in meds if m in prompt), None)
    protocol = next((p for p in protocols if p in prompt), None)

    return medication, protocol


async def interpret_query(prompt: str) -> str:
    try:
        medication, protocol = extract_med_and_protocol(prompt)

        if not medication or not protocol:
            return "Could not extract medication or protocol from the prompt."

        return await query_dose(medication, protocol)

    except Exception as e:
        return f"Error interpreting query: {str(e)}"


async def query_dose(medication: str, protocol: str) -> str:
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))

    query = """
    SELECT md.dose_info
    FROM medicationdose md
    JOIN medication m ON md.medication_id = m.id
    JOIN protocol p ON md.protocol_id = p.id
    WHERE LOWER(m.name) = LOWER($1)
      AND LOWER(p.name) = LOWER($2)
    """

    rows = await conn.fetch(query, medication, protocol)
    await conn.close()

    if not rows:
        return f"No dose found for {medication} in {protocol}."

    return "\n".join([row["dose_info"] for row in rows])
