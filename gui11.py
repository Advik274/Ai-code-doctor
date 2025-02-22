import gradio as gr
import requests
import subprocess
import re

# Replace with your actual API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

def fix_code(code, language, fix_mode, model):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # Use different prompts based on the selected fix mode.
    if fix_mode == "Fix Errors Only":
        prompt = f"Fix the following {language} code:\n{code}"
    else:
        prompt = f"Fix and optimize the following {language} code:\n{code}"
        
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception as e:
        return f"Request error: {str(e)}", ""
    
    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        corrected_code = extract_code(ai_response)
        return ai_response, corrected_code
    else:
        return f"Error: {response.status_code}, {response.text}", ""

def extract_code(response):
    """Extracts code from AI response safely."""
    match = re.search(r"```(?:\w+\n)?([\s\S]+?)```", response)
    return match.group(1) if match else response  # Return full response if no code block is found

def run_python_code(code):
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )
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

def chatbot_response(user_input, model):
    """Handles chatbot interactions."""
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": user_input}]}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception as e:
        return f"Request error: {str(e)}"
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Available options
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]
modes = ["Code Fixing & Execution", "Chat Mode"]
fix_modes = ["Fix Errors Only", "Fix Errors + Optimize", "Fix + Optimize + Explain"]
models = ["mistral-tiny", "mistral-medium", "mistral-large"]

# Gradio UI Layout
with gr.Blocks() as iface:
    gr.Markdown("# 🩺 AI Code Doctor - Fix, Optimize & Run")
    gr.Markdown("### The Ultimate Debugging Assistant")

    mode_selector = gr.Radio(choices=modes, label="Select Mode", value="Code Fixing & Execution")

    # Code fixing section
    with gr.Row(visible=True) as code_section:
        with gr.Column():
            code_input = gr.Code(language="python", lines=15, label="Paste Your Code Here")
            language_dropdown = gr.Dropdown(choices=languages, label="Select Language", value="Python")
            fix_mode_radio = gr.Radio(choices=fix_modes, label="Select Fix Mode", value="Fix Errors Only")
            model_dropdown = gr.Dropdown(choices=models, label="Select AI Model", value="mistral-tiny")
            fix_button = gr.Button("🛠 Fix Code")

        with gr.Column():
            output_box = gr.Textbox(label="AI Output (Fixed Code & Explanation)", lines=8, interactive=False)
            corrected_code_box = gr.Code(language="python", lines=12, label="Corrected Code", interactive=False)
            execution_output = gr.Textbox(label="Execution Output", lines=5, interactive=False)
            run_button = gr.Button("▶ Run My Code")
    
    # Chat section
    with gr.Row(visible=False) as chat_section:
        with gr.Column():
            gr.Markdown("### 💬 Chat with AI")
            chat_input = gr.Textbox(label="Ask AI Anything")
            chat_output = gr.Textbox(label="AI Response", lines=5, interactive=False)
            chat_button = gr.Button("💬 Send Message")
    
    def switch_mode(selected_mode):
        if selected_mode == "Code Fixing & Execution":
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)
    
    mode_selector.change(switch_mode, inputs=[mode_selector], outputs=[code_section, chat_section])
    fix_button.click(fix_code, inputs=[code_input, language_dropdown, fix_mode_radio, model_dropdown],
                     outputs=[output_box, corrected_code_box])
    run_button.click(run_code, inputs=[corrected_code_box, language_dropdown], outputs=execution_output)
    chat_button.click(chatbot_response, inputs=[chat_input, model_dropdown], outputs=chat_output)

iface.launch()
