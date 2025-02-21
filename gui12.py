import gradio as gr
import requests
import subprocess
import re

# Replace with your actual API key
API_KEY = "iSZSe54xfHDb4ONhaKFlwls7JuTKZNER"

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
    return match.group(1) if match else response

def run_python_code(code):
    try:
        result = subprocess.run(["python", "-c", code],
                                capture_output=True, text=True, timeout=5)
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
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": user_input}]}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Available options
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]
modes = ["Fix Errors Only", "Fix Errors + Optimize", "Fix + Optimize + Explain"]
models = ["mistral-tiny", "mistral-medium", "mistral-large"]

# Custom CSS with interactive animations
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
#fix_button, #run_button, #chat_button {
    background-color: #6B46C1 !important;
    color: white !important;
    font-weight: bold;
    padding: 10px 15px;
    border-radius: 8px;
    margin-top: 10px;
    transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out;
}
#fix_button:hover, #run_button:hover, #chat_button:hover {
    background-color: #8a5bc9 !important;
    transform: scale(1.05);
}
.fade-section {
    opacity: 1;
    transition: opacity 0.5s ease-in-out;
}
"""

with gr.Blocks(css=css) as iface:
    gr.Markdown("# 🩺 AI Code Doctor - Fix, Optimize & Run", elem_id="title")
    gr.Markdown("### The Ultimate Debugging Assistant", elem_id="subtitle")
    
    # Mode selector to toggle between Code Debug and Chat Mode
    mode_selector = gr.Radio(choices=["Code Debug", "Chat Mode"], label="Select Mode", value="Code Debug")
    
    # Code Debug Section with fade animation class
    with gr.Column(visible=True, elem_classes="fade-section") as code_section:
        with gr.Row():
            with gr.Column(scale=2):
                code_input = gr.Textbox(lines=16, placeholder="Paste Your Code Here:", label="Paste Your Code")
            with gr.Column(scale=1):
                language_dropdown = gr.Dropdown(choices=languages, label="Select Language")
                mode_radio = gr.Radio(choices=modes, label="Select Mode")
                model_dropdown = gr.Dropdown(choices=models, label="Select AI Model")
                fix_button = gr.Button("🛠 Fix Code", elem_id="fix_button")
        output_box = gr.Textbox(label="AI Output (Fixed Code & Explanation)", lines=15)
        with gr.Row():
            with gr.Column(scale=2):
                corrected_code_box = gr.Textbox(label="Corrected Code", lines=16)
            with gr.Column(scale=1):
                execution_output = gr.Textbox(label="Execution Output", lines=12)
                run_button = gr.Button("▶ Run My Code", elem_id="run_button")
        fix_button.click(fix_code, inputs=[code_input, language_dropdown, mode_radio, model_dropdown],
                         outputs=[output_box, corrected_code_box])
        run_button.click(run_code, inputs=[corrected_code_box, language_dropdown], outputs=execution_output)
    
    # Chat Mode Section with fade animation class
    with gr.Column(visible=False, elem_classes="fade-section") as chat_section:
        chat_input = gr.Textbox(lines=5, placeholder="Ask AI something...", label="Chat Input")
        chat_model_dropdown = gr.Dropdown(choices=models, label="Select AI Model", value="mistral-tiny")
        chat_button = gr.Button("💬 Send Message", elem_id="chat_button")
        chat_output = gr.Textbox(label="AI Chat Response", lines=10)
        chat_button.click(chatbot_response, inputs=[chat_input, chat_model_dropdown], outputs=chat_output)
    
    # Function to toggle mode visibility
    def switch_mode(selected_mode):
        if selected_mode == "Code Debug":
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)
    
    mode_selector.change(switch_mode, inputs=[mode_selector], outputs=[code_section, chat_section])
    
iface.launch()
