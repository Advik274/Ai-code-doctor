import gradio as gr
import requests
import subprocess

# Replace with your actual Mistral API key
API_KEY = "iSZSe54xfHDb4ONhaKFlwls7JuTKZNER"

def fix_code(code, language, mode, model):
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
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

def run_python_code(code):
    try:
        result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        error = result.stderr.strip()
        return output if output else error if error else "Execution completed with no output."
    except Exception as e:
        return str(e)

# Available programming languages
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]

# Mode options
modes = ["Fix Errors Only", "Fix Errors + Optimize", "Fix + Optimize + Explain"]

# Model options
models = ["mistral-tiny", "mistral-medium", "mistral-large"]

# Custom CSS for styling
css = """
#title {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

#subtitle {
    text-align: center;
    font-size: 18px;
    font-style: italic;
}

.gradio-button {
    background-color: #6B46C1 !important;
    color: white !important;
}
"""

# Gradio UI with updated styles
with gr.Blocks(css=css) as iface:
    gr.Markdown("# 🩺 AI Code Doctor - Fix, Optimize & Run", elem_id="title")
    gr.Markdown("### The Ultimate Debugging Assistant", elem_id="subtitle")
    
    code_input = gr.Textbox(lines=15, placeholder="Paste Your Code Here:", label="Paste Your Code")  # Increased height
    with gr.Row():
        language_dropdown = gr.Dropdown(choices=languages, label="Select Language")
        mode_radio = gr.Radio(choices=modes, label="Select Mode")
        model_dropdown = gr.Dropdown(choices=models, label="Select AI Model")

    output_box = gr.Textbox(label="AI Output (Fixed Code & Explanation)", lines=15)  # Increased height
    execution_output = gr.Textbox(label="Execution Output", lines=10)

    with gr.Row():
        fix_button = gr.Button("🛠 Fix Code")
        run_button = gr.Button("▶ Run Python Code")

    fix_button.click(fix_code, inputs=[code_input, language_dropdown, mode_radio, model_dropdown], outputs=output_box)
    run_button.click(run_python_code, inputs=[code_input], outputs=execution_output)

iface.launch()
