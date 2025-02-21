# AI Code Doctor

AI Code Doctor is an AI-powered debugging and conversational assistant that helps developers quickly fix, optimize, and understand their code. It also offers an interactive chat mode where you can ask questions and receive responses in various emotional tones!

**Note:** I have added all the files i made during the project making or you can say versions of it.

## Overview

This project has two primary functionalities:

### 1. Code Debug Mode
- **Input:** Paste your code (which may contain multiple errors) into the text area.
- **Options:**
  - **Fix Errors Only:** The AI returns only the corrected code without any additional explanation.
  - **Fix Errors + Optimize:** The AI fixes your code and suggests a few brief optimization improvements.
  - **Fix + Optimize + Explain:** The AI fixes, optimizes, and provides a user-friendly explanation of the changes.
- **Language Selection:** Choose the desired output language, independent of the input language.
- **Model Selection:** Choose among the available models (`mistral-tiny`, `mistral-medium`, `mistral-large`) for varying response quality.
- **Execution:** If your code is in Python, you can run the corrected code directly within the interface.

### 2. Chat Mode
- **Input:** Write your query in the chat box.
- **Emotional Tone:** Choose from various moods (`Neutral`, `Happy`, `Anger`, `Love`, `Explanation`, `One Liner`, `Over Explainer`) to tailor the AI's response.
- **Model Selection:** Select the AI model to use for generating the response.
- **Output:** The AI responds based on your query, selected mood, and chosen model.

## Features

- **Multi-Mode Debugging:** Easily switch between different debugging modes to suit your needs.
- **Language Flexibility:** Supports multiple programming languages. The output is tailored to the language you select.
- **In-Built Code Execution:** Run Python code directly from the interface.
- **Dynamic Chat Experience:** Interact with the AI using different emotional tones for creative, detailed, or succinct responses.
- **Custom UI & Styling:** Enjoy a modern interface with gradient headers and custom purple buttons.

## Getting Started

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-code-doctor.git
cd ai-code-doctor
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

Ensure to download all the libraries used in the project

### 4. Configure the API Key

- Open the `guifinal.py` file.
- Replace the placeholder API key (`API_KEY = "your-api-key"`) with your own Mistral AI API key.

### 5. Run the Application

```bash
python gui.py
```

The Gradio interface will open in your default web browser.

## Project Structure

- **gui.py:** Contains the main code for the application, including both Code Debug and Chat modes.
- **requirements.txt:** Lists all the required Python libraries.

## Usage

### Code Debug Mode

1. **Paste Your Code:** Enter the code you want to debug into the provided text area.
2. **Select Options:** Choose your programming language, the fix mode (`Fix Errors Only`, `Fix Errors + Optimize`, or `Fix + Optimize + Explain`), and the desired AI model.
3. **Fix & Execute:** Click on **"🛠 Fix Code"** to receive the corrected code along with additional details based on your selection. If your code is in Python, you can click **"▶ Run My Code"** to execute it.

### Chat Mode

1. **Switch Mode:** Use the mode selector to switch to Chat Mode.
2. **Enter Your Query & Choose Mood:** Type your query and select the desired emotional tone (`Neutral`, `Happy`, `Anger`, `Love`, `Explanation`, `One Liner`, or `Over Explainer`) along with the AI model.
3. **Send Message:** Click **"💬 Send Message"** to receive a response tailored to your query and mood.

## Customization

- **CSS Styling:** The project uses custom CSS in `gui.py` to create a visually appealing interface with gradient headers and purple buttons. You can modify this CSS block to further customize the look and feel.
- **Prompt Configuration:** The prompts for code debugging and chat responses are customizable within the `fix_code` and `chatbot_response` functions. Adjust these as needed to experiment with different styles or response details.

## Contributing

Contributions are welcome! Please feel free to fork the repository, add new features, or fix bugs. When contributing, consider opening an issue or submitting a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Gradio:** For providing an easy-to-use framework for building the web interface.
- **Mistral AI:** For powering the advanced debugging and chat functionalities.

