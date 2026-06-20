import os
import shutil
import tempfile
import gradio as gr
from dotenv import load_dotenv

from pipeline import rag, stt, tts, llm

load_dotenv()

# ── RAG initialisation (runs once at startup) ─────────────────────────────────
rag.init()


# ── Core pipeline ─────────────────────────────────────────────────────────────

def process(audio_path: str, feature_type: str) -> tuple[str, str, str]:
    """
    Full pipeline: audio → transcript → LLM response → speech.
    Returns (transcript, response_text, audio_output_path).
    """
    if audio_path is None:
        return "No audio received.", "Please record your question first.", None

    transcript = stt.transcribe(audio_path)
    if not transcript:
        return "[Could not understand audio]", "Please speak clearly and try again.", None

    context = rag.retrieve(transcript)
    response_text = llm.ask(transcript, context, feature_type)
    audio_out = tts.speak(response_text)

    return transcript, response_text, audio_out


def disease_pipeline(audio_path: str):
    return process(audio_path, "disease")


def education_pipeline(audio_path: str):
    return process(audio_path, "education")


# ── Gradio UI ─────────────────────────────────────────────────────────────────

CSS = """
#title { text-align: center; font-size: 2em; margin-bottom: 0.2em; }
#subtitle { text-align: center; color: #555; margin-bottom: 1.5em; }
.tab-label { font-size: 1.1em; }
"""

def build_tab(label: str, pipeline_fn, example_prompt: str):
    with gr.Column():
        gr.Markdown(f"### {label}")
        gr.Markdown(f"*{example_prompt}*")

        audio_in = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="🎤 Speak your question",
            elem_classes=["large-input"],
        )

        submit_btn = gr.Button("Submit", variant="primary", size="lg")

        transcript_box = gr.Textbox(
            label="📝 What I heard",
            lines=2,
            interactive=False,
            placeholder="Your words will appear here...",
        )
        response_box = gr.Textbox(
            label="🌿 Krishi's Advice",
            lines=6,
            interactive=False,
            placeholder="Advice will appear here...",
        )
        audio_out = gr.Audio(
            label="🔊 Listen to advice",
            type="filepath",
            autoplay=True,
        )

        submit_btn.click(
            fn=pipeline_fn,
            inputs=[audio_in],
            outputs=[transcript_box, response_box, audio_out],
        )


with gr.Blocks(css=CSS, title="Krishi — Natural Farming Consultant") as demo:
    gr.Markdown("# 🌾 Krishi — Your Natural Farming Consultant", elem_id="title")
    gr.Markdown(
        "Ask in **Hindi, English, or mixed** — Krishi understands you.",
        elem_id="subtitle",
    )

    with gr.Tabs():
        with gr.Tab("🦠 Disease & Treatment", elem_classes=["tab-label"]):
            build_tab(
                label="Describe your crop problem",
                pipeline_fn=disease_pipeline,
                example_prompt='Try: "Meri tomato ke patte pe kale dabbe aa rahe hain" or "My wheat leaves are turning yellow from the bottom"',
            )

        with gr.Tab("📚 Farming Education", elem_classes=["tab-label"]):
            build_tab(
                label="Ask about natural farming",
                pipeline_fn=education_pipeline,
                example_prompt='Try: "Jeevamrutha kaise banate hain?" or "What is companion planting and how do I start?"',
            )


if __name__ == "__main__":
    demo.launch()
