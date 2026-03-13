---
name: zai-suite
description: "Complete Z.AI integration - Vision, OCR, Image Gen, Audio, Chat, Web Search & Reader. Use for any Z.AI service operations."
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env: ["Z_AI_API_KEY"]
---

# Z.AI Suite - Complete Integration

Unified access to all Z.AI services for agents.

## Services Available

| Service | Endpoint | Capability |
|---------|----------|------------|
| **Chat** | chat.z.ai | GLM-5, GLM-4.7 chat completions |
| **Vision** | MCP Server | Image analysis, video understanding, OCR |
| **Web Search** | MCP Server | Real-time web search |
| **Web Reader** | MCP Server | Full webpage content extraction |
| **OCR** | ocr.z.ai | Document/image text extraction |
| **Image** | image.z.ai | GLM-Image generation |
| **Audio** | audio.z.ai | GLM-ASR transcription |

## MCP Tools (via mcporter)

### Vision MCP Tools
Call via: `mcporter call zai-vision.<tool>`

- **`ui_to_artifact`** - Turn UI screenshots into code/specs
- **`extract_text_from_screenshot`** - OCR for code/terminals/docs
- **`diagnose_error_screenshot`** - Analyze error screenshots
- **`understand_technical_diagram`** - Architecture/flow/UML diagrams
- **`analyze_data_visualization`** - Charts and dashboards
- **`ui_diff_check`** - Compare two UI screenshots
- **`image_analysis`** - General image understanding
- **`video_analysis`** - Video scene/entity detection

### Web Search MCP
Call via: `mcporter call zai-web-search.webSearchPrime`

```bash
mcporter call zai-web-search.webSearchPrime query="latest AI developments"
```

### Web Reader MCP
Call via: `mcporter call zai-web-reader.webReader`

```bash
mcporter call zai-web-reader.webReader url="https://example.com"
```

## HTTP API Direct Calls

### Chat Completion (GLM-5)

```bash
curl https://api.z.ai/api/coding/paas/v4/chat/completions \
  -H "Authorization: Bearer $Z_AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Image Generation

```bash
curl https://api.z.ai/api/paas/v4/images/generations \
  -H "Authorization: Bearer $Z_AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-image",
    "prompt": "A cyberpunk city at sunset",
    "n": 1,
    "size": "1024x1024"
  }'
```

### Audio Transcription (ASR)

```bash
curl https://api.z.ai/api/paas/v4/audio/transcriptions \
  -H "Authorization: Bearer $Z_AI_API_KEY" \
  -F "file=@audio.mp3" \
  -F "model=glm-asr-2512"
```

### OCR / Layout Parsing

```bash
curl https://api.z.ai/api/paas/v4/tools/layout-parsing \
  -H "Authorization: Bearer $Z_AI_API_KEY" \
  -F "file=@document.pdf"
```

## Usage Examples

### Analyze an Image
```bash
mcporter call zai-vision.image_analysis image_path="/tmp/screenshot.png" prompt="What's in this image?"
```

### Search the Web
```bash
mcporter call zai-web-search.webSearchPrime query="Solana memecoin trends 2024"
```

### Read a Webpage
```bash
mcporter call zai-web-reader.webReader url="https://docs.solana.com"
```

### Transcribe Audio
```bash
# Upload audio file and get transcription
curl -X POST "https://api.z.ai/api/paas/v4/audio/transcriptions" \
  -H "Authorization: Bearer $Z_AI_API_KEY" \
  -F "file=@recording.mp3" \
  -F "model=glm-asr-2512"
```

## Environment Setup

Ensure `Z_AI_API_KEY` is set in your environment or `.env` file.

Get your API key at: https://z.ai/manage-apikey/apikey-list

## Quotas (Coding Plan)

| Plan | Web Search/Reader | Vision Pool |
|------|------------------|-------------|
| Lite | 100 total | 5 hours |
| Pro | 1,000 total | 5 hours |
| Max | 4,000 total | 5 hours |
