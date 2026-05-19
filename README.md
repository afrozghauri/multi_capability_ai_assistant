# Multi-Capability AI Assistant

A Python-based AI assistant that combines three capabilities and four tools to handle a variety of requests intelligently.

## Capabilities

- **Email Writer**: Writes complete emails with subject lines. Supports formal, friendly, and casual tones. Automatically researches topics using news before writing when relevant.
- **Smart Summarizer**: Summarizes any text into 1-5 sentences depending on length preference. Shows original word count, summary word count, and reduction percentage.
- **Chat Assistant**: General-purpose conversational assistant with memory. Remembers previous exchanges within a session and can answer follow-up questions.

## Tools

- **Calculator**: Evaluates mathematical expressions including advanced functions like sqrt, sin, cos.
- **Web Search**: Searches the web using DuckDuckGo and returns real results.
- **Data Analyzer**: Accepts a list of numbers and returns count, sum, average, min, and max.
- **News Fetcher**: Fetches the latest real news headlines on any topic using NewsAPI.

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
    pip install -r requirements.txt
```
4. Copy `.env.example` to `.env` and add your API keys:
```bash
    cp .env.example .env
```

## Configuration

Get your API keys from:
- OpenAI: https://platform.openai.com
- NewsAPI: https://newsapi.org

## Usage

```bash
python assistant.py
```

## Example Interactions

**Email Writer:**
You: write a formal email about requesting sick leave
**Summarizer:**
You: summarize: [paste any text here]
You: write a short summary of: [paste any text here]
**Chat:**
You: what is a quantum computer?
You: how does that compare to a regular computer?

**Tools via Chat:**
You: what is sqrt(256) + 100?
You: analyze this data: 5, 10, 15, 20, 25
You: get me the latest news about climate change
You: search the web for machine learning tutorials

## Commands

- `help` — show available capabilities and tools
- `quit` / `exit` / `bye` — exit the assistant
