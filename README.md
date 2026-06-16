# VoiceScript Assessment – Audio Analysis Agent

## Overview

This project is an AI-powered audio analysis pipeline designed for legal deposition recordings. It combines deterministic audio signal analysis using **ffmpeg/ffprobe** with **LLM-based interpretation** to generate structured reports and actionable insights.

The system extracts technical metadata, detects potential audio quality issues, and produces both machine-readable JSON outputs and human-readable summaries.

The goal is to support downstream legal transcription workflows by identifying potential risks before Automated Speech Recognition (ASR) processing.

---

## Features

### Audio Analysis

* Extract audio metadata using `ffprobe`

  * Duration
  * Bitrate
  * Sample rate
  * Number of channels

### Audio Quality Checks

* Silence detection using `ffmpeg silencedetect`
* Average volume analysis using `ffmpeg volumedetect`
* Potential clipping detection

### Structured Reporting

* JSON report generation for each audio file
* Processing recommendations
* Detected issues and silence segments

### LLM Layer (Gemini)

* Generates human-readable insights
* Identifies potential transcription risks
* Suggests practical next steps
* Evaluates suitability for downstream ASR

### Batch Processing

* Processes multiple audio files automatically
* Produces consolidated summaries

---

## Architecture

```
Audio Files
     │
     ▼
ffprobe
(metadata extraction)
     │
     ▼
ffmpeg filters
├─ silencedetect
└─ volumedetect
     │
     ▼
Rule-based validation
(issue detection)
     │
     ▼
Structured JSON Report
     │
     ▼
Gemini LLM
(interprets findings)
     │
     ▼
Human-readable Summary
```

---

## Design Decisions

### Deterministic Analysis for Facts

Measurable audio characteristics such as duration, silence segments, volume levels, and clipping indicators are extracted directly using ffmpeg/ffprobe.

These values are treated as the source of truth.

### LLM for Interpretation Only

The LLM is intentionally limited to interpretation and recommendation tasks.

It does not generate measurements or infer unsupported conclusions.

This separation:

* improves reliability,
* reduces hallucination risk,
* keeps the system explainable,
* and maintains low operational cost.

### Hybrid Pipeline

The project combines traditional signal processing with modern LLM capabilities.

This approach leverages the strengths of both:

* deterministic tools for objective analysis,
* LLMs for contextual summarisation.

---

## Project Structure

```
audio-assessment/
├── input/
├── output/
├── src/
│   ├── analyzer.py
│   ├── llm.py
│   ├── report.py
│   └── main.py
├── requirements.txt
├── README.md
└── .env
```

---

## Example JSON Output

```json
{
    "analysis_timestamp": "2026-06-16T13:15:19",
    "file_name": "bad_audio.mp3",
    "duration_seconds": 51.7,
    "audio_quality": {
        "silence_ratio": 0.152,
        "clipping_detected": true,
        "avg_volume_db": -16.6,
        "max_volume_db": -0.4
    },
    "processing_recommendation": "manual_review",
    "issues": [
        "Long silence detected between 32.39–39.43 seconds",
        "Potential clipping detected."
    ]
}
```

---

## Example LLM Insight

> The detected clipping may negatively affect downstream ASR performance. Manual review is recommended before transcription. Long silence segments should also be reviewed to determine whether they represent intentional pauses or recording anomalies.

---

## Installation

### Prerequisites

* Python 3.10+
* ffmpeg
* ffprobe
* Gemini API Key

### Clone Repository

```bash
git clone <repository-url>
cd audio-assessment
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

Place audio files inside the `input/` directory.

Supported formats:

* `.mp3`
* `.wav`

Run:

```bash
python src/main.py
```

---

## Outputs

The system generates:

### JSON Reports

```
output/
├── bad_audio_report.json
├── moonlight-plaza_report.json
```

### Human-readable Summaries

```
output/
└── summaries.txt
```

---

## Future Improvements

Potential extensions include:

* Agent-based tool orchestration
* MCP server integration
* Noise analysis and SNR estimation
* Speaker diarization support
* Automated evaluation dashboards
* Real-time streaming analysis

---

## Notes

This project was designed as a technical assessment focused on practical AI engineering.

The implementation prioritises:

* correctness,
* explainability,
* maintainability,
* and extensibility over unnecessary complexity.

```
```
