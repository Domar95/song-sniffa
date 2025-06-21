from utils.audio_capturer import AudioCapturer
from utils.song_identifier import ACRClient

url = "https://www.twitch.tv/sniffa"


def sniff(url: str) -> str:
    """Captures an audio sample from stream and identifies the song."""

    # Initialize the AudioCapturer & ACRClient for song identification
    capturer = AudioCapturer(url)
    client = ACRClient()

    # Capture audio as mp3 and identify through file
    file = capturer.to_file()
    song = client.identify_from_file(file)

    # Capture audio as bytes buffer and identify through buffer
    # data = capturer.to_buffer()
    # song = client.identify_from_buffer(data)

    print(song)


if __name__ == "__main__":
    sniff(url)
