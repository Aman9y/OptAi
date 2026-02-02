# OptiAI - Smart Code Enhancement Tool

OptiAI is an intelligent code optimization platform that leverages AI to analyze, optimize, and enhance your code. Built with Flask and powered by Ollama's Qwen2.5-Coder model, it provides real-time code optimization, explanation, and quality analysis.

## Features

- **AI-Powered Code Optimization**: Automatically refactor and optimize code for better performance
- **Multi-Language Support**: Works with JavaScript, Python, Java, C/C++, HTML, CSS, and more
- **Real-Time Code Analysis**: Get instant feedback on code complexity, performance, and quality
- **Code Execution**: Test and run your code directly in the browser
- **Interactive Chat Assistant**: Ask coding questions and get expert guidance
- **Code Explanation**: Detailed explanations of how your code works
- **History Tracking**: Keep track of your optimization history
- **Modern UI**: Clean, responsive interface with syntax highlighting
- **Live Statistics**: Real-time metrics on code size, complexity, performance, and quality

## Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed and running
- Qwen2.5-Coder model downloaded in Ollama
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
   The database will be automatically initialized when you first run the application.

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Start optimizing code**
   - Paste your code in the left editor
   - Click "Optimize" to get an optimized version
   - Click "Explain" to get a detailed explanation
   - Click "Run" to execute your code and see output
   - Use the chat feature for coding assistance

## Project Structure

```
Mint jeera/
├── app.py                 # Main Flask application
├── database.py           # Database operations
├── code_executor.py      # Code execution engine
├── requirements.txt      # Python dependencies
├── optiai.db            # SQLite database (auto-generated)
├── static/
│   └── js/
│       └── language-patterns.js  # Language detection patterns
└── templates/
    ├── home.html        # Main interface
    ├── about.html       # About page
    ├── features.html    # Features page
    └── history.html     # Optimization history
```

## API Endpoints

- `GET /` - Home page with code editor
- `GET /features` - Features overview
- `GET /about` - About page
- `GET /history` - View optimization history
- `POST /ask` - Submit code for optimization or explanation
- `POST /chat` - Chat with AI assistant
- `POST /execute` - Execute code and get output

## Configuration

The application uses the following default settings:

- **Ollama API URL**: `http://localhost:11434/api/generate`
- **Model**: `qwen2.5-coder`
- **Database**: SQLite (`optiai.db`)
- **Port**: 5000 (Flask default)

## Supported Languages

### Code Optimization & Analysis
- JavaScript/TypeScript
- Python
- Java
- C/C++
- HTML/CSS
- PHP
- Ruby
- Rust
- SQL
- And more...

### Code Execution
- **Python**: Direct execution
- **JavaScript**: Node.js runtime
- **Java**: Compile and run
- **C/C++**: GCC compilation and execution

## Features in Detail

### Code Optimization
- Performance improvements
- Code readability enhancements
- Modern best practices implementation
- Redundant code removal

### Code Analysis
- **Complexity Score**: Measures code complexity (0-100)
- **Performance Score**: Evaluates code efficiency (0-100%)
- **Quality Score**: Assesses code quality (0-100)
- **Size Tracking**: Monitors code size changes

### Code Execution
- Run code directly in the browser
- Support for multiple programming languages
- Input/output handling
- Real-time execution results
- Error handling and debugging

### AI Chat Assistant
- Get coding help and guidance
- Ask questions about programming concepts
- Receive suggestions for improvements
- Interactive problem-solving

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Dependencies

- **Flask 3.0.2**: Web framework
- **Requests 2.31.0**: HTTP library for API calls
- **SQLite3**: Database (built-in with Python)
- **Ollama**: AI model serving platform

## Browser Requirements

- Modern web browser with JavaScript enabled
- Support for ES6+ features
- WebSocket support for real-time features

## Troubleshooting

### Common Issues

1. **Ollama not responding**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`

2. **Database errors**
   - Delete `optiai.db` to reset the database
   - Restart the application

3. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the repository.