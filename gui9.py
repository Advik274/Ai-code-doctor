import gradio as gr
import requests
import subprocess
import re

# Replace with your actual API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

def fix_code(code, language, mode, model):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    prompt = f"Fix and optimize the following {language} code:\n{code}" if mode != "Fix Errors Only" else f"Fix the following {language} code:\n{code}"
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        corrected_code = extract_code(ai_response)
        return ai_response, corrected_code
    else:
        return f"Error: {response.status_code}, {response.text}", ""

def extract_code(response):
    """Extracts code from AI response safely."""
    match = re.search(r"```(?:\w+\n)?([\s\S]+?)```", response)
    return match.group(1) if match else response  # Returns full response if no code found

def run_python_code(code):
    try:
        result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        error = result.stderr.strip()
        return output if output else error if error else "Execution completed with no output."
    except Exception as e:
        return str(e)

def run_code(code, language):
    """Runs code only if it is Python, otherwise shows a warning."""
    if language == "Python":
        return run_python_code(code)
    else:
        return "⚠ Running non-Python code is not supported yet!"

# Available options
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]
modes = ["Fix Errors Only", "Fix Errors + Optimize", "Fix + Optimize + Explain"]
models = ["mistral-tiny", "mistral-medium", "mistral-large"]

# Custom CSS for Modern UI
css = """
#title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    background: -webkit-linear-gradient(left, #6B46C1, #FFA500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#subtitle {
    text-align: center;
    font-size: 18px;
    font-style: italic;
    color: #ddd;
}

.gradio-button {
    background-color: #6B46C1 !important;
    color: white !important;
    font-weight: bold;
    padding: 10px 15px;
    border-radius: 8px;
    transition: all 0.3s ease-in-out;
}

.gradio-button:hover {
    background-color: #FFA500 !important;
    transform: scale(1.05);
}

.gradio-container {
    background-color: #1E1E1E;
    color: white;
    padding: 20px;
    border-radius: 10px;
}

.code-box {
    background-color: #2E2E2E;
    color: #FFF;
    font-family: monospace;
    padding: 10px;
    border-radius: 5px;
    white-space: pre-wrap;
}
"""

# Gradio UI Layout
with gr.Blocks(css=css) as iface:
    gr.Markdown("# 🩺 AI Code Doctor - Fix, Optimize & Run", elem_id="title")
    gr.Markdown("### The Ultimate Debugging Assistant", elem_id="subtitle")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 🔻 Input Code & Options", elem_id="section-title")
            code_input = gr.Code(language="python", lines=15, label="Paste Your Code Here")
            language_dropdown = gr.Dropdown(choices=languages, label="Select Language")
            mode_radio = gr.Radio(choices=modes, label="Select Mode")
            model_dropdown = gr.Dropdown(choices=models, label="Select AI Model")
            fix_button = gr.Button("🛠 Fix Code", elem_id="fix_button")

        with gr.Column(scale=2):
            gr.Markdown("### ✅ Fixed Code & Execution", elem_id="section-title")
            output_box = gr.Textbox(label="AI Output (Fixed Code & Explanation)", lines=8, interactive=False)
            corrected_code_box = gr.Code(language="python", lines=12, label="Corrected Code", interactive=False)
            execution_output = gr.Textbox(label="Execution Output", lines=5, interactive=False)
            run_button = gr.Button("▶ Run My Code", elem_id="run_button")

    fix_button.click(fix_code, inputs=[code_input, language_dropdown, mode_radio, model_dropdown], outputs=[output_box, corrected_code_box])
    run_button.click(run_code, inputs=[corrected_code_box, language_dropdown], outputs=execution_output)

iface.launch()
