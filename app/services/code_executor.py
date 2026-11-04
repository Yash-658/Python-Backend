import subprocess               # lets our backend launch an external process, here the Docker CLI.
import tempfile                 # creates temporary files safely; we'll store submitted code there.
from pathlib import Path        # helps work with filesystem paths in a clean, cross-platform way.
import uuid
from time import perf_counter

from app.services.execution_result import ExecutionResult


def execute_python(code: str, input_data: str = "", timeout: int = 3) -> ExecutionResult:
    with tempfile.TemporaryDirectory() as temp_dir:
        code_path = Path(temp_dir) / "main.py"
        code_path.write_text(code, encoding="utf-8")
        
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
            "python:3.12",
            "python", "/workspace/main.py"
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

        return ExecutionResult(
            status="success" if result.returncode == 0 else "runtime_error",
            output=result.stdout,
            execution_time=execution_time,
            error=result.stderr or None
        )