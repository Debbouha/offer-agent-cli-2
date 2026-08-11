from google import genai

from config import GEMINI_MODEL
from registry import TOOLS_REGISTRY


def generate(user_msg) -> None:
    client = genai.Client()
    MAX_ITERATION = 10
    tools = [
                tool["declaration"]
                for tool in TOOLS_REGISTRY.values()
            ]

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=user_msg,
        tools=tools,
    )

    for _ in range(MAX_ITERATION):
        step = next(
            (
                step
                for step in interaction.steps
                if step.type == "function_call"
            ),
            None,
        )

        if step is None:
            print(interaction.output_text)
            break
        print(interaction.steps)
        tool = TOOLS_REGISTRY[step.name]
        if "input_model" in tool:
            input_model = tool["input_model"]
            validated_input = input_model.model_validate(step.arguments)
            result = tool["function"](validated_input)
        else:
            result = tool["function"](**step.arguments)

        print(result)
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
                tools=tools,
            )
    else:
        print("max iterations reached")