# Phase 4: Realtime models

You've built a cascaded pipeline  - separate models for STT, LLM, and TTS, piped together. Now you'll swap to a **speech-to-speech** model that handles everything in one step, and compare the experience.

## What's different?

In the cascaded pipeline:
```
Audio → [STT] → Text → [LLM] → Text → [TTS] → Audio
```

With a realtime model:
```
Audio → [Single Model] → Audio
```

One model does it all. No transcription step, no text-to-speech step. Audio in, audio out.

This means:
- **Lower latency**  - two inference steps eliminated
- **Prosody preservation**  - tone, emotion, and emphasis carry through end-to-end
- **Less control**  - no text to inspect, filter, or log mid-pipeline

## Make the swap

The code change is small. That's the point of LiveKit's abstraction  - the framework handles the plumbing, you just swap the model.

In your `AgentSession`, replace the cascaded configuration with a realtime model:

<details>
<summary>Before (cascaded)</summary>

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
<summary>After (realtime)</summary>

```python
from livekit.plugins import openai

session = AgentSession(
    llm=openai.realtime.RealtimeModel(voice="coral"),
)
```

That's it. No `stt`, no `tts`, no `vad`  - the realtime model handles all of those internally.

</details>

## The exercise: compare

The learning here isn't in the code change  - it's in *experiencing* the architectural difference you learned about in the lecture. The swap takes two minutes. The comparison is the real work.

### Talk to both versions

1. **Run your cascaded agent** (`python agent.py dev`). Have a conversation for a few minutes. Pay attention to how it feels
2. **Swap to the realtime model** and restart. Have the same conversation. Pay attention again

### What to notice

As you go back and forth, consider:

- **Latency**  - which responds faster? Is the difference noticeable?
- **Naturalness**  - which sounds more like talking to a person? Is there a difference in rhythm, intonation, pacing?
- **Prosody**  - try saying something with strong emotion (frustration, excitement, sarcasm). Does the agent's response reflect your tone in the realtime version? What about cascaded?
- **Interruption handling**  - try talking over the agent mid-sentence. How does each version handle it?
- **Accuracy**  - does one give better or worse answers? Does removing the text stage affect response quality?

### Try your tools

If you added tool calling in phase 3, try triggering it with the realtime model. What happens? Does it still work? The realtime model handles function calls by emitting them alongside audio  - LiveKit Agents manages this for you, but the experience may differ.

### Write down three observations

Seriously  - write them down. These observations are the experiential version of the architectural tradeoffs from the lecture. You now have a felt sense of what "prosody loss at the text boundary" and "latency reduction from eliminating inference steps" actually mean in practice.

## Available realtime models

LiveKit supports several realtime model providers:

| Model | Provider | Notes |
|---|---|---|
| `openai.realtime.RealtimeModel` | OpenAI | Most mature, multiple voice options |
| `google.realtime.RealtimeModel` | Google (Gemini) | Gemini Live, multimodal |

Voice options for OpenAI's realtime model include: `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`. Try a few  - they have noticeably different personalities.

## Checkpoint

You've now experienced both voice agent architectures firsthand. You should have a clear sense of the tradeoffs  - not just theoretically, but from feeling the difference.

Think about: for the persona you built in phase 2, which architecture is a better fit? Why?

If you're done, you can move on to the stretch goal: **[Phase 5: Telephony](phase-5.md)**.
