import subprocess
import json
from pathlib import Path
import re

# Audio analysis functions
def get_audio_metadata(file_path):
    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(file_path)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )

    data = json.loads(result.stdout)

    stream = data["streams"][0]
    format_data = data["format"]

    return {
        "file_name": Path(file_path).name,
        "duration_seconds": round(float(format_data["duration"]), 2),
        "bitrate": int(format_data.get("bit_rate", 0)),
        "sample_rate": int(stream.get("sample_rate", 0)),
        "channels": stream.get("channels", 0)
    }

# Silence detection 
def detect_silence(file_path):
    command = [
        "ffmpeg",
        "-i", str(file_path),
        "-af", "silencedetect=noise=-30dB:d=2",
        "-f", "null",
        "-"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    stderr = result.stderr

    silence_starts = re.findall(r"silence_start: ([\d\.]+)", stderr)
    silence_ends = re.findall(
        r"silence_end: ([\d\.]+) \| silence_duration: ([\d\.]+)",
        stderr
    )

    segments = []

    for start, (end, duration) in zip(silence_starts, silence_ends):
        segments.append({
            "start": round(float(start), 2),
            "end": round(float(end), 2),
            "duration": round(float(duration), 2)
        })

    return segments

# Volume analysis
def detect_volume(file_path):
    command = [
        "ffmpeg",
        "-i", str(file_path),
        "-af", "volumedetect",
        "-f", "null",
        "-"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    stderr = result.stderr

    mean_match = re.search(
        r"mean_volume:\s*(-?\d+\.?\d*) dB",
        stderr
    )

    max_match = re.search(
        r"max_volume:\s*(-?\d+\.?\d*) dB",
        stderr
    )

    mean_volume = float(mean_match.group(1)) if mean_match else None
    max_volume = float(max_match.group(1)) if max_match else None

    clipping_detected = (
        max_volume is not None and max_volume > -1
    )

    return {
        "avg_volume_db": mean_volume,
        "max_volume_db": max_volume,
        "clipping_detected": clipping_detected
    }