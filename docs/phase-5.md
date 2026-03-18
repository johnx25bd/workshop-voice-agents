# Phase 5: Telephony (stretch goal)

Your agent lives in the browser. In this phase, you'll connect it to a phone number so anyone can call it.

This is a stretch goal  - it requires a Twilio account and some additional setup. If you don't get to it during the workshop, the instructions here are self-contained enough to try later.

## How it works

LiveKit supports SIP (Session Initiation Protocol), the standard protocol for internet telephony. The flow:

1. Someone dials a phone number
2. **Twilio** receives the call and forwards it to LiveKit via SIP
3. **LiveKit** creates a room and routes the audio to your agent
4. Your agent handles the call exactly as it handles a browser session  - same code, same pipeline

Your agent code barely changes. The main work is configuring the Twilio → LiveKit connection.

## Prerequisites

- A [Twilio account](https://www.twilio.com/try-twilio) (free trial works)
- A Twilio phone number with voice capability
- Your LiveKit Cloud project's SIP URI

## Setup

### 1. Configure LiveKit SIP

In your LiveKit Cloud dashboard, enable SIP and note your SIP URI. It will look something like:

```
sip:your-project@sip.livekit.cloud
```

### 2. Configure Twilio

In your Twilio console:

1. Go to your phone number's configuration
2. Under "Voice," set "A call comes in" to **SIP**
3. Set the SIP URI to your LiveKit SIP address
4. Configure authentication if required

### 3. Update your agent for telephony

Your agent code needs minimal changes. The main addition is handling the SIP participant type for noise cancellation:

```python
from livekit import rtc
from livekit.plugins import noise_cancellation

await session.start(
    room=ctx.room,
    agent=Assistant(),
    room_options=room_io.RoomOptions(
        audio_input=room_io.AudioInputOptions(
            noise_cancellation=lambda params:
                noise_cancellation.BVCTelephony()
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                else noise_cancellation.BVC(),
        ),
    ),
)
```

This uses telephony-optimized noise cancellation when the caller is connecting via SIP (phone) and standard noise cancellation for browser connections.

## Test it

1. Start your agent: `uv run python agent.py dev`
2. Call your Twilio phone number
3. Talk to your agent  - over the phone

The same agent handles both browser and phone calls. The difference is just the audio transport layer.

<details>
<summary>Go deeper: SIP and telephony concepts</summary>

**SIP** (Session Initiation Protocol) is the standard protocol for establishing voice calls over the internet. It handles call setup, teardown, and routing  - but not the actual audio. The audio travels over **RTP** (Real-time Transport Protocol).

**Twilio** acts as a bridge between the traditional phone network (PSTN) and SIP. When someone dials a phone number, Twilio receives the call from the phone network and can forward it to any SIP endpoint  - in this case, LiveKit.

**LiveKit SIP** is LiveKit's native SIP gateway. It receives incoming SIP calls and creates a room for each one, making the caller a participant just like a browser user. Your agent joins the same room and the conversation works identically.

This is what makes the voice agent code portable  - the agent doesn't know or care whether the user is in a browser or on a phone. LiveKit abstracts the transport.

</details>

## Resources

- [LiveKit SIP docs](https://docs.livekit.io/sip/)
- [Twilio SIP trunking guide](https://www.twilio.com/docs/sip-trunking)
- [LiveKit SIP agent example](https://github.com/livekit-examples/livekit-sip-agent-example)
