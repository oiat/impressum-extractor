import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Impressum extractor")
    parser.add_argument(
        "--url",
        "-u",
        help="Url to get impressum"
    )
    return parser.parse_args()
