import gradio as gr
import requests
import subprocess
import re

# Replace with your actual API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

# Function to interact with Mistral AI
def chat_with_mistral(user_message, chat_history):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    messages = [{"role": "user", "content": msg} for msg in chat_history] + [{"role": "user", "content": user_message}]
    
    payload = {"model": "mistral-medium", "messages": messages}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        chat_history.append(user_message)
        chat_history.append(ai_response)
        return chat_history
    else:
        return ["Error: Could not fetch response from Mistral AI."]

# Function to fix code
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

# Gradio UI
with gr.Blocks() as iface:
    gr.Markdown("# 🩺 AI Code Doctor & Chatbot")

    mode_toggle = gr.Radio(["Code Mode", "Chat Mode"], label="Select Mode", value="Code Mode")

    # Chat Mode UI
    with gr.Column(visible=False) as chat_mode_ui:
        gr.Markdown("### 💬 Chat with Mistral AI")
        chat_input = gr.Textbox(label="Your Message")
        chat_output = gr.Chatbot(label="Mistral AI Chat")
        chat_button = gr.Button("Send")

        chat_history = gr.State([])

        chat_button.click(chat_with_mistral, inputs=[chat_input, chat_history], outputs=chat_output)

    # Code Mode UI
    with gr.Column(visible=True) as code_mode_ui:
        gr.Markdown("### 🔻 Input Code & Options")
        code_input = gr.Code(language="python", lines=15, label="Paste Your Code Here")
        language_dropdown = gr.Dropdown(choices=languages, label="Select Language")
        mode_radio = gr.Radio(choices=modes, label="Select Mode")
        model_dropdown = gr.Dropdown(choices=models, label="Select AI Model")
        fix_button = gr.Button("🛠 Fix Code")

        gr.Markdown("### ✅ Fixed Code & Execution")
        output_box = gr.Textbox(label="AI Output (Fixed Code & Explanation)", lines=8, interactive=False)
        corrected_code_box = gr.Code(language="python", lines=12, label="Corrected Code", interactive=False)
        execution_output = gr.Textbox(label="Execution Output", lines=5, interactive=False)
        run_button = gr.Button("▶ Run My Code")

        fix_button.click(fix_code, inputs=[code_input, language_dropdown, mode_radio, model_dropdown], outputs=[output_box, corrected_code_box])
        run_button.click(run_code, inputs=[corrected_code_box, language_dropdown], outputs=execution_output)

    def switch_mode(mode):
        if mode == "Chat Mode":
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)

    mode_toggle.change(switch_mode, inputs=mode_toggle, outputs=[chat_mode_ui, code_mode_ui])

iface.launch()
