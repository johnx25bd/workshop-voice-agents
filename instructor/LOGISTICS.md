# Logistics

## Pre-workshop

### Attendee list
- [ ] Get attendee list — how many students, what cohort, skill levels
- [ ] Confirm room and AV setup (projector, screen sharing, speakers for demo)
- [ ] Test WiFi — WebRTC needs decent connectivity

### API keys
- [ ] Confirm who is providing OpenAI keys
- [ ] Decide on STT provider — Deepgram (needs separate key) or OpenAI Whisper API (same OpenAI key). LiveKit orchestrates the pipeline but doesn't provide AI models — you need keys for each provider. Using OpenAI for STT + LLM + TTS means one key covers everything
- [ ] Provision keys: one per student? One shared key? Shared is simpler but harder to track usage
- [ ] Distribute keys: handed out on paper? Shared doc? Pinned on Discord?
- [ ] Set usage limits / spending caps on all keys
- [ ] Plan for sunsetting keys after workshop (rotate or revoke within 24 hours)

### LiveKit Cloud
- [ ] Students have been directed to sign up for free tier individually 

### Student pre-requirements

Send comms at least 24 hours before:
- Python 3.9+ installed
- git installed
- A code editor
- Microphone and headphones (earbuds work — speakers cause echo/feedback)
- A browser (Chrome recommended for WebRTC)

### Environment setup

Students clone the repo and set up a local Python environment. The repo includes a setup script and clear instructions.

```
git clone https://github.com/johnx25bd/workshop-voice-agents.git
cd workshop-voice-agents
uv sync
cp .env.example .env
# fill in API keys
```

Or with venv and pip:
```
git clone https://github.com/johnx25bd/workshop-voice-agents.git
cd workshop-voice-agents
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill in API keys
```

These are experienced developers — standard Python setup should be sufficient. The repo README covers any OS-specific notes (Windows venv activation differs, etc.).

### Recording
- [ ] Confirm: is someone recording? Who handles the setup?
- [ ] If instructor is responsible: test recording setup beforehand. What should be recorded?

### Check-in
- [ ] Create QR code for check-in (Google Form or simple attendance sheet)
- [ ] Print or display QR code at entrance or on welcome slide

### Feedback
- [ ] Create feedback form (keep it short, 5 questions max)
- [ ] Create QR code for feedback form for closing slide
- [ ] Display during wrap-up

## Day-of checklist

### Before the workshop
- [ ] Test all API keys work
- [ ] Test the demo voice agent end-to-end
- [ ] Test the `phase-1` solution branch works from a clean clone
- [ ] Charge laptop, have charger ready, tidy up desktop + apps
- [ ] Print/prepare QR codes (check-in + feedback)

### 30 min before
- [ ] Arrive, set up projector/screen
- [ ] Run the demo voice agent, verify it's working
- [ ] Have the repo URL ready to share (on a slide, on the board, or printed)
- [ ] Have backup API keys accessible

### During
- [ ] QR check-in as people arrive
- [ ] Walk the room during build phases — don't sit at the front
- [ ] Host breakout lesson; invite students to present to the next group
- [ ] Set timer for check-in intervals (see PLAN.md)
- [ ] Note which students seem engaged for post-workshop debrief

### After
- [ ] Revoke or rotate API keys
- [ ] Review feedback form responses
- [ ] Debrief with observer (see PLAN.md for discussion questions)
- [ ] Note what to change for next time
- [ ] Follow ups etc
