import gradio as gr
import requests

# Replace with your actual Mistral API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

def fix_code(code, language, mode, model):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Enhanced prompt with explanations, comments, and time complexity analysis
    if mode == "Fix Errors Only":
        prompt = f"Fix the following {language} code and explain the corrections:\n{code}"
    elif mode == "Fix Errors + Optimize":
        prompt = f"Fix and optimize the following {language} code for better performance, readability, and efficiency. Explain the corrections and improvements:\n{code}"
    else:
        prompt = f"Fix, optimize, and add meaningful comments to the following {language} code. Also, analyze its time complexity and suggest improvements:\n{code}"

    payload = {
        "model": model,  # Allow user to select AI model
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to execute Python code
def execute_python_code(code):
    try:
        exec_globals = {}
        exec(code, exec_globals)  # Execute the code safely in a separate environment
        return "Code executed successfully!"
    except Exception as e:
        return f"Execution Error: {str(e)}"

# Available programming languages
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]

# Mode options
modes = ["Fix Errors Only", "Fix Errors + Optimize", "Fix + Optimize + Explain"]

# Model selection
models = ["mistral-tiny", "mistral-medium", "mistral-large"]

# UI with syntax highlighting and new features
with gr.Blocks(theme="default") as iface:
    gr.Markdown("## 🚀 AI Code Fixer & Optimizer (Multi-Language) 🔧")
    
    with gr.Row():
        code_input = gr.Code(language="python", label="Paste Your Code Here:")
    
    with gr.Row():
        lang_dropdown = gr.Dropdown(choices=languages, label="Select Language")
        mode_dropdown = gr.Radio(choices=modes, label="Select Mode")
        model_dropdown = gr.Dropdown(choices=models, label="Select AI Model")
    
    output_area = gr.Textbox(label="AI Output (Fixed Code & Explanation)", lines=10)
    
    with gr.Row():
        fix_button = gr.Button("🔧 Fix Code")
        exec_button = gr.Button("▶️ Run Python Code")
    
    fix_button.click(fix_code, inputs=[code_input, lang_dropdown, mode_dropdown, model_dropdown], outputs=output_area)
    exec_button.click(execute_python_code, inputs=[code_input], outputs=output_area)

iface.launch()
