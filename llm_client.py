from google import genai

from config import GEMINI_MODEL
from registry import TOOLS_REGISTRY


def generate(user_msg) -> None:
    client = genai.Client()

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=user_msg,
        tools = [
            tool["declaration"]
            for tool in TOOLS_REGISTRY.values()
        ]
    )

    step = next(
        step
        for step in interaction.steps
        if step.type == "function_call"
    )

    tool = TOOLS_REGISTRY[step.name]
    result = tool["function"](**step.arguments)
    
    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        previous_interaction_id=interaction.id,
        input=[
            {
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": result.model_dump(),
            }
        ],
        tools=[
            tool["declaration"]
            for tool in TOOLS_REGISTRY.values()
        ],
    )

    print(interaction.output_text)
