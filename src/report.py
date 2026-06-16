from datetime import datetime

LONG_SILENCE_THRESHOLD = 5
LOW_VOLUME_THRESHOLD = -30


def generate_issues(silences, volume_info):
    issues = []

    for segment in silences:
        if segment["duration"] >= LONG_SILENCE_THRESHOLD:
            issues.append(
                f"Long silence detected between "
                f"{segment['start']}–{segment['end']} seconds"
            )

    if volume_info["clipping_detected"]:
        issues.append("Potential clipping detected.")

    if (
        volume_info["avg_volume_db"] is not None
        and volume_info["avg_volume_db"] < LOW_VOLUME_THRESHOLD
    ):
        issues.append("Unusually low average volume detected.")

    return issues


def get_processing_recommendation(
    silence_ratio,
    volume_info
):
    if volume_info["clipping_detected"]:
        return "manual_review"

    if silence_ratio > 0.15:
        return "review_silence"

    if (
        volume_info["avg_volume_db"] is not None
        and volume_info["avg_volume_db"] < LOW_VOLUME_THRESHOLD
    ):
        return "normalize_audio"

    return "ready"


def build_report(
    metadata,
    silence_ratio,
    silences,
    volume_info,
    issues,
    recommendation
):
    return {
        "analysis_timestamp": datetime.now().isoformat(),

        **metadata,

        "audio_quality": {
            "silence_ratio": silence_ratio,
            "clipping_detected": volume_info["clipping_detected"],
            "avg_volume_db": volume_info["avg_volume_db"],
            "max_volume_db": volume_info["max_volume_db"]
        },

        "processing_recommendation": recommendation,

        "issues": issues,

        "silence_segments": silences
    }