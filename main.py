import sys
import json

from llm_client import generate
from offers import ensure_offers_cache, get_offers_text
from tools import list_offers


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python main.py \"user text request\"")
        return 1

    user_msg = sys.argv[1]

    ensure_offers_cache()
    offers = get_offers_text()
    generate(user_msg)
    #print(list_offers())
    #envoyer le message + tools

    return 0
if __name__ =="__main__":
    raise SystemExit(main())