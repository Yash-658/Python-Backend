# Internal contract for passing normalized code-execution results from the executor to the judge service.

from dataclasses import dataclass

@dataclass
class ExecutionResult:
    status: str
    output: str
    execution_time: float | None = None
    memory_used: int | None = None
    error: str | None = None