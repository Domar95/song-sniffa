import base64
import hashlib
import hmac
import os
import requests
import time

from dotenv import load_dotenv


def identify_song(file_path: str = "samples/sniffa_sample.mp3") -> str:
    """Sends an audio file to the ACRCloud service for recognition."""

    # You can get your access_key and access_secret from https://console.acrcloud.com
    config = _get_config()
    access_key = config.get("access_key")
    access_secret = config.get("access_secret")
    requrl = config.get("host")

    http_method = "POST"
    http_uri = "/v1/identify"
    # default is "fingerprint", it's for recognizing fingerprint,
    # if you want to identify audio, please change data_type="audio"
    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    string_to_sign = (
        http_method
        + "\n"
        + http_uri
        + "\n"
        + access_key
        + "\n"
        + data_type
        + "\n"
        + signature_version
        + "\n"
        + str(timestamp)
    )

    sign = base64.b64encode(
        hmac.new(
            access_secret.encode("ascii"),
            string_to_sign.encode("ascii"),
            digestmod=hashlib.sha1,
        ).digest()
    ).decode("ascii")

    # suported file formats: mp3,wav,wma,amr,ogg, ape,acc,spx,m4a,mp4,FLAC, etc
    # File size: < 1M , You'de better cut large file to small file, within 15 seconds data size is better
    sample_bytes = os.path.getsize(file_path)

    files = [("sample", (file_path, open(file_path, "rb"), "audio/mpeg"))]
    data = {
        "access_key": access_key,
        "sample_bytes": sample_bytes,
        "timestamp": str(timestamp),
        "signature": sign,
        "data_type": data_type,
        "signature_version": signature_version,
    }

    r = requests.post(requrl, files=files, data=data)
    r.encoding = "utf-8"
    return r.text


def identify_song_from_buffer(audio_data: bytes) -> str:
    """Sends an audio file to the ACRCloud service for recognition."""

    # You can get your access_key and access_secret from https://console.acrcloud.com
    config = _get_config()
    access_key = config.get("access_key")
    access_secret = config.get("access_secret")
    requrl = config.get("host")

    http_method = "POST"
    http_uri = "/v1/identify"
    # default is "fingerprint", it's for recognizing fingerprint,
    # if you want to identify audio, please change data_type="audio"
    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    string_to_sign = (
        http_method
        + "\n"
        + http_uri
        + "\n"
        + access_key
        + "\n"
        + data_type
        + "\n"
        + signature_version
        + "\n"
        + str(timestamp)
    )

    sign = base64.b64encode(
        hmac.new(
            access_secret.encode("ascii"),
            string_to_sign.encode("ascii"),
            digestmod=hashlib.sha1,
        ).digest()
    ).decode("ascii")

    encoded_audio = base64.b64encode(audio_data).decode("ascii")

    # suported file formats: mp3,wav,wma,amr,ogg, ape,acc,spx,m4a,mp4,FLAC, etc
    # File size: < 1M , You'de better cut large file to small file, within 15 seconds data size is better

    data = {
        "access_key": access_key,
        "sample_bytes": len(audio_data),
        "sample": encoded_audio,
        "timestamp": str(timestamp),
        "signature": sign,
        "data_type": data_type,
        "signature_version": signature_version,
    }

    r = requests.post(requrl, data=data)
    r.encoding = "utf-8"
    return r.text


def _get_config() -> dict:
    """Load configuration from environment variables."""

    load_dotenv()

    return {
        "host": os.getenv("ACR_HOST"),
        "access_key": os.getenv("ACR_ACCESS_KEY"),
        "access_secret": os.getenv("ACR_SECRET_KEY"),
        "timeout": 10,
    }
