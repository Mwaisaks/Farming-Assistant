I'm building a Voice-Based Natural Farming Consultant prototype for a
foundation assignment. Deadline: June 20. Evaluation: Technical 40%,
Empathy/UX 30%, AI/Prompt 30%.

OPTION: B — Multilevel Natural Farming Consultant
FEATURES TO BUILD (2 of 4):

  1. Disease Identification & Treatment — farmer describes symptoms,
     get organic remedy back
  2. Natural Farming Education — explain multilevel cropping,
     companion planting, soil health

USER: A farmer in rural India transitioning to natural farming.
May speak Hindi, English, or mixed. Not tech-savvy. Voice-first.

STACK:

- UI: Gradio (mobile-friendly, gives live URL)
- STT: Whisper (openai-whisper library, base model)
- LLM: Google Gemini 1.5 Flash via google-generativeai SDK
- TTS: gTTS (Google Text-to-Speech, outputs mp3)
- RAG: ChromaDB + sentence-transformers for farming document retrieval
- Hosting: HuggingFace Spaces (Gradio SDK)
- Language: Python

REPO STRUCTURE TO CREATE:
farming-consultant/
├── app.py              # Main Gradio app
├── pipeline/
│   ├── stt.py          # Whisper transcription
│   ├── llm.py          # Gemini call with system prompt
│   ├── tts.py          # gTTS text to speech
│   └── rag.py          # ChromaDB retrieval
├── docs/               # Farming PDFs/text corpus for RAG
├── requirements.txt
├── README.md
└── .env.example

SYSTEM PROMPT DESIGN (for llm.py):

- Role: "You are Krishi, a natural farming consultant..."
- Constrain to farming domain only (guardrails)
- Respond in the same language the farmer used (Hindi/English/mixed)
- Keep answers short, practical, jargon-free
- For disease: always give (1) likely cause (2) organic remedy (3) prevention
- For education: use simple analogies, reference Indian farming context
- Never recommend chemical pesticides or fertilizers

RAG STRATEGY:

- Chunk 3-5 farming documents into ChromaDB at startup
- On each query, retrieve top 2 relevant chunks
- Inject chunks into Gemini prompt as context
- Sources: use freely available text (NCOF guidelines,
  natural farming government docs — we'll add these as .txt files)

GRADIO UI LAYOUT:

- Title: "🌾 Krishi — Your Natural Farming Consultant"
- Two tabs: "Disease & Treatment" | "Farming Education"  
- Each tab: mic input → transcription display → AI response (text)
  → audio playback
- Mobile-optimized, large text, simple layout
- Show a "Listening..." state indicator

ENV VARIABLES NEEDED:

- GEMINI_API_KEY

DELIVERABLES I NEED AT THE END:

1. Working app.py that runs locally with: python app.py
2. requirements.txt with pinned versions
3. README.md with sections:
   - What it does
   - Tech stack
   - Prompt design & guardrails
   - Localization approach
   - How to run locally
   - How to deploy to HuggingFace Spaces
4. .env.example file

BUILD ORDER (do these in sequence, confirm each works before next):
  Step 1: Scaffold the repo structure and requirements.txt
  Step 2: Build stt.py — takes audio file path, returns transcript string
  Step 3: Build tts.py — takes text string, saves mp3, returns file path
  Step 4: Build rag.py — loads docs/, chunks, builds ChromaDB,
          has retrieve(query) function
  Step 5: Build llm.py — takes (query, retrieved_context, feature_type),
          calls Gemini, returns response string
  Step 6: Build app.py — wires everything into Gradio UI
  Step 7: Test full pipeline with a sample audio input
  Step 8: Write README.md

Do NOT skip steps or combine them. Confirm each step works before moving on.
Start with Step 1 now.

A few things to note:

- we're gonna use a GROQ_API_KEY instead of GEMINI_API_KEY
- 2-3 farming text files — drop these into docs/ as .txt. Good sources:

India's NCOF (National Centre of Organic Farming) guidelines — IN THE FOLDER ALREADY AS Field-Guide-for-Natural-Farming.pdf
Subhash Palekar's natural farming principles — widely available summaries online - <https://yakeclimate.com/subhash-palekar-natural-farming-principles-benefits-and-practices/#:~:text=Frequently%20Asked%20Questions-,What%20are%20the%20main%20principles%20of%20Subhash%20Palekar's%20organic%20farming,health%2C%20biodiversity%2C%20and%20sustainability>.
