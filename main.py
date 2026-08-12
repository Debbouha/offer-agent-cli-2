import sys

from llm_client import generate


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python main.py "<message>"')
        return

    user_msg = " ".join(sys.argv[1:])
    response = generate(user_msg)

    print(response)


if __name__ == "__main__":
    main()