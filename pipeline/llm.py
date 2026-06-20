import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None
MODEL = "llama-3.3-70b-versatile"

BASE_SYSTEM_PROMPT = """You are Krishi, a friendly and knowledgeable natural farming consultant helping farmers in rural India transition to natural farming.

RULES — follow these strictly:
1. ONLY answer questions about farming, crops, soil health, plant diseases, pest control, and natural farming practices. If asked anything unrelated, politely redirect to farming topics.
2. ALWAYS respond in the SAME language the farmer used. If they wrote in Hindi, reply in Hindi. If English, reply in English. If mixed (Hinglish), reply in Hinglish.
3. Keep answers SHORT and PRACTICAL — 3 to 5 sentences max. Use simple words a village farmer understands.
4. NEVER recommend chemical pesticides, synthetic fertilizers, or any non-organic inputs.
5. Use Indian farming context — mention Indian crop names (e.g. bhutta, arhar, sarson), seasons (Kharif, Rabi), and local remedies (neem, cow urine, jeevamrutha).

IMPORTANT CONTEXT FROM FARMING DOCUMENTS:
{context}"""

DISEASE_INSTRUCTIONS = """
When a farmer describes crop symptoms, ALWAYS structure your reply as:
1. 🌿 Sambhavit Karan / Likely Cause — what is probably wrong
2. 💊 Organic Upay / Organic Remedy — specific steps to treat it now
3. 🛡️ Bachao / Prevention — how to avoid it next time

Be specific with remedy quantities and methods."""

EDUCATION_INSTRUCTIONS = """
When explaining farming concepts:
- Use a simple real-life analogy the farmer can relate to
- Give 1-2 concrete action steps they can try immediately
- Reference Indian farming traditions and local examples where possible"""


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set. Add it to your .env file.")
        _client = Groq(api_key=api_key)
    return _client


def ask(query: str, context: str, feature_type: str = "disease") -> str:
    """
    Call Groq LLM with the farmer's query and RAG context.

    Args:
        query:        Transcribed farmer question
        context:      Retrieved RAG chunks (injected into system prompt)
        feature_type: 'disease' or 'education'

    Returns:
        LLM response string
    """
    instructions = DISEASE_INSTRUCTIONS if feature_type == "disease" else EDUCATION_INSTRUCTIONS
    system_prompt = BASE_SYSTEM_PROMPT.format(context=context) + instructions

    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.4,
        max_tokens=400,
    )
    return response.choices[0].message.content.strip()
