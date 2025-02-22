import gradio as gr
import requests
import subprocess
import re

# Replace with your actual API key
API_KEY = "cRPZfgYcTSluoLwakjvemAGlzUpOYOMy"

def fix_code(code, language, mode, model):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    if mode == "Fix Errors Only":
        prompt = (f"Fix the following {language} code:\n{code}\n"
                  "Return only the corrected code without any explanation.")
    elif mode == "Fix Errors + Optimize":
        prompt = (f"Fix and optimize the following {language} code:\n{code}\n"
                  "Return the corrected code along with a few brief optimization suggestions.")
    elif mode == "Fix + Optimize + Explain":
        prompt = (f"Fix, optimize, and explain the following {language} code:\n{code}\n"
                  "Return the corrected code, optimization suggestions, and a brief, user-friendly explanation of the fixes.")
    else:
        prompt = f"Fix and optimize the following {language} code:\n{code}"
        
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

def chatbot_response(user_input, model, mood):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    # Build prompt based on selected mood
    if mood == "Happy":
        prompt = f"Respond to the following query in a cheerful, happy tone:\n{user_input}"
    elif mood == "Anger":
        prompt = f"Respond to the following query in a blunt, angry tone:\n{user_input}"
    elif mood == "Love":
        prompt = f"Respond to the following query in a warm, loving tone:\n{user_input}"
    elif mood == "Explanation":
        prompt = f"Provide a detailed and clear explanation for the following query:\n{user_input}"
    elif mood == "One Liner":
        prompt = f"Give a witty one-liner answer to the following query:\n{user_input}"
    elif mood == "Over Explainer":
        prompt = f"Provide an overly detailed, verbose explanation for the following query:\n{user_input}"
    else:  # Default or Neutral
        prompt = f"Answer the following query:\n{user_input}"
    
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Available options
languages = ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript", "PHP", "Ruby"]
modes = ["Fix Errors Only", "Fix Errors + Optimize", "Fix + Optimize + Explain"]
models = ["mistral-tiny", "mistral-medium", "mistral-large"]
chat_moods = ["Neutral", "Happy", "Anger", "Love", "Explanation", "One Liner", "Over Explainer"]

# Custom CSS for styling
css = """
#header_debug {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    background: -webkit-linear-gradient(left, #6B46C1, #FFA500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
#header_chat {
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
#fix_button, #run_button, #chat_button {
    background-color: #6B46C1 !important;
    color: white !important;
    font-weight: bold;
    padding: 10px 15px;
    border-radius: 8px;
    margin-top: 10px;
}
"""

with gr.Blocks(css=css) as iface:
    # Two headers for different modes (only one will be visible at a time)
    header_debug = gr.Markdown("# 🩺 AI Code Doctor – Fix, Optimize & Run", elem_id="header_debug")
    header_chat = gr.Markdown("# 🩺 AI Code Doctor Chat", elem_id="header_chat", visible=False)
    gr.Markdown("### The Ultimate Debugging Machine by Arnav", elem_id="subtitle")
    
    # Mode selector to toggle between Code Debug and Chat Mode
    mode_selector = gr.Radio(choices=["Code Debug", "Chat Mode"], label="Select Mode", value="Code Debug")
    
    # Code Debug Section
    with gr.Column(visible=True) as code_section:
        with gr.Row():
            with gr.Column(scale=2):
                code_input = gr.Textbox(lines=16, placeholder="Errors in the code? \nNo problem give it to me", label="Paste Your Code")
            with gr.Column(scale=1):
                language_dropdown = gr.Dropdown(choices=languages, label="Select Language")
                mode_radio = gr.Radio(choices=modes, label="Select Fix Mode")
                model_dropdown = gr.Dropdown(choices=models, label="Select AI Model")
                fix_button = gr.Button("🛠 Fix Code", elem_id="fix_button")
        output_box = gr.Textbox(label="AI Output", lines=15)
        with gr.Row():
            with gr.Column(scale=2):
                corrected_code_box = gr.Textbox(label="Corrected Code", placeholder="It will extract the code automatically from the AI Output", lines=16)
            with gr.Column(scale=1):
                execution_output = gr.Textbox(label="Execution Output", lines=12)
                run_button = gr.Button("▶ Run My Code", elem_id="run_button")
        fix_button.click(fix_code, inputs=[code_input, language_dropdown, mode_radio, model_dropdown],
                         outputs=[output_box, corrected_code_box])
        run_button.click(run_code, inputs=[corrected_code_box, language_dropdown], outputs=execution_output)
      
    # Chat Mode Section
    with gr.Column(visible=False) as chat_section:
        chat_input = gr.Textbox(lines=5, placeholder="Ask AI something...", label="Chat Input")
        chat_model_dropdown = gr.Dropdown(choices=models, label="Select AI Model", value="mistral-tiny")
        chat_mood_dropdown = gr.Dropdown(choices=chat_moods, label="Select Chat Mood", value="Neutral")
        chat_button = gr.Button("💬 Send Message", elem_id="chat_button")
        chat_output = gr.Textbox(label="AI Chat Response", lines=10)
        chat_button.click(chatbot_response, inputs=[chat_input, chat_model_dropdown, chat_mood_dropdown], outputs=chat_output)
    
    # Function to toggle mode visibility and update headers
    def switch_mode(selected_mode):
        if selected_mode == "Code Debug":
            return (gr.update(visible=True), gr.update(visible=False),
                    gr.update(visible=True), gr.update(visible=False))
        else:
            return (gr.update(visible=False), gr.update(visible=True),
                    gr.update(visible=False), gr.update(visible=True))
    
    # Update: outputs are header_debug, header_chat, code_section, chat_section
    mode_selector.change(switch_mode, inputs=[mode_selector],
                         outputs=[header_debug, header_chat, code_section, chat_section])
    
iface.launch()
