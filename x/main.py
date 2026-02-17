import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="x", description="Prompt-based Linux command tool")
    parser.add_argument("-p", "--prompt", required=True, help="Prompt describing the command to run")
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
