from tools import list_offers, search_offers, read_offer
from models import (
    JobOffer,
    OffersSummaryOutput,
    ReadOfferInput,
    SearchOffersInput,
)


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
        "input_model": None,
        "output_model": OffersSummaryOutput,
    },
    "search_offers": {
        "declaration": {
            "type": "function",
            "name": "search_offers",
            "description": "Searches job offers by keyword and returns their ID and title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key_word": {
                        "type": "string",
                        "description": "Keyword used to search for relevant job offers.",
                    }
                },
                "required": ["key_word"],
            },
        },
        "function": search_offers,
        "input_model": SearchOffersInput,
        "output_model": OffersSummaryOutput,
    },
    "read_offer": {
        "declaration": {
            "type": "function",
            "name": "read_offer",
            "description": "Retrieves the full details of a job offer using its unique ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Unique identifier of the job offer.",
                    }
                },
                "required": ["id"],
            },
        },
        "function": read_offer,
        "input_model": ReadOfferInput,
        "output_model": JobOffer,
    },
}