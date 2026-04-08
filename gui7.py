import gradio as gr
import requests
import subprocess
import re

# Replace with your actual API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

def fix_code(code, language, mode, model):
    """
    Fix and/or optimize the provided code using Mistral AI API.
    
    Args:
        code (str): The code to be fixed/optimized
        language (str): Programming language of the code
        mode (str): Fix mode (errors only, optimize, or explain)
        model (str): AI model to use for processing
        
    Returns:
        tuple: (AI response text, extracted corrected code)
    """
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    prompt = f"Fix and optimize the following {language} code:\n{code}" if mode != "Fix Errors Only" else f"Fix the following {language} code:\n{code}"
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        
        # Extract corrected code using regex
        corrected_code_match = re.search(r"```(?:\w+\n)?([\s\S]+?)```", ai_response)
        corrected_code = corrected_code_match.group(1) if corrected_code_match else "Could not extract corrected code."

        return ai_response, corrected_code
    else:
        return f"Error: {response.status_code}, {response.text}", ""

def run_python_code(code):
    try:
        result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        error = result.stderr.strip()
        return output if output else error if error else "Execution completed with no output."
    except Exception as e:
        return str(e)

# Available options
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]
modes = ["Fix Errors Only", "Fix Errors + Optimize", "Fix + Optimize + Explain"]
models = ["mistral-tiny", "mistral-medium", "mistral-large"]

# Custom CSS for styling
css = """
#title { text-align: center; font-size: 24px; font-weight: bold; }
#subtitle { text-align: center; font-size: 18px; font-style: italic; }
.gradio-button { background-color: #6B46C1 !important; color: white !important; }
"""

# Gradio UI Layout
with gr.Blocks(css=css) as iface:
    gr.Markdown("# 🩺 AI Code Doctor - Fix, Optimize & Run", elem_id="title")
    gr.Markdown("### The Ultimate Debugging Assistant", elem_id="subtitle")

    with gr.Row():
        with gr.Column(scale=2):
            code_input = gr.Textbox(lines=15, placeholder="Paste Your Code Here:", label="Paste Your Code")
        with gr.Column(scale=1):
            language_dropdown = gr.Dropdown(choices=languages, label="Select Language")
            mode_radio = gr.Radio(choices=modes, label="Select Mode")
            model_dropdown = gr.Dropdown(choices=models, label="Select AI Model")
            fix_button = gr.Button("🛠 Fix Code")

    output_box = gr.Textbox(label="AI Output (Fixed Code & Explanation)", lines=15)

    with gr.Row():
        with gr.Column(scale=2):
            corrected_code_box = gr.Textbox(label="Corrected Code", lines=15)
        with gr.Column(scale=1):
            execution_output = gr.Textbox(label="Execution Output", lines=12)
            run_button = gr.Button("▶ Run My Code")

    # Run Code Button Moved Below Execution Output


    fix_button.click(fix_code, inputs=[code_input, language_dropdown, mode_radio, model_dropdown], outputs=[output_box, corrected_code_box])
    run_button.click(run_python_code, inputs=[corrected_code_box], outputs=execution_output)

iface.launch()