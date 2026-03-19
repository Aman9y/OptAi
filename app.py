from flask import Flask, render_template, request, jsonify, url_for, Response, stream_with_context
import requests
import json
import threading
import uuid
from database import init_db, save_optimization, get_history, save_execution_metric, get_execution_metrics
from code_executor import CodeExecutor

try:
    from radon.complexity import cc_visit, cc_rank
    from radon.metrics import mi_visit, mi_rank
    RADON_AVAILABLE = True
except ImportError:
    RADON_AVAILABLE = False

app = Flask(__name__, static_url_path='/static')

# Initialize database and code executor
init_db()
code_executor = CodeExecutor()

# In-memory async job store: {job_id: {status, result, error}}
_jobs = {}
_jobs_lock = threading.Lock()

def _run_job(job_id, prompt, temperature):
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={'model': 'qwen2.5-coder', 'prompt': prompt, 'temperature': temperature},
            stream=True
        )
        full = ''
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                full += chunk.get('response', '')
                if chunk.get('done'):
                    break
        with _jobs_lock:
            _jobs[job_id] = {'status': 'done', 'result': full.strip()}
    except Exception as e:
        with _jobs_lock:
            _jobs[job_id] = {'status': 'error', 'error': str(e)}

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

def create_suggestions_prompt(code):
    return f"""You are an expert code reviewer. Analyze the following code and return ONLY a JSON array of 3-5 specific, actionable optimization suggestions.
Each item must be a JSON object with these exact keys:
- "title": short name (max 6 words)
- "category": one of ["Performance", "Readability", "Security", "Best Practice", "Memory"]
- "description": one sentence explaining the issue
- "fix": one sentence describing the concrete fix

Return ONLY valid JSON array, no markdown, no explanation.

Code:
{code}"""

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

@app.route('/suggestions', methods=['POST'])
def suggestions():
    try:
        code = request.form.get('code', '')
        if not code.strip():
            return jsonify({"error": "No code provided"})

        prompt = create_suggestions_prompt(code)
        response = requests.post(
            OLLAMA_API_URL,
            json={'model': 'qwen2.5-coder', 'prompt': prompt, 'temperature': 0.3},
            stream=True
        )
        full = ''
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                full += chunk.get('response', '')
                if chunk.get('done'):
                    break

        # Extract JSON array from response
        start, end = full.find('['), full.rfind(']')
        if start == -1 or end == -1:
            return jsonify({"error": "Could not parse suggestions"})
        return jsonify({"suggestions": json.loads(full[start:end+1])})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.form['message']
        prompt = create_chat_prompt(message)
        job_id = str(uuid.uuid4())
        with _jobs_lock:
            _jobs[job_id] = {'status': 'pending'}
        t = threading.Thread(target=_run_job, args=(job_id, prompt, 0.7), daemon=True)
        t.start()
        return jsonify({'job_id': job_id})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/job/<job_id>', methods=['GET'])
def job_status(job_id):
    with _jobs_lock:
        job = _jobs.get(job_id)
    if not job:
        return jsonify({'status': 'not_found'}), 404
    # Clean up completed jobs after retrieval
    if job['status'] in ('done', 'error'):
        with _jobs_lock:
            _jobs.pop(job_id, None)
    return jsonify(job)

@app.route('/analyze', methods=['POST'])
def analyze_code():
    try:
        code = request.form['code']
        language = request.form.get('language', 'python').lower()

        if language != 'python' or not RADON_AVAILABLE:
            return jsonify({"radon": False})

        # Cyclomatic Complexity
        blocks = cc_visit(code)
        if blocks:
            avg_cc = sum(b.complexity for b in blocks) / len(blocks)
            max_cc = max(b.complexity for b in blocks)
            rank = cc_rank(max_cc)
            cc_results = [
                {"name": b.name, "complexity": b.complexity, "rank": cc_rank(b.complexity)}
                for b in blocks
            ]
        else:
            avg_cc, max_cc, rank = 1, 1, 'A'
            cc_results = []

        # Maintainability Index
        mi_score = mi_visit(code, multi=True)
        mi_letter = mi_rank(mi_score)

        return jsonify({
            "radon": True,
            "cyclomatic": {
                "average": round(avg_cc, 2),
                "max": max_cc,
                "rank": rank,
                "blocks": cc_results
            },
            "maintainability": {
                "score": round(mi_score, 2),
                "rank": mi_letter
            }
        })

    except SyntaxError as e:
        return jsonify({"radon": False, "error": f"Syntax error: {str(e)}"})
    except Exception as e:
        return jsonify({"radon": False, "error": str(e)})


@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        code = request.form['code']
        language = request.form['language']
        input_data = request.form.get('input', '')

        result = code_executor.execute_code(code, language, input_data)

        # Persist metrics
        save_execution_metric(
            language=language,
            execution_time_ms=result.get('execution_time_ms', 0),
            memory_kb=result.get('memory_kb', 0),
            code_size_bytes=len(code.encode('utf-8')),
            success=result.get('success', False)
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/dashboard', methods=['GET'])
def dashboard():
    metrics = get_execution_metrics(limit=20)
    return jsonify(metrics)

@app.route('/stream', methods=['POST'])
def stream():
    user_code = request.form.get('question', '')
    is_explain = request.form.get('mode') == 'explain'

    if is_explain:
        prompt = create_explanation_prompt(user_code)
    else:
        prompt = create_optimization_prompt(user_code)

    def generate():
        full_response = ''
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    'model': 'qwen2.5-coder',
                    'prompt': prompt,
                    'temperature': 0.7 if is_explain else 0.1
                },
                stream=True
            )
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get('response', '')
                    if token:
                        full_response += token
                        # SSE format: data: <token>\n\n
                        yield f"data: {json.dumps({'token': token})}\n\n"
                    if chunk.get('done'):
                        break

            # Save optimization to DB after full stream
            if full_response and not is_explain:
                save_optimization(user_code, full_response, 'auto-detected')

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


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
    