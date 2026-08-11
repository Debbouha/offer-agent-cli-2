from tools import list_offers
from models import ListOffersOutput


TOOLS_REGISTRY = {
    "list_offers": {
        "declaration": {
            "type": "function",
            "name": "list_offers",
            "description": "Lists available job offers with their ID and title.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        "function": list_offers,
        "output_model": ListOffersOutput,
    }
}