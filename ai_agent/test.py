import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv(override=True)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
for m in genai.list_models():
    methods = getattr(m, "supported_generation_methods", [])
    print(f"{m.name} -> {methods}")
