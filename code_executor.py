import subprocess
import tempfile
import os
import json
from pathlib import Path

class CodeExecutor:
    def __init__(self):
        self.supported_languages = {
            'python': {'extension': '.py', 'command': ['python']},
            'javascript': {'extension': '.js', 'command': ['node']},
            'java': {'extension': '.java', 'command': ['javac', 'java']},
            'c': {'extension': '.c', 'command': ['gcc', '-o']},
            'cpp': {'extension': '.cpp', 'command': ['g++', '-o']}
        }
    
    def execute_code(self, code, language, input_data=""):
        """Execute code and return output"""
        language = language.lower()
        
        if language not in self.supported_languages:
            return {"success": False, "error": f"Language {language} not supported"}
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                return self._run_code(code, language, temp_dir, input_data)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _run_code(self, code, language, temp_dir, input_data):
        lang_config = self.supported_languages[language]
        file_path = os.path.join(temp_dir, f"code{lang_config['extension']}")
        
        # Write code to file
        with open(file_path, 'w') as f:
            f.write(code)
        
        try:
            if language == 'python':
                return self._run_python(file_path, input_data)
            elif language == 'javascript':
                return self._run_javascript(file_path, input_data)
            elif language == 'java':
                return self._run_java(file_path, temp_dir, input_data)
            elif language in ['c', 'cpp']:
                return self._run_c_cpp(file_path, temp_dir, language, input_data)
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Code execution timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _run_python(self, file_path, input_data):
        result = subprocess.run(
            ['python', file_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        return self._format_result(result)
    
    def _run_javascript(self, file_path, input_data):
        result = subprocess.run(
            ['node', file_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        return self._format_result(result)
    
    def _run_java(self, file_path, temp_dir, input_data):
        # Compile
        compile_result = subprocess.run(
            ['javac', file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if compile_result.returncode != 0:
            return {"success": False, "error": compile_result.stderr}
        
        # Run
        class_name = Path(file_path).stem
        result = subprocess.run(
            ['java', '-cp', temp_dir, class_name],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        return self._format_result(result)
    
    def _run_c_cpp(self, file_path, temp_dir, language, input_data):
        exe_path = os.path.join(temp_dir, 'program.exe')
        compiler = 'gcc' if language == 'c' else 'g++'
        
        # Compile
        compile_result = subprocess.run(
            [compiler, file_path, '-o', exe_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if compile_result.returncode != 0:
            return {"success": False, "error": compile_result.stderr}
        
        # Run
        result = subprocess.run(
            [exe_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=10
        )
        return self._format_result(result)
    
    def _format_result(self, result):
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }