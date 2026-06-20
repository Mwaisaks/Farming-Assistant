# 🌾 Krishi — Voice-Based Natural Farming Consultant

Krishi is a voice-first AI assistant that helps farmers in rural India transition to natural farming. Farmers speak their question in Hindi, English, or mixed (Hinglish), and Krishi responds with practical organic advice — spoken back in the same language.

---

## What It Does

**Two features (Option B):**

| Tab | What the farmer does | What Krishi does |
|-----|----------------------|------------------|
| 🦠 Disease & Treatment | Describes crop symptoms by voice | Identifies likely cause, gives organic remedy, and explains prevention |
| 📚 Farming Education | Asks about natural farming practices | Explains concepts using Indian analogies and gives immediate action steps |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| UI | Gradio 4.44 — mobile-friendly, runs in browser |
| Speech-to-Text | OpenAI Whisper (base model) — supports Hindi + English |
| LLM | Groq API — `llama-3.3-70b-versatile` |
| Text-to-Speech | gTTS — auto-detects Hindi (Devanagari) vs English |
| RAG | ChromaDB (in-memory) + `all-MiniLM-L6-v2` embeddings |
| PDF parsing | PyMuPDF |
| Language | Python 3.10+ |

---

## Prompt Design & Guardrails

The system prompt defines Krishi's persona and enforces strict rules:

1. **Domain lock** — Only answers farming, crops, soil, and plant health questions. Off-topic queries are politely redirected.
2. **Language mirroring** — Detects the language of the farmer's query and replies in the same language (Hindi, English, or Hinglish).
3. **Brevity** — Responses capped at 3–5 sentences; uses simple vocabulary suited for village farmers.
4. **Organic only** — Never recommends chemical pesticides or synthetic fertilizers.
5. **Indian context** — Mentions Indian crop names (bhutta, arhar), seasons (Kharif, Rabi), and local remedies (neem spray, jeevamrutha, cow urine solution).

**Disease feature structure** (enforced in prompt):
```
1. 🌿 Likely Cause
2. 💊 Organic Remedy (with quantities and steps)
3. 🛡️ Prevention
```

**RAG injection** — Top 2 relevant chunks from farming documents are injected into the system prompt as grounding context before every LLM call.

---

## Localization Approach

- **Whisper** transcribes Hindi and English audio without language configuration — the `base` model handles both.
- **gTTS** detects the script: if the LLM response contains Devanagari characters it uses `lang='hi'`, otherwise `lang='en'`.
- **LLM prompt** explicitly instructs the model to mirror the farmer's language, enabling natural Hinglish responses.
- Example: a farmer who asks *"Meri tomato ke patte pe kale dabbe aa rahe hain"* gets a Hindi/Hinglish response with organic remedy steps.

---

## Knowledge Base (RAG Documents)

Documents in `docs/` are chunked (600 chars, 100-char overlap) and indexed into ChromaDB at startup:

| File | Content |
|------|---------|
| `Field-Guide-for-Natural-Farming.pdf` | NCOF field guide for natural farming practices |
| `palekar_natural_farming.txt` | Subhash Palekar's Zero Budget Natural Farming principles |
| `common_diseases_organic_remedies.txt` | Common crop diseases and organic treatment recipes |
| `companion_planting_multilayer.txt` | Companion planting and multilayer farming guide |

---

## How to Run Locally

### 1. Clone and set up environment

```bash
git clone <repo-url>
cd farming-assistant
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** Whisper requires `ffmpeg`. Install it with:
> - Ubuntu/Debian: `sudo apt install ffmpeg`
> - Mac: `brew install ffmpeg`
> - Windows: download from https://ffmpeg.org/download.html

### 2. Set your API key

```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

```
GROQ_API_KEY=your_key_here
```

Get a free Groq API key at https://console.groq.com

### 3. Run the app

```bash
python app.py
```

Gradio will print a local URL (e.g. `http://127.0.0.1:7860`) and a public share link. Open either in your browser.

### 4. (Optional) Run the smoke test first

```bash
python test_pipeline.py
```

This verifies TTS, RAG, and LLM modules work before launching the UI (no microphone required).

---

## How to Deploy to HuggingFace Spaces

1. Create a new Space at https://huggingface.co/spaces — choose **Gradio** SDK.
2. In the Space **Settings → Repository secrets**, add `GROQ_API_KEY`.
3. Push the repository:

```bash
git remote add space https://huggingface.co/spaces/<your-username>/<space-name>
git push space main
```

HuggingFace will install `requirements.txt` and run `app.py` automatically. The public URL is live within a few minutes.

> **Hardware note:** Whisper `base` model runs on CPU. For faster transcription on HuggingFace, choose a Space with at least 2 vCPUs or switch to the Groq Whisper API endpoint.

---

## Project Structure

```
farming-assistant/
├── app.py                  # Gradio UI — wires all pipeline modules
├── pipeline/
│   ├── __init__.py
│   ├── stt.py              # Whisper transcription
│   ├── tts.py              # gTTS text-to-speech
│   ├── rag.py              # ChromaDB indexing and retrieval
│   └── llm.py              # Groq LLM with system prompt
├── docs/                   # Farming knowledge base
│   ├── Field-Guide-for-Natural-Farming.pdf
│   ├── palekar_natural_farming.txt
│   ├── common_diseases_organic_remedies.txt
│   └── companion_planting_multilayer.txt
├── test_pipeline.py        # Smoke test (no mic needed)
├── requirements.txt
├── .env.example
└── README.md
```
