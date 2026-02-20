"""
Simple Claude agent using the tool runner (beta).
Uses ANTHROPIC_API_KEY environment variable — do not hardcode keys.

Run:
    pip install anthropic
    $env:ANTHROPIC_API_KEY = "sk-ant-..."   # PowerShell
    python "Claude agent test 2.py"
"""

import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment


@beta_tool
def calculator(operation: str, a: float, b: float) -> str:
    """Perform a basic arithmetic calculation.

    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'.
        a: First number.
        b: Second number.
    """
    match operation:
        case "add":
            return str(a + b)
        case "subtract":
            return str(a - b)
        case "multiply":
            return str(a * b)
        case "divide":
            if b == 0:
                return "Error: division by zero"
            return str(a / b)
        case _:
            return f"Error: unknown operation '{operation}'"


runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=[calculator],
    messages=[{"role": "user", "content": "What is (123 * 456) + 789? Show your work."}],
)

for message in runner:
    for block in message.content:
        if hasattr(block, "text"):
            print(block.text)
