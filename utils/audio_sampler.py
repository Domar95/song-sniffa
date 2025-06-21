import time
import io

from streamlink import Streamlink


def capture_audio_sample(
    url: str, output_path: str = "samples/sniffa_sample.mp3", duration: int = 20
) -> None:
    """Fetch a sample audio stream and save it to a file."""

    session = Streamlink()
    streams = session.streams(url)
    stream = streams.get("audio_only")

    if not stream:
        print("Stream not found.")
        return

    start = time.time()

    with stream.open() as fd, open(output_path, "wb") as f:
        while time.time() - start < duration:
            chunk = fd.read(4096)
            if not chunk:
                break
            f.write(chunk)

    print(f"Sample saved to {output_path}.")


def capture_audio_buffer(url: str, duration: int = 15) -> bytes:
    session = Streamlink()
    streams = session.streams(url)
    stream = streams.get("audio_only")

    if not stream:
        raise RuntimeError("No audio stream available")

    buffer = io.BytesIO()
    start = time.time()

    with stream.open() as fd:
        while time.time() - start < duration:
            chunk = fd.read(4096)
            if not chunk:
                break
            buffer.write(chunk)

    print(f"Captured audio buffer of size {buffer.tell()} bytes.")

    return buffer.getvalue()
