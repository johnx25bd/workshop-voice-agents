# Workshop execution plan

## Voice Agents

### Overview

A 4-hour workshop that takes students from understanding voice agent architecture to building a working voice agent in their browser. Cascaded pipeline first, then optionally swap to a realtime model.

### Timeline

Use relative offsets from workshop start. Adapt to your actual schedule.

| Offset | Duration | What |
|---|---|---|
| +0:00 | 15 min | Arrival, check-in (QR code), settle in |
| +0:15 | 5 min | **Demo**: talk to the finished voice agent. No explanation yet — just show it. |
| +0:20 | 25 min | **Lecture**: voice agents, architectures, hard problems (from NOTES.md) |
| +0:45 | 10 min | **Discussion**: evaluation, architecture tradeoffs, questions |
| +0:55 | 10 min | **LiveKit intro**: what it is, how it works, the plugin system |
| +1:05 | 10 min | **Setup**: clone repo, install dependencies, configure env. Troubleshoot stragglers |
| +1:15 | 45 min | **Phase 1**: build the basic cascaded voice agent. Solo or pairs, their choice |
| +2:00 | 10 min | **Check-in**: where is everyone? Quick show of hands. Help anyone stuck. Brief phase 1 recap |
| +2:10 | 30 min | **Phase 2**: customize persona, swap voices, tweak settings |
| +2:40 | 10 min | **Check-in**: progress update, introduce phase 3-4 as "Go Deeper" options |
| +2:50 | 25 min | **Phase 3/4**: choose your own adventure — add tool calls OR swap to realtime model |
| +3:15 | 15 min | **Wrap-up**: what did we build? Architecture recap now that they've felt it. Where this goes next (telephony, open models, fine-tuning) |
| +3:30 | 15 min | **Q&A, feedback** (QR code to feedback form), informal chat |
| +3:45 | | End |

### Pacing notes

- The lecture + discussion block must stay sharp. 25 min lecture, not 40. If questions are flowing during discussion, let it run a couple minutes into the LiveKit intro slot
- Setup is the highest-risk slot. Have fast students help stragglers. Do NOT let this run more than 15 minutes
- Phase 1 is the critical phase. Everyone should get a working voice agent. Walk the room during this time
- Check-ins are soft boundaries, not hard stops. Set a timer, give a 2-minute warning, but don't cut someone off who's about to get it working
- Phases 3-4 are stretch goals. It's fine if most people don't reach them. The win is phase 1 + phase 2
- The wrap-up should feel earned, not rushed
- Plan for 3.5 hours of content in a 4-hour slot. Something will go wrong or run long

### Demo plan

Have the finished voice agent (phase 2 or 3 version) running and ready before anyone arrives. Test it 30 minutes before the workshop. Have a backup plan if it fails (screen recording of it working).

### Collaboration style

- Invite people to work however they're comfortable — solo, pairs, small groups
- Don't force pairing. Some people learn better solo
- Encourage people to check in with neighbors if stuck
- Periodic check-ins at phase boundaries create natural moments for people to compare notes and share what they've learned

### Contingencies

- **WiFi issues**: have the demo as a screen recording backup. Phase 1 code can still be walked through conceptually
- **API keys not working**: have backup keys ready. Test all keys beforehand
- **Students way ahead**: phase 5 (Twilio telephony) exists as an additional challenge
- **Students way behind**: the solution branches exist. Nobody gets permanently stuck — they checkout the branch and learn from reading working code
- **LiveKit Cloud down**: instructions for running LiveKit locally (Docker) exist as a Go Deeper callout

### Post-workshop debrief

Questions to discuss with your observer/co-instructor:
- How did the pacing feel? Too fast, too slow, about right?
- Did the lecture land? Were the architecture concepts clear before they started building?
- How was the skill distribution? Did the phased approach work for different levels?
- Did the demo at the start set the right tone?
- What would you change for next time?
- Student feedback form results — any patterns?
- Specific students who seemed particularly engaged or who struggled?
