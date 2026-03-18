# Phase 5: Telephony (stretch goal)

Your agent lives in the browser. But voice agents become a lot more useful when people can call them on a phone number.

This is a stretch goal. It requires additional accounts and configuration, and we haven't tested every path here. If you don't get to it during the workshop, this page has enough pointers to try it on your own time.

## How it works

Your agent code doesn't change much. The key insight is that LiveKit abstracts the audio transport. Whether the user connects from a browser or a phone call, the agent joins the same kind of room and handles audio the same way.

The phone-to-agent flow:

1. Someone dials a phone number
2. A telephony provider (Twilio, or LiveKit's native SIP support) receives the call and forwards it to LiveKit
3. LiveKit creates a room and routes the audio to your agent
4. Your agent handles the call the same way it handles a browser session

## Options

**LiveKit SIP** - LiveKit has built-in SIP support. You configure a SIP trunk in your LiveKit Cloud dashboard and incoming calls get routed directly to your agent. This keeps everything in one platform. See the [LiveKit SIP docs](https://docs.livekit.io/sip/).

**Twilio** - If you already have a Twilio account with phone numbers, you can configure Twilio to forward calls to LiveKit via SIP. Twilio acts as a bridge between the traditional phone network and LiveKit. See the [Twilio SIP trunking guide](https://www.twilio.com/docs/sip-trunking).

Either way, the idea is the same: get a phone call into a LiveKit room, and your agent handles it from there.

## Things to think about

- Phone audio is lower quality than browser audio (narrowband vs wideband). Your agent may need telephony-optimized noise cancellation
- Latency matters more on a phone call. People expect phone conversations to feel immediate
- There's no visual UI on a phone. Everything has to work through voice alone - no fallback to a text chat or a button

## Resources

- [LiveKit SIP docs](https://docs.livekit.io/sip/)
- [LiveKit SIP agent example](https://github.com/livekit-examples/livekit-sip-agent-example)
- [Twilio SIP trunking guide](https://www.twilio.com/docs/sip-trunking)
