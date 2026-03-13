---
name: perplexity
description: "Perplexity AI search integration - Sonar, Pro Search, grounded LLM responses with citations. Use for real-time research and fact-checked answers."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      env: ["PERPLEXITY_API_KEY"]
---

# Perplexity AI Integration

Access Perplexity's Sonar models for grounded, citation-backed responses.

## Models Available

| Model | Description | Best For |
|-------|-------------|----------|
| `sonar` | Fast, lightweight search | Quick lookups |
| `sonar-pro` | Deep research with more sources | Comprehensive research |
| `sonar-reasoning` | Reasoning + search | Complex analysis |
| `sonar-reasoning-pro` | Advanced reasoning + deep search | Expert-level research |

## API Endpoints

### Chat Completions (with Search)

```bash
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [
      {"role": "user", "content": "What are the latest developments in Solana DeFi?"}
    ]
  }'
```

### Search API

```bash
curl https://api.perplexity.ai/search \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": ["What is Pump.fun?", "Solana token launches"]
  }'
```

### Responses API (Agentic)

```bash
curl https://api.perplexity.ai/v1/responses \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "preset": "pro-search",
    "input": "Analyze the current memecoin market on Solana"
  }'
```

## Advanced Options

### Domain Filtering
```json
{
  "web_search_options": {
    "search_domain_filter": ["arxiv.org", "github.com"],
    "search_recency_filter": "week"
  }
}
```

### Structured Output
```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "schema": {
        "type": "object",
        "properties": {
          "summary": {"type": "string"},
          "sources": {"type": "array"}
        }
      }
    }
  }
}
```

## Usage Examples

### Quick Search
```bash
# Fast web search
curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sonar", "messages": [{"role": "user", "content": "Current BTC price"}]}' | jq '.choices[0].message.content'
```

### Deep Research
```bash
# Comprehensive research with citations
curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar-pro",
    "messages": [{"role": "user", "content": "Analyze the competitive landscape of AI coding assistants"}]
  }' | jq '.'
```

### Recent News Only
```bash
# Search only recent sources
curl -s https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sonar",
    "messages": [{"role": "user", "content": "AI news today"}],
    "web_search_options": {"search_recency_filter": "day"}
  }'
```

## Response Format

Perplexity responses include:
- `content` - The answer text
- `citations` - Source URLs
- `search_results` - Structured search data

```json
{
  "choices": [{
    "message": {
      "content": "Answer text here...",
      "citations": ["https://source1.com", "https://source2.com"]
    }
  }]
}
```

## Get API Key

1. Go to https://perplexity.ai/settings/api
2. Generate an API key
3. Set `PERPLEXITY_API_KEY` environment variable

## Pricing

| Model | Input | Output |
|-------|-------|--------|
| sonar | $1/1M tokens | $1/1M tokens |
| sonar-pro | $3/1M tokens | $15/1M tokens |
| sonar-reasoning | $1/1M tokens | $5/1M tokens |
| sonar-reasoning-pro | $2/1M tokens | $8/1M tokens |
