from utils.audio_sampler import capture_audio_sample
from utils.song_identifier import identify_song

url = "https://www.twitch.tv/sniffa"


def sniff(url: str) -> str:
    """Captures an audio sample from stream and identifies the song."""

    capture_audio_sample(url)
    song = identify_song()
    print(song)


if __name__ == "__main__":
    sniff(url)
