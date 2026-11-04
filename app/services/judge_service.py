from app.models.testCaseDB import TestCaseDB
from app.services.code_executor import execute_python
from app.services.execution_result import ExecutionResult


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
            output=result.output
        )

    return ExecutionResult(
        status="wrong_answer",
        output=result.output
    )
    
    
def judge_submission(code: str, test_cases: list[TestCaseDB]) -> str:
    for test_case in test_cases:
        result = judge_test_case(
            code=code,
            test_case = test_case
        )

        if result.status != "accepted":
            return result.status

    return "accepted"