# Learning objectives

## By the end of this workshop, students should be able to:

### Core (everyone)
1. Explain the two dominant voice agent architectures (cascaded vs speech-to-speech) and articulate the tradeoffs between them
2. Describe the role of each component in a cascaded pipeline (VAD → STT → LLM → TTS)
3. Identify the hard problems in voice AI (latency, endpointing, turn-taking, prosody)
4. Build and run a working voice agent using LiveKit Agents
5. Customize a voice agent's behavior through system prompts and configuration

### Stretch (fast movers)
6. Add tool-calling capabilities to a voice agent
7. Swap a cascaded pipeline for a realtime/multimodal model and compare the experience
8. Connect a voice agent to telephony (Twilio)

### Conceptual (from the lecture)
- Understand what a spectrogram is and why it matters for audio ML
- Know what VAD does and why Silero is the standard
- Understand endpointing and why it's a hard tradeoff
- Have a mental model for how audio tokenization works in S2S models (neural codecs, without needing to understand RVQ details)
- Know the current model landscape: Whisper, Deepgram, Cartesia, Kokoro, OpenAI Realtime, Moshi, Ultravox
