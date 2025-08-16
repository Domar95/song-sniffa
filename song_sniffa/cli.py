import argparse


def run_cli():
    parser = argparse.ArgumentParser(
        description="Identify songs from live audio streams."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL of the stream (e.g. https://www.twitch.tv/sniffa)",
    )
    parser.add_argument(
        "--mode",
        choices=["buffer", "file"],
        default="buffer",
        help="Choose how to process audio: 'buffer' (use memory buffer) or 'file' (save mp3)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=15,
        help="Duration (in seconds) to capture audio sample. Recommended: 10–20.",
    )

    args = parser.parse_args()

    return args
