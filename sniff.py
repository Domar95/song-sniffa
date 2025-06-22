from typing import Optional

from utils.audio_capturer import AudioCapturer
from utils.song_identifier import ACRClient
from cli import run_cli


def sniff(url: str, mode: str, duration: int = 15) -> Optional[str]:
    """Captures an audio sample from stream and identifies the song."""

    # Initialize the AudioCapturer & ACRClient for song identification
    capturer = AudioCapturer(url)
    client = ACRClient()

    if mode == "buffer":
        data = capturer.to_buffer(duration)
        songs_data = client.identify_from_buffer(data)
    elif mode == "file":
        file = capturer.to_file(duration=duration)
        songs_data = client.identify_from_file(file)
    else:
        raise ValueError("Invalid mode: choose 'file' or 'buffer'")

    if not songs_data:
        return None

    return client.analyze_songs(songs_data)


if __name__ == "__main__":
    args = run_cli()
    result = sniff(args.url, args.mode, args.duration)
    print(result)
