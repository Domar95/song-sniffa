import base64
import hashlib
import hmac
import os
import requests
import time
import json

from dotenv import load_dotenv


class ACRClient:
    def __init__(self):
        # You can get your access_key and access_secret from https://console.acrcloud.com
        load_dotenv()
        self.access_key = os.getenv("ACR_ACCESS_KEY")
        self.access_secret = os.getenv("ACR_SECRET_KEY")
        self.host = os.getenv("ACR_HOST")
        self.timeout = 10
        self.http_uri = "/v1/identify"
        self.data_type = "audio"
        self.signature_version = "1"

    def identify_from_file(self, file_path: str = "samples/sniffa_sample.mp3") -> str:
        """Sends an audio file to the ACRCloud service for recognition."""

        timestamp = time.time()
        signature = self._generate_signature(timestamp)
        sample_bytes = os.path.getsize(file_path)

        files = [("sample", (file_path, open(file_path, "rb"), "audio/mpeg"))]
        data = {
            "access_key": self.access_key,
            "sample_bytes": sample_bytes,
            "timestamp": str(timestamp),
            "signature": signature,
            "data_type": self.data_type,
            "signature_version": self.signature_version,
        }

        return self._send_request(data, files)

    def identify_from_buffer(self, audio_data: bytes) -> str:
        """Sends audio data to the ACRCloud service for recognition."""

        timestamp = time.time()
        signature = self._generate_signature(timestamp)

        encoded_audio = base64.b64encode(audio_data).decode("ascii")

        data = {
            "access_key": self.access_key,
            "sample_bytes": len(audio_data),
            "sample": encoded_audio,
            "timestamp": str(timestamp),
            "signature": signature,
            "data_type": self.data_type,
            "signature_version": self.signature_version,
        }

        return self._send_request(data)

    def analyze_songs(self, songs_data: str) -> dict:
        """Analyzes song result."""

        try:
            response = json.loads(songs_data)
        except ValueError as e:
            raise ValueError(f"Invalid JSON response: {e}") from e

        songs = response.get("metadata", {}).get("music", [])

        filtered_songs = []

        for song in songs:
            if song.get("score", 0) >= 70:
                filtered_songs.append(
                    {
                        "title": song.get("title", "Unknown title"),
                        "artists": [
                            artist.get("name", "Unknown artist")
                            for artist in song.get("artists", [])
                        ],
                        "album": song.get("album", {}).get("name", "Unknown album"),
                    }
                )

        return self._format_response(filtered_songs)

    def _format_response(self, songs: []) -> str:
        """Formats the response to a readable string."""

        if not songs:
            return ""

        formatted_songs = []
        for song in songs:
            title = song.get("title", "Unknown title")
            artists = ", ".join(song.get("artists", ["Unknown artist"]))
            album = song.get("album", "Unknown album")
            formatted_songs.append(f"{artists} - {title} (album: {album})")

        return "  or  ".join(set(formatted_songs))

    def _generate_signature(self, timestamp: float) -> str:
        string_to_sign = "\n".join(
            [
                "POST",
                self.http_uri,
                self.access_key,
                self.data_type,
                self.signature_version,
                str(timestamp),
            ]
        )

        return base64.b64encode(
            hmac.new(
                self.access_secret.encode("ascii"),
                string_to_sign.encode("ascii"),
                digestmod=hashlib.sha1,
            ).digest()
        ).decode("ascii")

    def _send_request(self, data: dict, files: list = None) -> str:
        """Sends a POST request."""

        response = requests.post(
            self.host,
            data=data,
            files=files,
        )
        response.encoding = "utf-8"
        return response.text
