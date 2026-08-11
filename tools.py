from models import ListOffersOutput, OfferSummary
from offers import get_offers_data


def list_offers() -> ListOffersOutput:
    data = get_offers_data()

    offers = [
        OfferSummary(
            id=offer["id"],
            title=offer["intitule"],
        )
        for offer in data["resultats"]
    ]

    return ListOffersOutput(offers=offers)