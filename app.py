from flask import Flask, render_template, request, jsonify, url_for
import requests
import json
from database import init_db, save_optimization, get_history
from code_executor import CodeExecutor

app = Flask(__name__, static_url_path='/static')

# Initialize database and code executor
init_db()
code_executor = CodeExecutor()

# Ensure static files are not cached during development
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama runs on port 11434 by default

def create_optimization_prompt(code):
    prompt = f"""You are an expert code optimizer. Analyze the following code and provide an optimized version.
Rules for optimization:
1. Focus on performance improvements
2. Maintain code readability
3. Use modern best practices
4. Provide ONLY the optimized code without explanations
5. Keep the same functionality
6. Remove any redundant or unnecessary code

Here's the code to optimize:

{code}

Return ONLY the optimized code without any explanations or markdown formatting."""
    return prompt

def create_explanation_prompt(code):
    prompt = f"""Analyze and explain the following code in detail:

{code}

Provide a clear, detailed explanation of how the code works, its structure, and any potential improvements."""
    return prompt

def create_chat_prompt(message):
    prompt = f"""You are a helpful AI coding assistant. Help the user with their coding questions and provide clear, concise answers.
Previous context: The user is working with a code optimization website.

User's message: {message}

Provide a helpful response focusing on coding-related aspects."""
    return prompt

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/history')
def history():
    db_history = get_history()
    return render_template('history.html', history=db_history)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.form['message']
        prompt = create_chat_prompt(message)
        
        # Send request to Ollama API
        response = requests.post(
            OLLAMA_API_URL, 
            json={
                "model": "qwen2.5-coder",
                "prompt": prompt,
                "temperature": 0.7
            },
            stream=True
        )
        
        # Handle streaming response
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'response' in json_response:
                    full_response += json_response['response']
        
        return jsonify({"answer": full_response.strip() if full_response else "I'm not sure how to help with that."})
        
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        code = request.form['code']
        language = request.form['language']
        input_data = request.form.get('input', '')
        
        result = code_executor.execute_code(code, language, input_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_code = request.form['question']
        is_explain = 'Explain this code' in user_code
        
        if is_explain:
            prompt = create_explanation_prompt(user_code.replace('Explain this code in detail:\n', ''))
        else:
            prompt = create_optimization_prompt(user_code)
        
        # Send request to Ollama API
        response = requests.post(
            OLLAMA_API_URL, 
            json={
                "model": "qwen2.5-coder",
                "prompt": prompt,
                "temperature": 0.1 if not is_explain else 0.7
            },
            stream=True
        )
        
        # Handle streaming response
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'response' in json_response:
                    full_response += json_response['response']
        
        # Save to database if optimization was successful
        if full_response and not is_explain:
            save_optimization(user_code, full_response, "auto-detected")
        
        return jsonify({"answer": full_response.strip() if full_response else "No response received."})
        
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
    