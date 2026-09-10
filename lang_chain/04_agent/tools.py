from langchain_core.tools import tool

# tool 이 달린 함수의 doc-string 을 AI 가 판단하여 어디에 쓸지 결정
@tool
def multiply(a:int, b:int) -> int:
    """두 수를 곱하는 도구 입니다. 수식기호 '*' 또는 'x' 를 인식합니다."""
    return a * b

@tool
def plus(a:int, b:int) -> int:
    """두 수를 더하는 도구 입니다. 수식기호 '+' 를 인식합니다."""
    return a + b

@tool
def minus(a:int, b:int) -> int:
    """두 수를 빼는 도구 입니다. 수식기호 '-' 를 인식합니다."""
    return a - b

@tool
def divide(a:int, b:int) -> int:
    """두 수를 나누는 도구 입니다. 수식기호 '/' 를 인식합니다."""
    return a / b