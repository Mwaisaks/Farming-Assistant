"""One-shot uploader to HuggingFace Spaces — bypasses git binary restrictions."""
import os
from huggingface_hub import HfApi

token = os.getenv("HF_TOKEN") or input("Paste your HuggingFace WRITE token: ").strip()

api = HfApi(token=token)

print("Uploading to Mwaisaka/Krishi ...")
api.upload_folder(
    folder_path=".",
    repo_id="Mwaisaka/Krishi",
    repo_type="space",
    ignore_patterns=[
        "venv/**",
        ".git/**",
        ".env",
        ".claude/**",
        "**/__pycache__/**",
        "**/*.pyc",
        "deploy_hf.py",
    ],
)
print("Done! Visit https://huggingface.co/spaces/Mwaisaka/Krishi")
