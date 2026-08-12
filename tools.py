from models import JobOffer, OffersSummaryOutput, OfferSummary, ReadOfferInput, SearchOffersInput
from offers import get_offers_data


def list_offers() -> OffersSummaryOutput:
    data = get_offers_data()

    offers = [
        OfferSummary(
            id=offer["id"],
            title=offer["intitule"],
        )
        for offer in data["resultats"]
    ]

    return OffersSummaryOutput(offers=offers)


def search_offers(search_offers_input:SearchOffersInput) -> OffersSummaryOutput:
    data = get_offers_data()
    keyword = search_offers_input.key_word.lower()

    offers = [
        OfferSummary(
            id=offer["id"],
            title=offer["intitule"],
        )
        for offer in data["resultats"]
            if (
                keyword in offer["intitule"].lower()
                or keyword in offer["description"].lower()
            )
    ]

    return OffersSummaryOutput(offers=offers)

def read_offer(read_offer_input: ReadOfferInput) -> JobOffer:
    data = get_offers_data()

    offer = next(
        (
            offer
            for offer in data["resultats"]
            if offer["id"] == read_offer_input.id
        ),
        None,
    )

    if offer is None:
        raise ValueError(
            f'Offer "{read_offer_input.id}" not found.'
        )

    return JobOffer(
        id=offer["id"],
        title=offer["intitule"],
        description=offer["description"],
        publication_date=offer["dateCreation"],
        company=offer.get("entreprise", {}).get("nom"),
        location=offer.get("lieuTravail", {}).get("libelle"),
        salary=offer.get("salaire", {}).get("libelle"),
        experience=offer.get("experienceLibelle"),
        skills=[
            competence["libelle"]
            for competence in offer.get("competences", [])
            if "libelle" in competence
        ],
        apply_url=(
            offer.get("contact", {}).get("urlPostulation")
            or offer.get("origineOffre", {}).get("urlOrigine")
        ),
    )