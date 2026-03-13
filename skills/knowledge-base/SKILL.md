---
name: knowledge-base
description: "Semantic search over Obsidian vault using QMD embeddings - find notes by meaning, not just keywords"
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      config: []
---

# Knowledge Base - Obsidian Semantic Search

Search your entire Obsidian vault by meaning.

## Setup

### Initial Index

```bash
# Install QMD (if not already)
npm install -g qmd

# Build initial index
qmd index /path/to/vault --exclude ".obsidian,.trash,Templates"
```

### Nightly Reindex

```bash
# Cron: 3:00 AM daily
0 3 * * * qmd index /path/to/vault --update
```

## Excluded Directories

- `.obsidian/` - Obsidian config
- `.trash/` - Deleted notes
- `Templates/` - Note templates

## Query Examples

- "What did I decide about thumbnail design last month?"
- "Find my notes about AI agent security"
- "What were the key points from that article about prompt injection?"
- "How do I handle authentication in my apps?"

## Response Format

```
🔍 Found [N] relevant notes:

## [Note Title 1]
Path: /path/to/note.md
> [Relevant excerpt]

## [Note Title 2]  
Path: /path/to/other.md
> [Relevant excerpt]

---
Connections: [How these notes relate]
```

## Semantic vs Keyword

- **Keyword**: Finds exact word matches
- **Semantic**: Finds meaning matches

Example: "authentication" query also finds notes about "login", "OAuth", "session management"

## Connecting Notes

When multiple relevant notes found:
- Summarize connections between them
- Highlight contradictions or evolution of thought
- Suggest related notes to explore

## Vault Stats

```
📊 Vault Statistics:
- Notes: 2,800+
- Indexed: [count]
- Last reindex: [date]
- Size: [MB]
```

## Configuration

```bash
OBSIDIAN_VAULT_PATH=/path/to/vault
QMD_INDEX_PATH=~/.qmd/index
```
