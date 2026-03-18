# Presentation speaker notes

Ordered to match slides. Key terms in **bold**, definitions inline.

---

### 1. Title
Voice Agents / Founders and Coders / Check-in QR / Discord link

### 2. Demo
Live demo of a voice agent. Have a short conversation prepared.
- How does a neural network work?
- Can you tell what I mean when I say "Sounds interesting"?
After: "How natural did that feel? Why or why not?"

### 3. How did that work?
Arrow → ? → Arrow. "What goes in the box?"

### 4. Motivation
- Language makes us human. Speech is ~100,000 years old, writing ~5,000
- Speech as an enabling technology - we evolved to listen and speak
- Voice unlocks: more inclusive UIs, wider contexts (hands-free, eyes-free), natural interaction

### 5. Design goals
What do we want from a voice agent system?
- **Natural UX** - feels like talking to a person, not a machine
- **Quality responses** - accurate, relevant, well-reasoned
- **Efficient, reliable, debuggable** - works in production, not just demos

### 6. The cascaded pipeline - ?
Arrow → [?] → Arrow. "Let's open the box."

### 7. The cascaded pipeline - three components
Arrow → [STT] → [LLM] → [TTS] → Arrow. Reveal labels one at a time. "Three models, each specialized."

### 8. Speech-to-Text (STT)
Pipeline with STT highlighted. Waveform → MODEL → "Hello, how are you?"

Key terms:
- **STT / ASR** - Speech-to-Text / Automatic Speech Recognition. Converts audio to text
- **Transcription** - the text output of STT
- **Streaming STT** - emits partial transcripts that refine as more audio arrives ("hel..." → "hello" → "hello, how are you")
- **Endpointing** - deciding when the user has finished speaking. Usually a silence threshold (500-800ms). The gate between listening and responding
- **Word Error Rate (WER)** - % of words transcribed incorrectly. Key STT quality metric

### 9. What is a spectrogram?
Waveform (amplitude over time) alongside a spectrogram (time x frequency, energy as color).

Key terms:
- **Digital audio** - a sequence of amplitude samples at a fixed rate (16,000/sec for speech). Each sample is air pressure at that instant. A one-dimensional sequence of values
- **Waveform** - amplitude over time. All frequencies are mixed together in one signal. Amplitude = how loud (size of the peaks). Frequency = how fast it oscillates (tight zigzags = high pitch, wide bumps = low pitch). Real speech is many frequencies stacked on top of each other, so the raw waveform is hard to interpret by eye
- **Fourier transform** - the math that unstacks a waveform into its component frequencies. Takes a window of samples and says "this contains X amount of 200Hz, Y amount of 500Hz, Z amount of 1000Hz..."
- **Spectrogram** - the result of running Fourier transforms across the whole waveform. X-axis is time, y-axis is frequency, brightness is energy/intensity. Essentially an image. ML models work well on spectrograms because spatial patterns (formants, energy bursts) suit CNNs and transformers
- **Mel spectrogram** - spectrogram with frequency axis warped to match human hearing perception

### 10. Large Language Model (LLM)
Pipeline with LLM highlighted. "Hello, how are you?" → MODEL → "I'm doing well, thanks for asking!"

Key terms:
- **LLM** - Large Language Model. Text in, text out. Reasoning, knowledge, personality
- **System prompt** - instructions that define agent behavior, persona, scope
- **Tool calling / function calling** - LLM decides to invoke a function instead of generating text directly
- **TTFT (Time to First Token)** - how quickly the LLM starts producing output. In voice, this matters more than total generation time because TTS can start as soon as the first tokens arrive
- **Streaming LLM** - tokens output one at a time, fed to TTS incrementally

### 11. Text-to-Speech (TTS)
Pipeline with TTS highlighted. "I'm doing well, thanks for asking!" → MODEL → waveform

Key terms:
- **TTS** - Text-to-Speech. Converts text to spoken audio
- **Voice synthesis** - generating speech audio from text
- **Prosody generation** - the TTS model decides intonation, stress, pacing for the generated speech
- **Voice selection** - choosing which voice the agent uses. Different voices have different characters
- **Voice cloning** - providing an audio sample to clone a specific voice. Uses **speaker embeddings** (a vector capturing timbre, pitch, rhythm)
- **Streaming TTS** - starts generating audio from the first tokens, before the full text exists
- **Mean Opinion Score (MOS)** - human judges rate naturalness 1-5. Key TTS quality metric

### 12. Naive architecture
Pipeline with speaking head icon. "This works. But there are problems."

### 13. Challenge: inference is expensive
Same pipeline, red "Inference is expensive!" banner. "We're sending everything from the microphone through expensive models. Silence, coughs, background noise."

### 14. Voice Activity Detection - pipeline
VAD added to the pipeline (smaller box). "Inference is expensive" banner still visible. "A tiny filter at the front."

### 15. Voice Activity Detection - detail
VAD with input filtering visual (red X for noise, green check for speech).

Key terms:
- **VAD** - Voice Activity Detection. Determines if audio contains human speech
- **Silero VAD** - industry standard. Tiny CNN (<1MB), runs on CPU, faster than real-time. Looks at spectrograms
- **CNN (Convolutional Neural Network)** - slides learned filters across input (images, spectrograms) to detect spatial patterns
- Speech detection + noise filtering

### 16. Turn Detection - intro
"How can we tell when someone is finished speaking?" Pipeline with gate/barrier between STT and LLM.

### 17. Turn Detection - question mark
Same slide with "?" at the gate. VAD and STT both feed signals (asterisk markers) into the turn detector.

### 18. Turn Detection - with asterisks
Asterisks on VAD and STT showing both contribute signals. Turn Detection box appears below.

Key terms:
- **Turn detection** - deciding when it's the agent's turn to respond. Cross-cutting concern that draws from multiple signals
- **Endpointing** - the specific decision that the user is done. Silence threshold (500-800ms) + linguistic cues
- VAD answers "is someone talking?" Turn detection answers "are they done?" Different questions
- **Half-duplex** - one direction at a time (cascaded agents). **Full-duplex** - both simultaneously (some S2S models like Moshi)
- Humans use eye contact, body language, grammar, social context. Current systems mostly count silence milliseconds

### 19. Latency budget
Horizontal bar: VAD ~10ms | STT ~300ms | LLM ~300ms | TTS ~150ms | Net ~75ms = ~800ms total

Key terms:
- **Latency** - time from user stops speaking to agent starts speaking
- Natural conversation gaps average ~200ms. Over 500ms feels slow. Over 1s feels broken
- **Streaming** - each stage feeds the next incrementally. Output-side only. The input is gated by endpointing (full transcript goes to LLM). But LLM tokens stream to TTS, and TTS audio streams to the speaker. Without streaming this would be 2-3 seconds

### 20. Prosody - "Another thing..."
Same text said angrily vs happily → both go through STT → identical transcript.

Key terms:
- **Prosody** - patterns of stress, intonation, pace, phrasing, pauses in speech. Non-linguistic information that modifies meaning
- Lost at the audio → text boundary in cascaded systems. TTS reinvents new prosody from scratch
- "That's great" said sarcastically vs sincerely. Same transcript. Different meaning

### 21. Emotional prosody - definition
Blue callout box. "The patterns of stress and intonation in language - tone, stress, pace, phrasing, pauses."

### 22. Speech-to-Speech pipeline - collapsing
The three cascaded boxes (STT, LLM, TTS) merge into one. "What if one model did it all?"

### 23. S2S with responsibilities
Single S2S Model box with all the responsibilities listed below: speech detection, noise filtering, transcription, endpointing, streaming, world knowledge, reasoning, personality, tool calling, safety, voice synthesis, prosody, voice selection, streaming.

"One model has to do everything the cascaded pipeline spread across four specialized components."

### 24. Cascaded vs Speech-to-Speech
Traffic light comparison table (green/yellow/red dots):
- Latency: Cascaded red, S2S yellow
- Prosody: Cascaded red, S2S green
- Debuggability: Cascaded green, S2S red
- Tool calling: Cascaded green, S2S yellow
- Modularity: Cascaded green, S2S red
- Maturity: Cascaded green, S2S yellow

### 25. Use cases
Slider visual showing which architecture fits:
- Therapy/coaching → S2S
- High-volume support → Cascaded
- Regulated industries → Cascaded
- Collaborative brainstorming → either, leaning S2S
- Tool-heavy workflows → Cascaded
- Multilingual → either, leaning S2S

### 26. Landscape
Provider grid:
- **STT**: Whisper, Deepgram, AssemblyAI
- **LLM**: OpenAI, Anthropic, Meta, Google
- **TTS**: Cartesia, ElevenLabs, Kokoro, OpenAI
- **S2S**: OpenAI Realtime, Gemini Live, Moshi, Ultravox
- **Framework**: LiveKit Agents, Pipecat, Vocode
- **Telephony**: Twilio, LiveKit SIP

### 27. LiveKit
- Open-source WebRTC infrastructure
- Handles real-time audio/video between participants
- Handles the "plumbing" for voice agent systems

Key terms:
- **WebRTC** - Web Real-Time Communication. Browser-native protocol for real-time audio/video. Same tech as Google Meet, Discord
- **SFU (Selective Forwarding Unit)** - server that receives audio streams and forwards them to other participants. Audio goes through the server, not peer-to-peer

### 28. LiveKit Architecture
Client ↔ LiveKit Cloud ↔ Agent
- Client: mic/speakers, WebRTC, browser/app
- LiveKit Cloud: audio routing, "room" management, LK or self-hosted
- Agent: Python process, runs inference, hosted wherever

Audio path: browser → LiveKit Cloud → agent → OpenAI (STT) → agent → OpenAI (LLM) → agent → OpenAI (TTS) → agent → LiveKit Cloud → browser

### 29. LiveKit Agents Framework
Code snippet showing AgentSession config:
```
AgentSession(
    stt=openai.STT(model="gpt-4o-transcribe"),
    llm="openai/gpt-4.1-mini",
    tts=openai.TTS(voice="coral"),
    vad=silero.VAD.load()
)
```
"You configure which model goes in each slot. LiveKit handles the streaming, audio routing, WebRTC. You just pick your components."

### 30. Build
Repo URL, phase timing, QR codes, Discord link.
- Setup + Phase 1: ~45min
- Phase 2: ~30min
- Check-in
- Phase 3/4: Choose your own adventure
- Q+A: 15min
