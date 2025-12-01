import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env values every run, even if the shell already has variables set
load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY in your .env file.")

genai.configure(api_key=api_key)

# Get the model from the environment variable
env_model = os.getenv("GEMINI_MODEL")
if env_model:
    print(f"Using model from GEMINI_MODEL: {env_model}")

# Initialize the model
try:
    model = genai.GenerativeModel(env_model)
except Exception as e:
    print("Error: Failed to initialize Gemini Client")
    print("Details:", e)
    exit(1)


def generate_ai_code(prompt: str) -> str:
    print(f" Gemini Agent: Receiving task... \"{prompt}\"")
    instruction = """You are an expert Python programming assistant.
Your sole purpose is to generate clean, runnable, and self-contained Python code in response to a user's request.
DO NOT provide any explanations, comments, or narrative.
ONLY output the raw Python code inside a single markdown code block.
For example, if asked for a script that prints "hello", you should ONLY output:
"""

    full_prompt = f"{instruction}\n\nUser Request: {prompt}"

    try:
        response = model.generate_content(full_prompt)
        ai_response_text = response.candidates[0].content.parts[0].text
        code = extract_python_code(ai_response_text)
        if code:
            print("Gemini Agent: Code generated successfully.")
            print(code)
            return code
        else:
            print("Gemini Agent: Failed to extract Python code from the response.")
            print("Full Response:", ai_response_text)
            return "print('Error: AI failed to generate valid code.')"
    except Exception as e:
        print(f"Error Communicating with google API: {e}")
        return "print('Could not connect with the AI service')"


def extract_python_code(text: str) -> str | None:
    print("went here")
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        stripped_text = match.group(1).strip()
        return stripped_text
    # If no triple backticks, check if starts like code
    common_code_starts = ('import ', 'def ', 'class ', 'print(', 'if ', 'for ', 'while ', '#', '"""')
    t = text.strip()
    if t.startswith(common_code_starts):
        return t
    return None


if __name__ == "__main__":
    task = input("Enter a prompt : ")
    generated_code = generate_ai_code(task)
    
    # Save the response to app.txt (overwrites existing content)
    # Get the script's directory and navigate to the root code/app.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)  # Go up one level from ai_agent/ to root
    app_txt_path = os.path.join(root_dir, "code", "app.txt")
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(app_txt_path), exist_ok=True)
        # Open in write mode to replace old content with new content
        with open(app_txt_path, "w", encoding="utf-8") as f:
            f.write(generated_code)
        print(f"\n Response saved to {app_txt_path} (replaced previous content)")
    except Exception as e:
        print(f"Error saving to file: {e}")