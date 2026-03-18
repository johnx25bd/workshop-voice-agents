# Phase 2: Make it yours

Your agent works. Now make it useful. In this phase you'll give it a purpose, load it with context, experiment with voices, and tune its behavior.

## Give it context and purpose

The `instructions` in your `Agent` class are a system prompt  - they shape everything about how the agent behaves. A generic "helpful assistant" is functional but forgettable. A purpose-built agent with real context is genuinely useful.

Think about a real scenario: a customer calls a business. What do they usually ask? What information does the agent need to answer well?

The system prompt is where you front-load that knowledge  - FAQs, product details, policies, tone guidelines. This is the cheapest way to make your agent smart about a specific domain, without needing tool calls or RAG.

<details>
<summary>Example: a gym front desk agent</summary>

```python
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are the voice assistant for FitSpace gym.
            You help members and prospective members with common questions.

            Key information:
            - Hours: Mon-Fri 6am-10pm, Sat-Sun 8am-8pm
            - Membership: £40/month, no contract. Student discount £30/month
            - Free trial: 3-day pass available, just need an email address
            - Classes: yoga (Tue/Thu 7pm), spin (Mon/Wed/Fri 6:30am), HIIT (daily 12pm)
            - Cancellation: cancel anytime, 30 days notice, email cancel@fitspace.com
            - Parking: free for members, 2-hour limit for guests

            Tone: friendly, efficient, helpful. Don't oversell  - just answer honestly.
            Keep responses to 2-3 sentences. If you don't know something, say so and
            suggest they call the front desk at 020 7946 0958.""",
        )
```

</details>

<details>
<summary>Example: a property management agent</summary>

```python
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are the after-hours voice agent for Oakwood Properties.
            You handle tenant inquiries when the office is closed.

            Common issues and responses:
            - Emergency repairs (burst pipe, no heating, gas smell): "For emergencies,
              call our 24-hour maintenance line at 0800 555 0199"
            - Rent payments: due on the 1st, pay via bank transfer to the details in
              your tenancy agreement, or through the tenant portal at portal.oakwood.co.uk
            - Noise complaints: log them at portal.oakwood.co.uk/report, include date,
              time, and flat number. The team reviews these within 48 hours
            - Viewing requests: take their name, email, and preferred dates. Let them
              know someone will follow up within one business day
            - Anything else: take a message with their name, flat number, and issue.
              The office reopens at 9am Monday-Friday

            Be calm, professional, and empathetic. Keep it brief.""",
        )
```

</details>

## Change the voice

The TTS model determines what your agent sounds like. Different providers offer different voices with different qualities.

In your `AgentSession`, the `tts` parameter controls this. Try swapping providers or voices:

```python
# OpenAI TTS voices
tts=openai.TTS(voice="coral")    # warm, conversational
tts=openai.TTS(voice="onyx")     # deep, authoritative
tts=openai.TTS(voice="shimmer")  # clear, expressive
tts=openai.TTS(voice="nova")     # friendly, versatile
```

The voice should match the purpose. A professional property agent probably shouldn't sound like a bubbly podcast host.

<details>
<summary>Go deeper: Voice cloning and speaker embeddings</summary>

Some TTS providers (like ElevenLabs) support **voice cloning**  - you provide a short audio sample of a target voice, and the model extracts a **speaker embedding**: a vector that captures the unique characteristics of that voice (timbre, pitch range, resonance, rhythm).

The TTS model then generates new speech that sounds like that person. This enables brand-consistent voices, personalized agents, or character voices, but raises real ethical questions around consent and deepfakes.

</details>

## Tune the behavior

Beyond the persona, you can adjust how the agent interacts:

### Initial greeting

The `generate_reply` call at the end of your session handler controls what the agent says first:

```python
await session.generate_reply(
    instructions="Greet the caller, tell them they've reached FitSpace gym, and ask how you can help."
)
```

### Response style

Experiment with your instructions to control:
- **Length**  - "Keep responses to one or two sentences" vs. "Provide detailed explanations"
- **Questioning**  - "Always ask a follow-up question" vs. "Only answer what was asked"
- **Tone**  - "Be formal and professional" vs. "Be casual and friendly"
- **Scope**  - "Only discuss gym-related topics" vs. "Help with anything"
- **Escalation**  - "If someone is angry, acknowledge their frustration and offer to take a message for a manager"

## Try it

1. Pick a real scenario  - a business, a service, a use case
2. Load your system prompt with the context that agent would need
3. Pick a voice that fits
4. Customize the greeting
5. Run `python agent.py dev` and try to break it  - ask questions it should handle, and questions it shouldn't

## Checkpoint

You should now have a voice agent that knows things  - not because it's calling APIs, but because you gave it the right context upfront. This is the simplest and most reliable way to make a domain-specific agent.

When you're ready, move on to **[Phase 3: Add tool calling](phase-3.md)**  - where the agent starts doing things it *can't* just know from a system prompt.
