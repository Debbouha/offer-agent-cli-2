import json
import os
from pathlib import Path

from datetime import datetime, timedelta, timezone
import requests


OFFERS_FILE_PATH = "data/francetravail.json"
CLIENT_ID = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
CLIENT_SECRET = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")


def offers_cache_is_valid() -> bool:
    path = Path(OFFERS_FILE_PATH)
    if not path.is_file():
        return False

    last_modified = datetime.fromtimestamp(path.stat().st_mtime)
    if datetime.now() - last_modified > timedelta(hours=24):
        return False

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return False

    if (
        not isinstance(data, dict)
        or "resultats" not in data
        or not isinstance(data["resultats"], list)
        or len(data["resultats"]) < 1
    ):
        return False
    return True

def fetch_offers() -> None:
    token_response = requests.post(
        "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "api_offresdemploiv2 o2dsoffre",
        },
    )

    token_response.raise_for_status()

    token = token_response.json()["access_token"]

    now = datetime.now(timezone.utc)
    two_months_ago = now - timedelta(days=60)

    params = {
        "departement": "75",
        "domaine": "M18",
        "typeContrat": "CDI",
        "range": "0-149",
        "minCreationDate": two_months_ago.strftime("%Y-%m-%dT00:00:00Z"),
        "maxCreationDate": now.strftime("%Y-%m-%dT23:59:59Z"),
    }

    response = requests.get(
        "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
    )
    response.raise_for_status()

    with open(OFFERS_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(response.json(), file, indent=2, ensure_ascii=False)

def ensure_offers_cache() -> None:
    if offers_cache_is_valid():
        return

    fetch_offers()
    print("New offers fetched.")


def get_offers_text() -> list[dict]:
    with open(OFFERS_FILE_PATH, "r", encoding="utf-8") as file:
        data = file.read()
    return data


def get_offers_data() -> list[dict]:
    with open(OFFERS_FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data