import json
from pathlib import Path
from datetime import datetime
from analyzer import get_audio_metadata
from analyzer import (
    get_audio_metadata,
    detect_silence,
    detect_volume
)
from llm import generate_insight

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_summaries = []

    # Process each audio file in the input directory
    for audio_file in INPUT_DIR.iterdir():
        if audio_file.suffix.lower() not in [".mp3", ".wav"]:
            continue

        metadata = get_audio_metadata(audio_file)
        
        # Analyze audio quality
        silences = detect_silence(audio_file)
        volume_info = detect_volume(audio_file)
        total_silence = sum(
            segment["duration"]
            for segment in silences
            )
        
        # Calculate silence ratio
        silence_ratio = round(
            total_silence / metadata["duration_seconds"], 3)

        issues = []

        # Identify potential issues based on analysis
        for segment in silences:
            if segment["duration"] >= 5:
                issues.append(
                     f"Long silence detected between "
                     f"{segment['start']}–{segment['end']} seconds"
                     )
                
        # Check for clipping and low volume
        if volume_info["clipping_detected"]:
            issues.append("Potential clipping detected.")
        
        # Check for unusually low average volume
        if (volume_info["avg_volume_db"] is not None and volume_info["avg_volume_db"] < -30 ):
            issues.append("Unusually low average volume detected.")
        
        # Determine overall processing recommendation
        processing_recommendation = "ready"
        if volume_info["clipping_detected"]:
            processing_recommendation = "manual_review"
        elif silence_ratio > 0.15:
            processing_recommendation = "review_silence"
        elif (volume_info["avg_volume_db"] is not None and volume_info["avg_volume_db"] < -30):
            processing_recommendation = "normalize_audio"

        # Compile report data
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            **metadata,
            "processing_recommendation": processing_recommendation,
            "audio_quality": {
                "silence_ratio": silence_ratio,
                "clipping_detected": volume_info["clipping_detected"],
                "avg_volume_db": volume_info["avg_volume_db"]
                },
            "issues": issues,
            "silence_segments": silences
            }
        
        # Generate LLM insight
        insight = generate_insight(report)
        report["llm_insight"] = insight

        # Append to overall summaries
        all_summaries.append(
            f"=== {audio_file.name} ===\n"
            f"{insight}\n\n")

        output_file = OUTPUT_DIR / f"{audio_file.stem}_report.json"

        with open(output_file, "w") as f:
            json.dump(report, f, indent=4)

        print(f"Processed: {audio_file.name}")

    # Write all summaries to a single text file
    summary_path = OUTPUT_DIR / "summaries.txt"

    with open(summary_path, "w", encoding="utf-8") as f:
        f.writelines(all_summaries)

    print("Generated summaries.txt")


if __name__ == "__main__":
    main()