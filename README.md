# Voice agents workshop

Build a voice agent that listens, thinks, and speaks  - from scratch, in your browser.

This workshop walks you through building voice agents with [LiveKit Agents](https://docs.livekit.io/agents/), starting with a cascaded STT → LLM → TTS pipeline and progressing to realtime speech-to-speech models, tool calling, and telephony.

## What you'll build

A voice-powered AI assistant that you can talk to through your browser. You'll start with a basic implementation and progressively add customization, tool calling, and alternative architectures.

## Prerequisites

- Python 3.9+
- git
- A code editor
- A microphone and headphones (earbuds work  - speakers cause echo)
- Chrome browser (recommended for WebRTC)
- A [LiveKit Cloud](https://cloud.livekit.io) account (free tier)
- API keys (provided during the workshop, or bring your own)

## Setup

Clone the repo and install dependencies:

```bash
git clone https://github.com/johnx25bd/workshop-voice-agents.git
cd workshop-voice-agents
```

With [uv](https://docs.astral.sh/uv/) (recommended):
```bash
uv sync
```

Or with pip:
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy the environment template and fill in your API keys:
```bash
cp .env.example .env
```

## Tutorial

Work through the phases in order. Each phase builds on the previous one.

1. **[Phase 1: Build a voice agent](docs/phase-1.md)**  - Get a basic cascaded pipeline running
2. **[Phase 2: Make it yours](docs/phase-2.md)**  - Custom persona, voice selection, tuning behavior
3. **[Phase 3: Add tool calling](docs/phase-3.md)**  - Give your agent the ability to take actions
4. **[Phase 4: Realtime models](docs/phase-4.md)**  - Swap to a speech-to-speech model and compare
5. **[Phase 5: Telephony](docs/phase-5.md)**  - Connect your agent to a phone number

If you get stuck on any phase, the bottom of each tutorial page includes full solution code in a dropdown.

## Project structure

```
agent.py              ← Your voice agent (start here)
.env.example          ← API key template
docs/                 ← Tutorial for each phase
  phase-1.md
  phase-2.md
  phase-3.md
  phase-4.md
  phase-5.md
```

## Resources

- [Workshop slides](https://docs.google.com/presentation/d/1OUmVp-3GC0Ujf8bEC0RjZi7UsEn_k8eyduCgCkIYQng/edit?usp=sharing)
- [LiveKit Agents docs](https://docs.livekit.io/agents/)
- [LiveKit Agents Playground](https://agents-playground.livekit.io)  - browser UI for testing your agent

## License

MIT
