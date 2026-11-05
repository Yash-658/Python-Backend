from app.models.testCaseDB import TestCaseDB
from app.services.code_executor import execute_python
from app.services.execution_result import ExecutionResult
from dataclasses import dataclass

@dataclass
class SubmissionJudgeResult:
    status: str
    passed_test_cases: int
    total_test_cases: int
    execution_time: float
    memory_used: float

def normalize_output(output: str) -> str:
    return output.strip()

def compare_output(actual: str, expected: str) -> bool:
    return normalize_output(actual) == normalize_output(expected)
  

def judge_test_case(code: str, test_case: TestCaseDB) -> ExecutionResult:
    result = execute_python(code, test_case.input_data)

    if result.status != "success":
        return result

    if compare_output(result.output, test_case.expected_output):
        return ExecutionResult(
            status="accepted",
            output=result.output,
            execution_time=result.execution_time,
            memory_used= result.memory_used
        )

    return ExecutionResult(
        status="wrong_answer",
        output=result.output,
        execution_time=result.execution_time,
        memory_used=result.memory_used
    )
    
    
def judge_submission(code: str, test_cases: list[TestCaseDB]) -> SubmissionJudgeResult:
    
    total_test_cases = len(test_cases)
    passed_test_cases = 0
    first_failure_status = None
    total_execution_time = 0.0
    maxm_memory_used = 0.0
    
    for test_case in test_cases:
        result = judge_test_case(
            code=code,
            test_case = test_case
        )
        
        if result.memory_used is not None:
            maxm_memory_used = max(maxm_memory_used, result.memory_used)
        
        if result.execution_time is not None:
            total_execution_time += result.execution_time

        if result.status == "accepted":
            passed_test_cases += 1
            
        elif first_failure_status is None:
            first_failure_status = result.status

    if total_test_cases == 0:
        final_status = "no_test_cases"
    else:
        final_status = first_failure_status or "accepted"
        
    return SubmissionJudgeResult(
        status=final_status,
        passed_test_cases=passed_test_cases,
        total_test_cases=total_test_cases,
        execution_time=total_execution_time,
        memory_used = maxm_memory_used
    )