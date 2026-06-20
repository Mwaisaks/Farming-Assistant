"""Quick smoke test for stt, tts, rag, and llm modules."""
import os, sys

print("=" * 50)

# ── 1. TTS ────────────────────────────────────────────────────────────────────
print("\n[1/4] Testing tts.py...")
from pipeline.tts import speak, cleanup

path = speak("Namaste! Main Krishi hoon, aapka prakriti kheti sahayak.")
assert os.path.exists(path), "TTS output file not created"
print(f"  ✓ TTS OK — saved to {path}")
cleanup(path)
print("  ✓ Cleanup OK")

# ── 2. RAG ────────────────────────────────────────────────────────────────────
print("\n[2/4] Testing rag.py...")
from pipeline import rag

rag.init()
result = rag.retrieve("tomato leaf blight disease remedy")
assert len(result) > 50, "RAG returned too little content"
print(f"  ✓ RAG OK — retrieved {len(result)} chars")
print(f"  Preview: {result[:120]}...")

# ── 3. LLM ────────────────────────────────────────────────────────────────────
print("\n[3/4] Testing llm.py...")
from pipeline.llm import ask

sample_context = rag.retrieve("powdery mildew white powder on leaves")
response = ask(
    query="My tomato leaves have white powder on them, what should I do?",
    context=sample_context,
    feature_type="disease",
)
assert len(response) > 20, "LLM returned empty response"
print(f"  ✓ LLM OK")
print(f"  Response preview: {response[:200]}...")

# ── 4. STT (import-only check — requires mic/audio file to fully test) ────────
print("\n[4/4] Testing stt.py (import only — no audio file needed)...")
from pipeline.stt import transcribe
print("  ✓ STT import OK — full test requires an audio file")

print("\n" + "=" * 50)
print("All module checks passed! Ready to run app.py")
print("=" * 50)
