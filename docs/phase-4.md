# Phase 4: Speech-to-speech models

So far you've been running a cascaded pipeline where separate models handle STT, LLM, and TTS. Now you'll swap that out for a single speech-to-speech model and see how it feels different.

## The difference

Cascaded:
```
Audio → [STT] → Text → [LLM] → Text → [TTS] → Audio
```

Speech-to-speech:
```
Audio → [Single Model] → Audio
```

One model, no text intermediate. Audio goes in, audio comes out. That means lower latency (two inference steps gone), better prosody preservation (no lossy text bottleneck), but less visibility into what's happening (no text to inspect or log).

## Make the swap

Replace your `AgentSession` configuration:

<details>
<summary>Cascaded (what you have now)</summary>

```python
session = AgentSession(
    stt=openai.STT(model="gpt-4o-transcribe"),
    llm="openai/gpt-4.1-mini",
    tts=openai.TTS(voice="coral"),
    vad=silero.VAD.load(),
)
```

</details>

<details>
<summary>Speech-to-speech</summary>

```python
from livekit.plugins import openai

session = AgentSession(
    llm=openai.realtime.RealtimeModel(voice="coral"),
)
```

No `stt`, no `tts`, no `vad`. The realtime model handles all of that internally.

</details>

Restart your agent and connect from the frontend.

## Compare them

Swap back and forth. Have the same conversation with both versions. Pay attention to:

- **Latency** - which responds faster?
- **Naturalness** - rhythm, intonation, pacing. Which sounds more human?
- **Prosody** - say something sarcastic, or excited, or frustrated. Does the speech-to-speech version pick up on your tone? Does the cascaded version?
- **Interruptions** - talk over the agent mid-sentence. What happens with each?
- **Tool calling** - if you added tools in phase 3, do they still work? The realtime model handles function calls differently (it emits them alongside audio rather than in a text stream)
- **Accuracy** - are the answers better or worse without a text stage?

## Available voices

OpenAI's realtime model voices: `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`. Try a few. They have noticeably different characters.

LiveKit also supports Google's Gemini realtime model via `google.realtime.RealtimeModel`.

## Checkpoint

You've now used both architectures. Think about the agent you built in phase 2. Which architecture fits that use case better? Why?

If you want to keep going: **[Phase 5: Telephony](phase-5.md)**.
