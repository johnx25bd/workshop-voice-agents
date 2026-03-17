# Phase 2: Make it yours

Your agent works. Now make it interesting. In this phase you'll give it a persona, experiment with different voices, and tune its behavior.

## Give it a persona

The `instructions` in your `Agent` class are a system prompt — they shape everything about how the agent behaves. A generic "helpful assistant" is functional but forgettable. A well-defined persona is engaging and memorable.

Think about:
- **Who** is this agent? (A character, a professional role, an expert in something specific?)
- **How** does it speak? (Formal? Casual? Enthusiastic? Deadpan?)
- **What** constraints should it have? (Stay on topic? Avoid certain subjects? Always ask follow-up questions?)

Try updating your agent's instructions. Be specific — vague instructions produce vague behavior.

<details>
<summary>Example: a film noir detective</summary>

```python
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a hardboiled private detective from a 1940s film noir.
            You speak in short, clipped sentences with a world-weary tone.
            You refer to everyone as "kid" or "pal."
            You relate everything back to detective metaphors.
            You're helpful, but you make it sound like you've seen it all before.
            Keep responses to 2-3 sentences max.""",
        )
```

</details>

<details>
<summary>Example: a cooking coach</summary>

```python
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are an enthusiastic home cooking coach.
            You help people cook with whatever they have in their kitchen.
            Ask what ingredients they have before suggesting recipes.
            Give instructions one step at a time — don't overwhelm.
            Be encouraging and practical, not fancy.
            Keep responses conversational and concise.""",
        )
```

</details>

## Change the voice

The TTS model determines what your agent sounds like. Different providers offer different voices with different qualities.

In your `AgentSession`, the `tts` parameter controls this. Try swapping providers or voices:

```python
# Cartesia — low latency, good for real-time
tts="cartesia/sonic-3"

# OpenAI TTS — good quality, several voice options
tts="openai/tts-1:nova"    # warm, conversational
tts="openai/tts-1:onyx"    # deep, authoritative
tts="openai/tts-1:shimmer" # clear, expressive
```

Experiment — the voice should match your persona. A noir detective probably shouldn't sound like a cheerful assistant.

<details>
<summary>Go deeper: Voice cloning and speaker embeddings</summary>

Some TTS providers (like ElevenLabs) support **voice cloning** — you provide a short audio sample of a target voice, and the model extracts a **speaker embedding**: a vector that captures the unique characteristics of that voice (timbre, pitch range, resonance, rhythm).

The TTS model then generates new speech that sounds like that person. This enables brand-consistent voices, personalized agents, or character voices, but raises real ethical questions around consent and deepfakes.

</details>

## Tune the behavior

Beyond the persona, you can adjust how the agent interacts:

### Initial greeting

The `generate_reply` call at the end of your session handler controls what the agent says first. Make it fit your persona:

```python
await session.generate_reply(
    instructions="Introduce yourself as Detective Murphy and ask what case the user needs help with."
)
```

### Response style

Experiment with your instructions to control:
- **Length** — "Keep responses to one or two sentences" vs. "Provide detailed explanations"
- **Questioning** — "Always ask a follow-up question" vs. "Only answer what was asked"
- **Tone** — "Be formal and professional" vs. "Be casual and use humor"
- **Scope** — "Only discuss cooking topics" vs. "Help with anything"

## Try it

1. Update your agent's persona and instructions
2. Change the TTS voice to match
3. Customize the initial greeting
4. Run `python agent.py dev` and have a conversation
5. Iterate — the instructions rarely work perfectly on the first try

## Checkpoint

You should now have a voice agent with a distinct persona, an appropriate voice, and a tailored greeting. Talk to it for a few minutes — does the persona hold? Does the voice match? Tweak until it feels right.

When you're ready, move on to **[Phase 3: Add tool calling](phase-3.md)**.
