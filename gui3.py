import gradio as gr
import requests

# Replace with your actual Mistral API key
API_KEY = "iSZSe54xfHDb4ONhaKFlwls7JuTKZNER"

def fix_code(code, language, mode):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    if mode == "Fix Errors Only":
        prompt = f"Fix the following {language} code and explain the corrections:\n{code}"
    else:
        prompt = f"Fix and optimize the following {language} code for better performance, readability, and efficiency. Explain the corrections and improvements:\n{code}"
    
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

# Mode options
modes = ["Fix Errors Only", "Fix Errors + Optimize"]

# Gradio UI with additional optimization mode selection
iface = gr.Interface(
    fn=fix_code,
    inputs=[
        gr.Textbox(lines=10, placeholder="Paste your code here..."),
        gr.Dropdown(choices=languages, label="Select Language"),
        gr.Radio(choices=modes, label="Select Mode")
    ],
    outputs="text",
    title="AI Code Fixer & Optimizer (Multi-Language)",
    description="Paste your code, select a programming language, choose mode (fix errors or optimize), and AI will improve it!"
)

iface.launch()
