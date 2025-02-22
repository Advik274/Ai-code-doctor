import gradio as gr
import requests

# Replace with your actual Mistral API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

def fix_code(code, language):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"Fix the following {language} code and explain the corrections:\n{code}"
    
    payload = {
        "model": "mistral-medium",  # You can use "mistral-tiny" or "mistral-large"
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Available programming languages
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]

# Gradio UI with a dropdown for language selection
iface = gr.Interface(
    fn=fix_code,
    inputs=[
        gr.Textbox(lines=10, placeholder="Paste your code here..."),
        gr.Dropdown(choices=languages, label="Select Language")
    ],
    outputs="text",
    title="AI Code Fixer (Multi-Language)",
    description="Paste your code, select a programming language, and AI will fix it!"
)

iface.launch()
