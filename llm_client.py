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

    for iteration in range(MAX_ITERATION):
        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        if not function_calls:
            print(interaction.output_text)
            break

        print(interaction.steps)

        function_results = []

        for step in function_calls:
            tool = TOOLS_REGISTRY[step.name]

            if "input_model" in tool:
                input_model = tool["input_model"]
                validated_input = input_model.model_validate(step.arguments)
                result = tool["function"](validated_input)
            else:
                result = tool["function"](**step.arguments)

            print(result)

            function_results.append(
                {
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": result.model_dump(),
                }
            )

        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            previous_interaction_id=interaction.id,
            input=function_results,
            tools=tools,
        )

    else:
        print(f"max iterations reached{iteration}")

    print(iteration)
    