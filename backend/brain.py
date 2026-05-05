import os
import json
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def parse_intent(user_prompt: str) -> dict:
    current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
    
    system_prompt = f"""
    You are Z-OS, an advanced local OS automation core. 
    Current System Time: {current_time}. 
    
    Convert the user's command into a strict JSON execution plan.
    Supported actions: 
    - "navigate" (url param)
    - "search_web" (query param)
    - "type" (text param)
    - "press_key" (key param)
    - "desktop_mode" (no params)
    - "run_command" (command param)
    - "open_app" (app_name param)
    - "system_reply" (message param)
    - "wait" (seconds param, integer)
    - "force_close" (app_exe param, e.g., "notepad.exe")
    
    CRITICAL RULES:
    1. THE REASONING ENGINE: You MUST think step-by-step in the "thought_process" field before generating the steps array. Analyze the most efficient way to execute the user's request.
    2. BROWSER RULE: If the user asks to open a website or search, ONLY use "navigate" or "search_web". These automatically handle opening the browser. 
    3. NEVER invent fake "www" URLs. Use "search_web" if unknown.
    4. PUNCTUATION & TONE: If you use "system_reply", use perfect, polite English. DO NOT use ALL CAPS.
    5. ONLY return raw JSON. No markdown, no backticks.
    
    Format: 
    {{
        "thought_process": "Briefly reason about the most efficient execution path...",
        "steps": [{{ "action": "...", ... }}]
    }}
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
    )
    
    response_text = completion.choices[0].message.content
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        clean_text = response_text.replace("`", "").replace("json", "").strip()
        return json.loads(clean_text)