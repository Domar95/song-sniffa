import time
import io

from streamlink import Streamlink


class AudioCapturer:
    def __init__(self, url: str, chunk_size: int = 4096):
        self.url = url
        self.chunk_size = chunk_size
        self.session = Streamlink()
        self.stream = self._get_stream()

    def to_file(
        self, output_path: str = "samples/sniffa_sample.mp3", duration: int = 15
    ) -> str:
        """Fetch a sample audio stream and save it to a file."""

        start = time.time()

        with self.stream.open() as fd, open(output_path, "wb") as f:
            while time.time() - start < duration:
                chunk = fd.read(self.chunk_size)
                if not chunk:
                    break
                f.write(chunk)

        print(f"Sample saved to {output_path}.")

        return output_path

    def to_buffer(self, duration: int = 15) -> bytes:
        """Fetch a sample audio stream and return it as a bytes buffer."""

        buffer = io.BytesIO()
        start = time.time()

        with self.stream.open() as fd:
            while time.time() - start < duration:
                chunk = fd.read(self.chunk_size)
                if not chunk:
                    break
                buffer.write(chunk)

        print(f"Captured audio buffer of size {buffer.tell()} bytes.")

        return buffer.getvalue()

    def _get_stream(self):
        """Initialize the audio stream."""

        self.session.set_option("twitch-disable-ads", True)
        streams = self.session.streams(self.url)
        stream = streams.get("audio_only")
        if not stream:
            raise RuntimeError("No audio stream available for the provided URL.")
        return stream
