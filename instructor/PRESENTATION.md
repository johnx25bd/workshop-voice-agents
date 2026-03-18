# Presentation outline

## Slide deck structure

~25 min lecture + 10 min discussion. Iterative structure — build the naive pipeline, then introduce problems and solutions.

Slides should be visual-first: one idea per slide, big images or diagrams, minimal text.

---

### 0. Demo (1 min)

Show the demo of a voice agent, talk to it, ask some questions, notice some things. 
- How natural did that feel? 
- Why?

### 1. The question (2 min)

**Slide**: Photo of a speaking mouth (left) → big empty box with "?" (center) → photo of a human ear (right)

"You just saw the demo. You talked, it listened, it thought, it spoke back. How did that work? What goes in the box?"

---

### 2. Why this matters (2 min)

**Slide**: Simple visual — something evocative about voice as our primary communication medium

- We evolved to communicate through sound. Written language is recent
- Voice interaction unlocks inclusion (not everyone reads/writes well), new contexts (hands-free, eyes-free), more natural UX
- The motivating challenge: how do we build software that listens and speaks?

Keep this brief. Set the stage, move on.

---

### 3. Build the pipeline (10 min)

This is the core of the talk. Start simple, add complexity by introducing problems. Each component gets its own slide — these are the key concepts people need to understand.

#### Slide: What is digital audio?

**Visual**: Waveform — a squiggly line of amplitude over time

"Before we can process speech, we need to understand what we're working with. Digital audio is just a list of numbers — amplitude samples captured thousands of times per second. 16,000 samples per second is typical for speech. Each number represents air pressure at that instant."

"A WAV file is literally just this list of numbers with a header."

#### Slide: What is a spectrogram?

**Visual**: Side by side — raw waveform (top) and its spectrogram (bottom). Speech patterns clearly visible

"If we convert those samples to a time × frequency representation, we get a spectrogram. It's essentially an image — time on the x-axis, frequency on the y-axis, brightness is energy. This is what many ML models actually work with. You can *see* speech patterns in it."

#### Slide: The naive pipeline

**Visual**: Mouth → [STT] → [LLM] → [TTS] → Ear

"The simplest idea. Three steps. Convert speech to text. Think about it. Convert the response back to speech."

#### Slide: Speech-to-Text (STT)

**Visual**: Waveform going in, text coming out. Highlight STT in the pipeline diagram

"The first model takes audio and produces a transcript. It's analyzing spectrograms — looking for patterns that correspond to phonemes, words, sentences."

- Listens to audio, outputs text
- Streaming: emits partial transcripts that refine in real time ("hel..." → "hello" → "hello, how are...")
- Key providers: Whisper (open weight, the workhorse), Deepgram (fast, commercial)
- Measured by Word Error Rate (WER) — what percentage of words are wrong?

#### Slide: Large Language Model (LLM)

**Visual**: Text in, text out. Highlight LLM in the pipeline diagram

"You know this one. Same models you use for text chat — GPT-4, Claude, Llama. Takes the transcript, generates a response."

- Text in, text out — reasoning, knowledge, personality
- System prompt defines behavior (just like a chatbot)
- Can call tools / functions
- In voice context, **time to first token (TTFT)** matters more than total generation time — because TTS can start as soon as the first tokens arrive
- Streaming: tokens come out one at a time

#### Slide: Text-to-Speech (TTS)

**Visual**: Text in, waveform coming out. Highlight TTS in the pipeline diagram

"The final step. Takes the LLM's text response and generates spoken audio."

- Text in, audio out
- Streaming: starts generating audio from the first few tokens, before the full response exists
- Different voices available — each with distinct character
- Key providers: Cartesia (low latency), ElevenLabs (high quality, voice cloning), Kokoro (open weight)
- Measured by Mean Opinion Score (MOS) — human judges rate naturalness 1-5
- Design question: what should the agent *sound like*? Voice selection matters

"This pipeline works. You heard it in the demo. But there are problems."

#### Problem: wasted compute

**Visual**: Same pipeline diagram, but the arrow from Mouth is labeled "silence... cough... background noise... someone else talking... actual speech (finally)"

"We're running expensive inference on every millisecond of audio coming from the microphone. Most of it isn't even speech."

#### Slide: Voice Activity Detection (VAD)

**Visual**: Mouth → **[VAD]** → [STT] → [LLM] → [TTS] → Ear. VAD highlighted as new addition

"Solution: a tiny, cheap filter at the front. One job: 'Is someone talking right now?' If yes, pass the audio through. If no, throw it away."

- Detects whether audio contains human speech
- Silero VAD is the industry standard: a small CNN (< 1MB), runs on CPU, processes audio faster than real-time
- It works on spectrograms — since a spectrogram is like an image, a convolutional neural network slides learned filters across it, detecting patterns that look like human speech vs noise
- Output: a probability between 0 and 1. Above a threshold → speech detected
- Costs almost nothing. Runs continuously. This is why it goes first

#### Problem: when is the user done?

**Visual**: Transcript appearing word by word... "I want to book a flight to..." [long pause — 600ms] "...Paris"

"When do we send the transcript to the LLM? How do we know the user has finished their thought?"

#### Slide: Endpointing

**Visual**: Same pipeline, highlight the boundary between STT and LLM. A "gate" icon or barrier

"Endpointing: the decision that the user is done talking. This is the gate between listening and responding."

- Usually a silence duration threshold — 500-800ms of quiet after speech
- Sometimes supplemented with linguistic cues (did the sentence end grammatically?)
- The fundamental tradeoff: too short → you cut people off mid-thought. Too long → the agent feels sluggish
- This is genuinely hard. Humans use eye contact, body language, grammar, social context, shared knowledge. Current systems mostly count milliseconds of silence

#### Problem: latency

**Visual**: Horizontal waterfall / bar chart showing where time goes:

```
VAD (~10ms) | STT (~300ms) | LLM TTFT (~300ms) | TTS (~150ms) | Network (~75ms)
                                                          Total: ~800ms
```

"Every step adds time. Research shows natural turn gaps in conversation average ~200ms. We're at 800ms if we're lucky. Over 1 second and it feels broken."

"But here's the key insight: this is a **streaming** pipeline. TTS starts generating audio from the LLM's first tokens, before the full response exists. Each stage feeds into the next in real time. Without streaming, this would be 2-3 seconds. Streaming is what makes this usable."

#### Problem: what gets lost?

**Visual**: Two audio waveforms that look different but produce the same transcript. Or: the text "That's great" with two arrows pointing to it — one from a happy face, one from an angry face

"Try it: say 'That's great' sarcastically. Now say it sincerely. Transcribe both — identical text. But the meaning is completely different."

"This is **prosody** — stress, intonation, pacing, emphasis. When we convert audio to text, we throw all of this away. When TTS converts text back to audio, it invents new prosody from scratch. The emotional signal that was in the user's voice is gone."

#### Slide: The full cascaded pipeline

**Visual**: Complete pipeline diagram with responsibilities listed under each component:

```
[VAD]              [STT]               [LLM]                  [TTS]
- Speech detection - Transcription     - World knowledge      - Voice synthesis
- Noise filtering  - Endpointing       - Reasoning            - Prosody generation
                   - Streaming         - Personality/persona   - Voice selection
                                       - Tool calling          - Streaming
                                       - Safety & alignment
```

"Each component is specialized. This is powerful — you can use the best model for each job, swap them independently, inspect the text at every boundary, filter content, log everything. But the boundaries are lossy. And every boundary adds latency."

"This is the architecture you'll build first in the tutorial."

---

### 4. What if one model did it all? (5 min)

**Slide**: Same mouth/ear diagram, but the middle is ONE box labeled "Speech-to-Speech Model"

"What if we removed the text stage entirely? Audio in, audio out. One model."

**Slide**: The responsibilities list — everything that model has to encode:

- World knowledge (like a text LLM)
- Speech understanding (like STT)
- Speech generation (like TTS)
- Voice activity detection
- Turn-taking and interruption
- Emotional prosody — interpretation AND generation

"This is why these models are enormous and hard to build. They're doing everything at once."

**Slide**: Side-by-side comparison

| | Cascaded | Speech-to-speech |
|---|---|---|
| Latency | Higher (multiple steps) | Lower (one step) |
| Prosody | Lost at text boundary | Preserved end-to-end |
| Debuggability | High (inspect text) | Low (black box) |
| Tool calling | Natural (text-based) | Tricky (no text stage) |
| Modularity | Swap any component | All or nothing |
| Maturity | Production-proven | Frontier |

**Slide**: Mental model

"**Cascaded = Unix philosophy.** Small tools, piped together. Lossy at the seams, but modular and debuggable."

"**Speech-to-speech = one model that natively speaks.** Preserves everything, but you give up control."

**Slide**: The choosing-an-architecture table (from NOTES.md). Quick — spend 30 seconds, don't read every row.

---

### 5. The landscape (3 min)

**Slide**: A grid or logo cloud of the key players. Don't explain each — just name and category.

| Role | Options |
|---|---|
| STT | Whisper (open), Deepgram, AssemblyAI |
| LLM | GPT-4o, Claude, Llama, Gemini |
| TTS | Cartesia, ElevenLabs, Kokoro (open), OpenAI TTS |
| S2S | OpenAI Realtime, Gemini Live, Moshi (open), Ultravox (open) |
| Orchestration | LiveKit Agents, Pipecat, Vocode |
| Telephony | Twilio, LiveKit SIP |

"Open weight options exist for every component. This matters for cost, privacy, and customization."

---

### 6. What we're building (3 min)

**Slide**: LiveKit architecture diagram — browser ↔ LiveKit Cloud ↔ your agent

"LiveKit handles the real-time audio connection. Your agent is a Python process that joins a 'room' — like joining a video call. LiveKit routes audio between you and the user."

**Slide**: The phases

1. Build a basic cascaded voice agent
2. Give it a persona and pick a voice
3. Add tool calling — make it do things
4. Swap to a realtime model — feel the difference
5. (Stretch) Connect it to a phone number

"You'll experience both architectures firsthand. By the end, you'll have a felt sense of the tradeoffs, not just a theoretical understanding."

**Slide**: Setup instructions — repo URL, setup commands. Keep this on screen while people clone and install.

---

### 7. Discussion (10 min)

**Slide**: "How would you evaluate a voice agent?"

Open question — let the room generate ideas before showing any framework. They'll come up with good stuff: latency, accuracy, naturalness, task completion. Then you can add dimensions they missed.

Follow-up discussion prompts:
- "If you were building a voice agent for [specific use case], which architecture would you pick? Why?"
- "What's the hardest problem to solve here?"
- Open Q&A

---

## Slide design notes

- **Visual-first**: every slide should have an image, diagram, or visualization as the primary element. Text supports the visual, not the other way around
- **One idea per slide**: if you're making two points, that's two slides
- **Build-up diagrams**: the pipeline should animate/build — don't show the whole thing at once. Add components one at a time
- **Spectrogram image**: find or generate a clear spectrogram showing visible speech patterns
- **Waveform comparison**: for the prosody slide, two waveforms of the same sentence said differently would be powerful
- **Dark background**: easier on the eyes in a projector setting, and diagrams/images pop more

## Assets needed

- [ ] Photo: speaking mouth (or stylized graphic)
- [ ] Photo: human ear (or stylized graphic)
- [ ] Spectrogram image showing speech
- [ ] Audio waveform comparison (same text, different prosody)
- [ ] LiveKit architecture diagram (browser ↔ cloud ↔ agent)
- [ ] Pipeline diagrams (v1, v2, v3, full cascaded, S2S)
- [ ] Provider logos or grid
- [ ] (v2) Animated pipeline build-up
- [ ] (v3) Manim visualizations of audio → spectrogram, streaming pipeline, latency waterfall
