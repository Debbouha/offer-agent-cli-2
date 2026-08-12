from google import genai
from google.genai import errors
from pydantic import ValidationError

from config import GEMINI_MODEL
from registry import TOOLS_REGISTRY


MAX_ITERATION = 10


def _create_interaction(client, **kwargs):
    try:
        return client.interactions.create(**kwargs)
    except errors.APIError as err:
        raise RuntimeError(
            f"Gemini API error: {err}"
        ) from err


def _execute_tool_call(step) -> dict:
    tool = TOOLS_REGISTRY[step.name]
    input_model = tool["input_model"]

    try:
        if input_model is not None:
            validated_input = input_model.model_validate(step.arguments)
            result = tool["function"](validated_input)
        else:
            result = tool["function"]()

        result_data = result.model_dump()

    except (ValidationError, ValueError) as err:
        result_data = {
            "error": str(err)
        }

    return {
        "type": "function_result",
        "name": step.name,
        "call_id": step.id,
        "result": result_data,
    }


def generate(user_msg: str) -> str:
    client = genai.Client()

    tools = [
        tool["declaration"]
        for tool in TOOLS_REGISTRY.values()
    ]

    interaction = _create_interaction(
        client,
        model=GEMINI_MODEL,
        input=user_msg,
        tools=tools,
    )

    for _ in range(MAX_ITERATION):
        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        if not function_calls:
            return interaction.output_text

        function_results = [
            _execute_tool_call(step)
            for step in function_calls
        ]

        interaction = _create_interaction(
            client,
            model=GEMINI_MODEL,
            previous_interaction_id=interaction.id,
            input=function_results,
            tools=tools,
        )

    raise RuntimeError("Maximum agent iterations reached.")