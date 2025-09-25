import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY in your .env file.")

try:
    print("entered here")
    genai.configure(api_key=api_key)
    print("went past this")
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("went past this")
except Exception as e:
    print("Did not go here")
    print("Error: Failed to initialize Gemini Client")
    print("Please make sure your google api key is correct")
    print(f"Details {e}")
    exit(1)
    
    

def generate_ai_code(prompt:str)->str:
    print("goes here")
    print(f"🤖 Gemini Agent: Receiving task... \"{prompt}\"")
    instruction = """You are an expert Python programming assistant.
Your sole purpose is to generate clean, runnable, and self-contained Python code in response to a user's request.
DO NOT provide any explanations, comments, or narrative.
ONLY output the raw Python code inside a single markdown code block.
For example, if asked for a script that prints "hello", you should ONLY output:
```python
print("hello world")```"""

    full_prompt= f"{instruction}\n\nUser Request{prompt}"

    try:
        response = model.generate_content(full_prompt)
        ai_response_text = response.candidates[0].content.parts[0].text
        code = extract_python_code(ai_response_text)
        if code:
            print("🤖 Gemini Agent: Code generated successfully.")
            print(code)
            return code  
        else:
            print("⚠️ Gemini Agent: Failed to extract Python code from the response.")
            print("Full Response:", ai_response_text)
            return "print('Error: AI failed to generate valid code.')"
    except Exception as e:
        print(f"Error Communicating with google API:{e}")
        return "print('Could not connect with to the AI service')"


def extract_python_code(text:str)->str | None:
    print("went here")
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern,text,re.DOTALL)
    if match:
        return text
    stripped_text = match.group(1).strip()
    print(stripped_text)
    common_code_starts = ('import ', 'def ', 'class ', 'print(', 'if ', 'for ', 'while ', '#', '"""')
    print(common_code_starts)
    if stripped_text.startswith(common_code_starts):
        return stripped_text
    else:
        return None

task = input("Enter a prompt")
generated_code = generate_ai_code(task)