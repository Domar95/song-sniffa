from utils.audio_sampler import capture_audio_sample, capture_audio_buffer
from utils.song_identifier import identify_song, identify_song_from_buffer

url = "https://www.twitch.tv/sniffa"


def sniff(url: str) -> str:
    """Captures an audio sample from stream and identifies the song."""

    # capture_audio_sample(url)
    # song = identify_song()

    data = capture_audio_buffer(url)
    song = identify_song_from_buffer(data)

    print(song)


if __name__ == "__main__":
    sniff(url)
