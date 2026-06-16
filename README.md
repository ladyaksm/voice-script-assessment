# AI Engineer Assessment – Audio Analysis Agent (ffmpeg + LLM)

## Overview

This project implements an AI-powered audio analysis pipeline for legal deposition recordings.

The system combines deterministic audio signal analysis using **ffmpeg/ffprobe** with **LLM-based interpretation** to generate both structured machine-readable outputs and human-readable insights.

The objective is to identify potential audio quality issues before downstream transcription workflows.

---

## Assessment Requirements Coverage

| Requirement | Implementation |
|---|---|
| Extract metadata using ffprobe | ✅ Duration, bitrate, sample rate, channels |
| Detect silence segments | ✅ Using ffmpeg `silencedetect` |
| Detect unusually low volume | ✅ Using ffmpeg `volumedetect` |
| Detect potential clipping | ✅ Using maximum volume threshold |
| Generate structured JSON output | ✅ Per audio file |
| Generate human-readable insights | ✅ Using Gemini |
| Batch processing | ✅ Multiple files supported |
| Aggregate insights | ✅ `summaries.txt` generated |
| Architecture documentation | ✅ Included |
| Extensibility considerations | ✅ Included |
| Agentic approach | ⚪ Proposed as future extension |
| MCP integration | ⚪ Proposed as future extension |

---

## Features

### Audio Metadata Extraction

Using `ffprobe`, the system extracts:

- Duration
- Bitrate
- Sample Rate
- Number of Channels

---

### Audio Quality Analysis

Using ffmpeg filters, the system detects:

#### Silence Segments

Implemented using:

```bash
silencedetect
```

Outputs:

- Silence start time
- Silence end time
- Silence duration
- Overall silence ratio

#### Low Volume Detection

Implemented using:

```bash
volumedetect
```

Outputs:

- Average volume (dB)

#### Potential Clipping Detection

Implemented using:

```bash
volumedetect
```

Outputs:

- Maximum volume peak (dB)

A clipping warning is triggered when the maximum volume approaches 0 dB.

---

### Structured Reporting

For each audio file, the system generates a JSON report containing:

- Metadata
- Audio quality metrics
- Silence segments
- Detected issues
- Processing recommendations
- LLM-generated insights

---

### LLM Interpretation Layer

Gemini is used to transform structured findings into practical summaries.

The generated insights include:

- Overall assessment
- Potential transcription risks
- Recommended actions
- Suitability for downstream ASR

---

### Batch Processing

The pipeline automatically processes multiple audio files from the input directory and produces:

- Individual JSON reports
- Consolidated summaries

---

## Architecture

```
Input Audio Files
        │
        ▼
    ffprobe
(metadata extraction)
        │
        ▼
     ffmpeg
 ┌─────────────┬─────────────┐
 │             │             │
 ▼             ▼             ▼
Silence     Volume      Clipping
Detection   Analysis    Detection
        │
        ▼
 Rule-Based Validation
        │
        ▼
 Structured JSON Report
        │
        ▼
     Gemini LLM
(Interpretation Layer)
        │
        ▼
Human-Readable Insights
```

---

## Design Decisions

### Deterministic Analysis for Facts

All measurable audio characteristics are extracted directly from ffmpeg/ffprobe.

These measurements are treated as the source of truth.

Examples include:

- Duration
- Silence intervals
- Average volume
- Maximum volume peaks

This ensures that objective findings remain reproducible and explainable.

---

### LLM for Interpretation, Not Measurement

The LLM is intentionally limited to interpretation and recommendation tasks.

It does **not** generate measurements or infer unsupported technical findings.

Its responsibilities include:

- Summarising audio quality
- Highlighting operational risks
- Suggesting follow-up actions
- Assessing readiness for ASR

This separation improves:

- Reliability
- Explainability
- Maintainability
- Hallucination resistance

---

### Hybrid Pipeline Approach

This implementation combines traditional signal processing with modern LLM capabilities.

Deterministic tools provide objective analysis, while the LLM adds contextual understanding.

This reflects how production AI systems frequently integrate conventional pipelines with LLM reasoning.

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
    "bitrate": 47235,
    "sample_rate": 16000,
    "channels": 1,
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

## Example Human-Readable Insight

> This recording may require manual review before ASR processing due to the presence of clipping. Extended silence segments should also be reviewed to determine whether they represent intentional pauses or recording anomalies.

---

## Installation

### Prerequisites

- Python 3.10+
- ffmpeg
- ffprobe
- Gemini API Key

---

### Clone Repository

```bash
git clone <repository-url>
cd audio-assessment
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

Place supported audio files inside the `input/` directory.

Supported formats:

- `.mp3`
- `.wav`

Run:

```bash
python src/main.py
```

---

## Outputs

After execution, the system generates:

### JSON Reports

```
output/
├── bad_audio_report.json
├── moonlight-plaza_report.json
```

---

### Consolidated Summaries

```
output/
└── summaries.txt
```

---

## Optional Extensions

The following enhancements were considered but not implemented due to assessment scope.

### Agent-Based Tool Orchestration

An LLM agent could dynamically determine which analysis tools to invoke before composing the final report.

For example:

- Retrieve metadata
- Detect silence
- Detect clipping
- Aggregate findings
- Generate recommendations

---

### MCP Integration

Audio analysis capabilities could be exposed through an MCP server using tools such as:

- `get_audio_metadata`
- `detect_silence`
- `detect_clipping`

This would allow external agents to access the analysis pipeline through a standardized interface.

---

### Additional Audio Intelligence

Potential future improvements include:

- Noise analysis
- Signal-to-noise ratio estimation
- Speaker diarization
- Real-time streaming analysis
- Evaluation dashboards
- Automated quality scoring

---

## Notes

This project was developed as part of an AI Engineer technical assessment focused on practical AI engineering and systems thinking.

The implementation prioritises:

- Correctness
- Explainability
- Maintainability
- Extensibility
- Practical use of LLMs

rather than unnecessary architectural complexity.
