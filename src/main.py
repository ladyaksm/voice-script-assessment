import json
from pathlib import Path

from analyzer import (get_audio_metadata, detect_silence, detect_volume)
from llm import generate_insight
from report import (generate_issues, get_processing_recommendation, build_report)

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
SUPPORTED_FORMATS = [".mp3", ".wav"]

def save_report(audio_file, report):
    output_file = OUTPUT_DIR / f"{audio_file.stem}_report.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)


def save_summaries(all_summaries):
    summary_path = OUTPUT_DIR / "summaries.txt"

    with open(summary_path, "w", encoding="utf-8") as f:
        f.writelines(all_summaries)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    all_summaries = []

    for audio_file in INPUT_DIR.iterdir():

        if audio_file.suffix.lower() not in SUPPORTED_FORMATS:
            continue

        metadata = get_audio_metadata(audio_file)

        silences = detect_silence(audio_file)

        volume_info = detect_volume(audio_file)

        total_silence = sum(
            segment["duration"]
            for segment in silences
        )

        silence_ratio = round(
            total_silence / metadata["duration_seconds"],
            3
        )

        issues = generate_issues(
            silences,
            volume_info
        )

        recommendation = get_processing_recommendation(
            silence_ratio,
            volume_info
        )

        report = build_report(
            metadata,
            silence_ratio,
            silences,
            volume_info,
            issues,
            recommendation
        )

        try:
            insight = generate_insight(report)

        except Exception as e:
            insight = f"LLM generation failed: {e}"

        report["llm_insight"] = insight

        save_report(audio_file, report)

        all_summaries.append(
            f"=== {audio_file.name} ===\n"
            f"{insight}\n\n"
        )

        print(f"Processed: {audio_file.name}")

    save_summaries(all_summaries)

    print("Generated summaries.txt")


if __name__ == "__main__":
    main()