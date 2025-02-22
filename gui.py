import gradio as gr
import requests

# Replace with your actual Mistral API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

def fix_code(code):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mistral-medium",  # You can use "mistral-tiny" or "mistral-large"
        "messages": [{"role": "user", "content": f"Fix this Python code:\n{code}"}]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Gradio UI
iface = gr.Interface(
    fn=fix_code,
    inputs=gr.Textbox(lines=10, placeholder="Paste your Python code here..."),
    outputs="text",
    title="AI Code Fixer",
    description="Paste your Python code, and AI will fix it!",
)

iface.launch()
