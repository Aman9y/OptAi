# OptiAI - Smart Code Enhancement Tool

OptiAI is an intelligent code optimization platform that leverages AI to analyze, optimize, and enhance your code. Built with Flask and powered by Ollama's Qwen2.5-Coder model, it provides real-time code optimization, explanation, static analysis, and quality insights.

## Features

- **AI-Powered Code Optimization**: Automatically refactor and optimize code for better performance via real-time SSE streaming
- **AI Optimization Suggestions**: Get 3-5 specific, categorized, actionable suggestions before committing to a full optimization
- **Multi-Language Support**: Works with JavaScript, Python, Java, C/C++, HTML, CSS, and more
- **Radon Static Analysis**: Real cyclomatic complexity and maintainability index for Python code using the Radon library
- **Code Execution**: Test and run your code directly in the browser with stdin support
- **Performance Dashboard**: Collapsible bar chart dashboard tracking execution time and memory usage across runs
- **Async Chat Assistant**: Non-blocking AI chat with job polling — ask questions while the editor stays fully interactive
- **Code Explanation**: Detailed explanations streamed token-by-token into the output editor
- **History Tracking**: Persistent optimization history stored in SQLite
- **Modern UI**: Clean, responsive interface with CodeMirror syntax highlighting and resizable panels
- **Live Statistics**: Real-time metrics on code size, cyclomatic complexity, performance, time/space complexity, and maintainability

## Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed and running
- Qwen2.5-Coder model pulled in Ollama
- **For Code Execution**: Node.js (JavaScript), Java JDK (Java), GCC (C/C++)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Mint jeera"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   - Download and install Ollama from [https://ollama.ai/](https://ollama.ai/)
   - Pull the required model:
     ```bash
     ollama pull qwen2.5-coder
     ```
   - Start Ollama service:
     ```bash
     ollama serve
     ```

4. **Initialize the database**
   The database is automatically initialized on first run — no manual setup needed.

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Start optimizing code**
   - Paste your code in the left editor — language is auto-detected
   - Click **Optimize** to stream an optimized version into the output editor
   - Click **Explain** to stream a detailed explanation
   - Click **Suggest** to get AI-driven optimization suggestions with categories and fixes
   - Click **Run** to execute your code and see output (supports optional stdin input)
   - Use the **Chat** panel for async coding assistance

## Project Structure

```
Mint jeera/
├── app.py                 # Main Flask application
├── database.py            # Database operations
├── code_executor.py       # Code execution engine (time + memory tracking)
├── requirements.txt       # Python dependencies
├── optiai.db              # SQLite database (auto-generated)
├── static/
│   └── js/
│       ├── language-patterns.js     # Language detection patterns
│       └── complexity-analyzer.js   # Time/space complexity heuristics
└── templates/
    ├── home.html          # Main interface
    ├── about.html         # About page
    ├── features.html      # Features page
    └── history.html       # Optimization history
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home page with code editor |
| `GET` | `/features` | Features overview |
| `GET` | `/about` | About page |
| `GET` | `/history` | Optimization history |
| `POST` | `/stream` | SSE streaming for optimize/explain (mode param) |
| `POST` | `/suggestions` | AI-driven optimization suggestions (JSON array) |
| `POST` | `/analyze` | Radon static analysis for Python code |
| `POST` | `/execute` | Execute code and return output + metrics |
| `GET` | `/dashboard` | Execution metrics for the performance dashboard |
| `POST` | `/chat` | Start async chat job, returns `job_id` |
| `GET` | `/job/<job_id>` | Poll async job status and result |
| `POST` | `/ask` | Legacy synchronous optimize/explain endpoint |

## Configuration

- **Ollama API URL**: `http://localhost:11434/api/generate`
- **Model**: `qwen2.5-coder`
- **Database**: SQLite (`optiai.db`)
- **Port**: 5000 (Flask default)

## Supported Languages

### Code Optimization, Explanation & Suggestions
- JavaScript / TypeScript
- Python
- Java
- C / C++
- HTML / CSS
- PHP, Ruby, Rust, SQL, and more

### Static Analysis (Radon)
- **Python only** — cyclomatic complexity per function + maintainability index with letter grades (A–F)
- Heuristic fallback for all other languages

### Code Execution
- **Python**: Direct execution via subprocess
- **JavaScript**: Node.js runtime
- **Java**: Compile and run with JDK
- **C/C++**: GCC compilation and execution

## Features in Detail

### SSE Real-Time Streaming
Optimize and Explain use Server-Sent Events via a `fetch` + `ReadableStream` reader. Tokens from Ollama are appended directly to the output editor as they arrive — no fake typing delays.

### AI Optimization Suggestions
The **Suggest** button calls `/suggestions` which prompts the model to return a strict JSON array. Each suggestion includes:
- `title` — short label
- `category` — one of: Performance, Readability, Security, Best Practice, Memory
- `description` — one sentence explaining the issue
- `fix` — one sentence describing the concrete fix

Results render as color-coded cards in a collapsible panel below the editors.

### Radon Static Analysis
For Python code, after optimization the app calls `/analyze` using the `radon` library to compute:
- **Cyclomatic Complexity** — average and max across all functions, with A–F rank
- **Maintainability Index** — 0–100 score with letter grade

Falls back to heuristic scoring for non-Python languages. Controlled by the `RADON_AVAILABLE` flag.

### Performance Dashboard
A collapsible panel with Canvas-based bar charts (no external chart library) showing:
- Last execution time (ms) and peak memory (KB)
- Trends across the last 10 runs
- Total run count and last code size

Metrics are persisted in the `execution_metrics` SQLite table.

### Async Chat
`/chat` returns a `job_id` immediately. The frontend polls `/job/<id>` every 600ms while showing a loading animation. The Flask thread is never blocked — the Ollama call runs in a daemon thread. Completed jobs are cleaned from memory after retrieval.

### Code Execution
- Measures real elapsed time with `time.perf_counter()` and peak memory with `tracemalloc`
- Supports optional stdin input
- Results and metrics are saved to the database after each run

## Dependencies

- **Flask 3.0.2**: Web framework
- **Requests 2.31.0**: HTTP library for Ollama API calls
- **Radon 6.0.1**: Python static analysis (cyclomatic complexity, maintainability index)
- **SQLite3**: Database (built-in with Python)
- **Ollama**: Local AI model serving platform

## Troubleshooting

### Common Issues

1. **Ollama not responding**
   - Ensure Ollama is running: `ollama serve`
   - Check the model is installed: `ollama list`

2. **Suggestions return a parse error**
   - The model occasionally wraps JSON in markdown fences — the endpoint strips them automatically, but very short/malformed code may still fail. Try with more complete code.

3. **Radon not available**
   - Install it: `pip install radon==6.0.1`
   - The app falls back to heuristic analysis if Radon is missing

4. **Code execution fails**
   - Python: ensure Python is on PATH
   - JavaScript: install Node.js and ensure `node` is on PATH
   - Java: install JDK and ensure `javac`/`java` are on PATH
   - C/C++: install GCC and ensure `gcc`/`g++` are on PATH

5. **Database errors**
   - Delete `optiai.db` to reset — it will be recreated on next startup

6. **Port already in use**
   - Change the port: `app.run(debug=True, port=5001)`

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
