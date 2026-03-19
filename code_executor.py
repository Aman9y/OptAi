import subprocess
import tempfile
import os
import time
import tracemalloc

class CodeExecutor:
    def __init__(self):
        self.timeout = 10

    def execute_code(self, code, language, input_data=""):
        try:
            if language.lower() == 'python':
                return self._execute_python(code, input_data)
            elif language.lower() == 'javascript':
                return self._execute_javascript(code, input_data)
            elif language.lower() == 'java':
                return self._execute_java(code, input_data)
            elif language.lower() in ['c', 'cpp', 'c++']:
                return self._execute_c_cpp(code, input_data, language)
            else:
                return {"success": False, "error": f"Language {language} not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _measure(self, cmd, input_data):
        """Run a command and return output + elapsed ms + peak memory KB."""
        tracemalloc.start()
        start = time.perf_counter()
        result = subprocess.run(cmd, input=input_data, capture_output=True, text=True, timeout=self.timeout)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return result, elapsed_ms, round(peak / 1024, 2)  # peak in KB

    def _execute_python(self, code, input_data):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            fname = f.name
        try:
            result, elapsed_ms, memory_kb = self._measure(['python', fname], input_data)
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "execution_time_ms": elapsed_ms,
                "memory_kb": memory_kb
            }
        finally:
            os.unlink(fname)

    def _execute_javascript(self, code, input_data):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            fname = f.name
        try:
            result, elapsed_ms, memory_kb = self._measure(['node', fname], input_data)
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "execution_time_ms": elapsed_ms,
                "memory_kb": memory_kb
            }
        finally:
            os.unlink(fname)

    def _execute_java(self, code, input_data):
        import re
        class_match = re.search(r'public\s+class\s+(\w+)', code)
        if not class_match:
            return {"success": False, "error": "No public class found"}
        class_name = class_match.group(1)

        with tempfile.TemporaryDirectory() as temp_dir:
            java_file = os.path.join(temp_dir, f"{class_name}.java")
            with open(java_file, 'w') as f:
                f.write(code)

            compile_result = subprocess.run(['javac', java_file], capture_output=True, text=True, timeout=self.timeout)
            if compile_result.returncode != 0:
                return {"success": False, "error": f"Compilation error: {compile_result.stderr}", "output": ""}

            result, elapsed_ms, memory_kb = self._measure(['java', '-cp', temp_dir, class_name], input_data)
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "execution_time_ms": elapsed_ms,
                "memory_kb": memory_kb
            }

    def _execute_c_cpp(self, code, input_data, language):
        suffix = '.c' if language.lower() == 'c' else '.cpp'
        compiler = 'gcc' if language.lower() == 'c' else 'g++'

        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, f"main{suffix}")
            executable = os.path.join(temp_dir, "main.exe")
            with open(source_file, 'w') as f:
                f.write(code)

            compile_result = subprocess.run([compiler, source_file, '-o', executable], capture_output=True, text=True, timeout=self.timeout)
            if compile_result.returncode != 0:
                return {"success": False, "error": f"Compilation error: {compile_result.stderr}", "output": ""}

            result, elapsed_ms, memory_kb = self._measure([executable], input_data)
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "execution_time_ms": elapsed_ms,
                "memory_kb": memory_kb
            }