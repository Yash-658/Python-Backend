import subprocess               # lets our backend launch an external process, here the Docker CLI.
import tempfile                 # creates temporary files safely; we'll store submitted code there.
from pathlib import Path        # helps work with filesystem paths in a clean, cross-platform way.
import textwrap
import uuid
from time import perf_counter

from app.services.execution_result import ExecutionResult


def execute_python(code: str, input_data: str = "", timeout: int = 3) -> ExecutionResult:
    with tempfile.TemporaryDirectory() as temp_dir:
        code_path = Path(temp_dir) / "main.py"
        code_path.write_text(code, encoding="utf-8")
        
        runner_path = Path(temp_dir) / "runner.py"

        runner_code = textwrap.dedent("""              # It removes common leading whitespace from every line. This allows us to define properly formatted Python code inside another function.
            import resource
            import subprocess
            import sys
        
            result = subprocess.run([sys.executable, "/workspace/main.py"])
        
            memory_kb = resource.getrusage(
                resource.RUSAGE_CHILDREN
            ).ru_maxrss
        
            print(
                f"__JUDGE_MEMORY_KB__={memory_kb}",
                file=sys.stderr,
                flush=True
            )
        
            sys.exit(result.returncode)
        """)

        runner_path.write_text(runner_code, encoding="utf-8")
        
        container_name = f"judge-{uuid.uuid4().hex}"       # gave a unique name to this container that we are going to create~
        
        docker_command = [
            "docker",
            "run",
            "-i",
            "--name", container_name,
            "--rm",
            "--network", "none",
            "--memory", "128m",
            "--cpus", "0.5",
            "--read-only",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--pids-limit", "64",
            "--mount", f"type=bind,source={code_path},target=/workspace/main.py,readonly",
            "--mount", f"type=bind,source={runner_path},target=/workspace/runner.py,readonly",
            "python:3.12",
            "python", "/workspace/runner.py"
        ]

        start_time = perf_counter()
        
        try:
            result = subprocess.run(
                docker_command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )

        except subprocess.TimeoutExpired:
            execution_time = perf_counter() - start_time
            
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                capture_output=True,
                text=True
            )
            
            return ExecutionResult(
                status="time_limit_exceeded",
                output="",
                error="Execution timed out",
                execution_time=execution_time
            )
            
        execution_time = perf_counter() - start_time

        stderr_text = result.stderr or ""               # or "" ensures we have an empty string rather than None if nothing was captured.
        memory_marker = "__JUDGE_MEMORY_KB__="
        
        memory_used = None
        error_message = stderr_text.strip() or None
        
        if memory_marker in stderr_text:
            actual_errors, memory_data = stderr_text.rsplit(memory_marker, 1)
        
            try:
                memory_used = round(int(memory_data.strip()) / 1024, 2)
                error_message = actual_errors.strip() or None
        
            except ValueError:
                memory_used = None
                error_message = stderr_text.strip() or None
        
        return ExecutionResult(
            status="success" if result.returncode == 0 else "runtime_error",
            output=result.stdout,
            execution_time=execution_time,
            memory_used=memory_used,
            error=error_message
        )