# Voice agents

An AI voice agent is an autonomous software system that conducts natural, human-like voice conversations using machine learning — speech-to-text, large language models, and text-to-speech.

## Why voice?

Humans evolved to communicate through sound. Written language is a relatively recent invention — our brains are wired for speech in ways they aren't for text. Talking and listening activate different cognitive pathways than reading and writing.

So what happens when we can talk to computers the way we talk to people? The implications are significant: broader inclusion (not everyone reads and writes well, or at all), new contexts where AI becomes useful (hands-free, eyes-free), and more natural interaction patterns that reduce the friction between intent and action.

That's the motivating challenge: we have microphones, computers, and speakers. How do we build software that listens and speaks?

## Key challenges

- **Latency** — conversational response times need to feel natural
- **Cost** — running multiple models per turn adds up at scale
- **Privacy** — voice data is biometric and sensitive
- **Turn-taking** — knowing when the user is done speaking (and when they're just pausing)
- **Interruption handling** — what happens when someone talks over the agent?
- **RAG** — how do you ground responses in real-time data without adding latency?
- **Tool use** — how does the agent take actions in the world?
- **Emotional prosody** — interpreting and preserving tone, stress, and intonation
- **Intelligence** — responses should be well-reasoned, clearly articulated, safe and aligned

### The latency budget

How fast does a voice agent need to respond? Research on conversational dynamics gives us a target: natural turn gaps in human conversation average around 200ms. Gaps over 500ms feel noticeably slow; over 1 second feels broken.

In a cascaded pipeline, every component contributes to the total latency:

| Stage | Typical latency | What's happening |
|---|---|---|
| VAD | ~10ms | Detecting whether the audio contains speech |
| STT | 200-500ms | Transcribing speech to text (includes endpointing wait) |
| LLM (TTFT) | 200-500ms | Time to first token from the language model |
| TTS (first chunk) | 100-200ms | Generating the first audio chunk from text |
| Network round-trips | 50-100ms | Data traveling between services |
| **Total** | **~500-1300ms** | End-to-end, user stops speaking → agent starts speaking |

This is why streaming matters so much — without it, you'd add every stage's full processing time sequentially. With streaming, TTS starts generating audio from the LLM's first tokens while the LLM is still producing more. The pipeline overlaps rather than waiting.

Speech-to-speech models can cut this significantly by eliminating the STT and TTS steps entirely.

## Evaluation

How do you measure whether a voice agent is good? This depends heavily on purpose — a customer service bot and a therapy companion have very different success criteria.

Some useful dimensions ([Coval's evaluation framework](https://www.coval.dev/blog/voice-ai-evaluation-in-2026-the-5-metrics-that-actually-predict-production-success)):
- Transcription accuracy (Word Error Rate)
- Response quality (relevance, accuracy, tone)
- TTS naturalness (Mean Opinion Score from human judges)
- Latency (time to first audio byte)
- Task completion rate

The right evaluation framework is part of the design process — decide what matters before you build.

## Foundational concepts

### Digital audio

Digital audio is a sequence of amplitude samples captured at a fixed rate. CD quality is 44,100 samples/sec; speech processing typically uses 16,000/sec. Each sample is a number representing air pressure at that instant.

- **WAV** — raw samples with a header. No compression, no structure
- **FLAC** — lossless compression. Smaller file, bit-perfect reconstruction (like ZIP for audio)
- **MP3** — lossy compression. Much smaller, but information is permanently discarded

### Spectrograms

A spectrogram converts a sequence of audio samples into a time × frequency matrix — essentially an image where the x-axis is time, y-axis is frequency, and pixel intensity represents energy at that frequency at that moment. This is the representation many ML models work with, because spatial patterns in spectrograms (formant shapes, energy bursts, harmonic structures) are well-suited to convolutional neural networks.

### Streaming

Streaming means processing and delivering data incrementally as it's produced, rather than waiting for the complete result before sending anything. In voice agents, each pipeline stage streams its output to the next as chunks become available.

Each stage's "streaming" means something specific:
- **Streaming STT** — emitting partial transcripts as audio arrives, refining them in real time
- **Streaming LLM** — outputting tokens one at a time rather than generating the full response first
- **Streaming TTS** — starting to produce audio from the first few tokens of text, before the full response exists

This overlapping is what makes sub-second response times possible in a multi-stage pipeline.

### WebRTC

WebRTC (Web Real-Time Communication) is a browser-native protocol for real-time audio and video — the same technology that powers Google Meet and Discord. It handles microphone capture, audio encoding/decoding, network transport, and echo cancellation, all built into the browser with no plugins required. This is what makes "voice agent in the browser" possible. LiveKit is built on top of WebRTC.

## Anatomy of a voice agent

A voice agent is built from several components working together. In a cascaded architecture these are separate models; in speech-to-speech they're collapsed into one. Understanding each component helps you make informed choices about your stack.

### Voice Activity Detection (VAD)

**What it does**: determines whether an audio signal contains human speech. If not, don't process it — processing is expensive and increases the chance of errors. If speech is detected, route the audio to the next stage.

**How it works**: the current standard approach uses convolutional neural networks (CNNs) on spectrograms. Since a spectrogram is essentially an image, CNN filters slide across it detecting learned patterns — one filter might fire on vowel formants, another on plosive consonant bursts, another on the flat profile of silence. Stack a few layers and later ones detect combinations: "that's a human voice, not a door slam." The final output is pooled down to a single vector, passed through a linear layer and sigmoid, producing a probability between 0 and 1.

**The standard**: Silero VAD is the industry default. It's a tiny CNN (< 1MB), runs on CPU, and processes audio faster than real-time. Takes a ~30-96ms audio window and outputs a speech probability. Negligible overhead, runs continuously. This is what LiveKit and most voice agent frameworks use under the hood.

**Earlier approaches** (mostly historical):
- Energy thresholding — if the signal is loud enough, speech is present. Struggles in noisy environments
- Zero-Crossing Rate — measures how often the waveform crosses zero. Speech has a characteristic moderate ZCR; static is very high, hum is very low. Neither is reliable alone

### Speech-to-Text (STT)

**What it does**: converts audio into text. In streaming mode, emits partial transcripts that update in real time as more audio arrives.

**Options**:

| Model | Type | Notes |
|---|---|---|
| Whisper (OpenAI) | Open weight | The workhorse. Multiple sizes. Can run locally or via API |
| Deepgram | Commercial API | Optimized for speed and low latency. Popular in production |
| OpenAI Whisper API | Commercial API | Hosted Whisper. Simple to use, one API key |
| AssemblyAI | Commercial API | Strong accuracy, good streaming support |

**Key metric**: Word Error Rate (WER) — the percentage of words transcribed incorrectly.

**Endpointing** operates here: the STT system (or a separate component) decides when the user has finished their turn. Typically a silence duration threshold (500-800ms) optionally supplemented with linguistic cues like grammatical completeness.

The endpointing tradeoff: too short and you cut people off mid-thought ("I want a flight to... *[thinking]*... Paris"). Too long and the agent feels sluggish.

### Large Language Model (LLM)

**What it does**: takes the transcribed text and generates a response. This is the "brain" — where reasoning, personality, and knowledge live.

This is the component most familiar to builders working with AI. The same models used for text chat (GPT-4o, Claude, Llama, etc.) work here. The key difference in a voice context is that **time to first token (TTFT)** matters more than total generation time, because TTS can start producing audio as soon as the first tokens arrive.

System prompts define the agent's persona, behavior, and constraints — just like in a text chatbot.

### Text-to-Speech (TTS)

**What it does**: converts the LLM's text response into spoken audio. In streaming mode, starts generating audio from the first few tokens before the full response exists.

**Options**:

| Model | Type | Notes |
|---|---|---|
| OpenAI TTS | Commercial API | Good quality, simple (same API key as LLM) |
| ElevenLabs | Commercial API | High quality, voice cloning, wide voice library |
| Cartesia | Commercial API | Designed for low latency in real-time pipelines |
| Kokoro | Open weight | Surprisingly good quality for an open model |
| PlayHT | Commercial API | Natural-sounding, good for long-form |

**Key metric**: Mean Opinion Score (MOS) — human judges rate naturalness on a 1-5 scale.

**What does the output voice sound like?** This is a design decision. You can choose from pre-built voices, or use **voice cloning** — providing a short audio sample of a target voice, from which the model extracts a **speaker embedding** (a vector that captures the unique characteristics of that voice: timbre, pitch range, resonance, speaking rhythm). The TTS model then generates new speech that sounds like that person.

Voice cloning raises both powerful possibilities (brand-consistent voice, personalized agents) and serious ethical questions (consent, deepfakes, impersonation).

### The pipeline glue: orchestration

Individual components don't do much alone. An orchestration framework manages:
- Connecting components in a streaming pipeline
- WebRTC audio transport to/from the browser
- Room and session management
- VAD → STT → LLM → TTS data flow
- Interruption handling (user starts talking while agent is speaking)

**LiveKit Agents** is the framework we use in this workshop. It provides a plugin system where you swap providers by changing an import — same pipeline structure, different models underneath.

## Architectures

### Cascaded pipeline

```
[AUDIO] → VAD → STT → [TEXT] → LLM → [TEXT] → TTS → [AUDIO]
```

The dominant production architecture. Each component is a separate model, and the pipeline streams — each stage feeds into the next in real time:

1. Audio streams continuously into **VAD**
2. When VAD detects speech, audio chunks flow to **STT**, which transcribes incrementally
3. **Endpointing** decides "the user is done talking"
4. The full transcript goes to the **LLM**, which streams tokens back
5. LLM tokens stream into **TTS**, which starts generating audio before the LLM is finished

**Benefits:**
- Legible and easy to monitor — you can inspect text at every boundary
- Content filtering and compliance checks are straightforward (it's all text)
- Clear separation of concerns; swap components independently
- Best-in-class model for each step
- Established evaluation ecosystem (WER, MOS, etc.)
- Tool calling is natural — the LLM works with text, same as in any chat application

**Challenges:**
- Latency — multiple inference steps, each adds time
- Prosody loss — emotional information is discarded at the audio→text boundary, then reinvented at text→audio

> **Prosody**: the patterns of stress and intonation in language — intonation, stress, pace, phrasing, pauses. The same sentence can mean very different things depending on *how* it's said. Transcribe both versions and you get identical text, but the meaning differs. This is the information cascaded systems lose — non-linguistic signals that modify meaning.

### Speech-to-speech (realtime)

Speech in, speech out. One model — no separate STT or TTS steps. The model IS the LLM, and it has to encode everything in a single set of weights:

1. World knowledge (like a text LLM)
2. Speech understanding (like an STT model)
3. Speech generation (like a TTS model)
4. Conversational dynamics (turn-taking, interruption)
5. Paralinguistic features (emotion, prosody, emphasis)

This is why these models are enormous and hard to build.

**Benefits:**
- Eliminates two inference steps — significant latency reduction
- Prosody preservation end-to-end (no lossy text bottleneck)
- More natural conversational dynamics (full-duplex is possible)

**Challenges:**
- Single black box — harder to debug, monitor, and control
- Content filtering is harder (no text to inspect mid-pipeline)
- Enormous models, expensive to train
- Less mature tooling and evaluation ecosystem
- **Tool calling is an open question** — with no text stage, how does the model call a function? Some models (e.g. OpenAI Realtime API) handle this by emitting text-mode function calls alongside audio output, effectively maintaining a hidden text channel. This is an active area of development and a real architectural tension

#### Audio tokenization

Speech-to-speech models need to convert audio into discrete tokens a transformer can process. This is similar in *purpose* to text tokenization, but fundamentally different in mechanism.

**Neural audio codecs** (EnCodec, SoundStream, Mimi) are learned compression schemes — neural network encoder-decoders trained to compress and reconstruct audio. Traditional codecs like MP3 use hand-designed algorithms to decide what to discard; neural codecs *learn* what matters perceptually, achieving better quality at lower bitrates.

The encoder takes raw audio samples and outputs a continuous vector (e.g. 128 floats) per time frame (~13ms). This vector is then quantized using **Residual Vector Quantization (RVQ)**.

**How RVQ works** (for one ~13ms frame):

1. Codebook 1 finds the nearest entry to the encoder's vector → **code 742**. Compute the residual (the difference between the original and codebook 742's vector)
2. Codebook 2 finds the nearest entry to *that residual* → **code 91**. Compute the new residual
3. Codebook 3 finds the nearest to the remaining residual → **code 1533**
4. Continue for 4-8 codebook layers

One frame becomes an ordered tuple of integers: `[742, 91, 1533, 407, ...]`. Sum all the corresponding codebook vectors → you approximately reconstruct the original encoder output.

Key properties:
- The first code captures coarse structure ("voiced 'ah' at 200Hz")
- Each subsequent code corrects what previous ones missed (resonance, breathiness, fine detail)
- **Order matters** — code 2 encodes the residual *from* code 1, so it's meaningless alone
- Analogy: progressive JPEG loading. First pass gives a blurry image, each pass sharpens. Shuffle the passes and you get garbage

Typical codebook size: 1024-8192 entries. With 8 RVQ layers, the effective expressiveness is ~1024^8 combinations — more than enough for prosody, emotion, speaker identity, and background acoustics.

**Streaming**: fixed time intervals at ~75 frames/sec. Each frame produces one code per codebook layer. One second of audio ≈ 75 frames × 8 layers = 600 codes.

**Decoding**: sum the codebook vectors for each frame, pass through the decoder network → reconstructed audio waveform.

#### Training speech-to-speech models

Multiple stages:

1. **Text pretraining** — standard LLM training on massive text corpora. This is where world knowledge comes from. Some models (e.g. Ultravox) start from an existing text LLM and add audio capabilities on top
2. **Audio codec training** — trained separately on large amounts of raw audio to compress and reconstruct faithfully. Self-supervised: the only objective is "make the output sound like the input"
3. **Bridging audio and text** — paired data like audiobooks and podcasts with transcripts. The model learns that audio code sequence X corresponds to text sequence Y. This is where semantic understanding of audio comes from — the transcript is the label
4. **Conversational fine-tuning** — dialogue data, often synthetic (text models generate conversations, TTS synthesizes the audio). Turn-taking behavior and conversational dynamics are learned here

Emotion and prosody are learned implicitly. The codec preserves prosodic information in its codes (it's trained to reconstruct audio faithfully), so when the model sees enough varied speech, it picks up the statistical patterns. Nobody labels millions of hours of audio with emotions — the model learns from the structure of the codes, grounded by text transcripts that provide semantic context.

#### Moshi (case study)

Moshi by Kyutai is a fully open speech-to-speech model with a genuinely novel architecture:

- **Temporal transformer** — attends across time steps within one codebook level (what came before in this stream?)
- **Depth transformer** — attends across codebook levels at a single time step (how do coarse and fine details relate right now?). Needed because codes must be predicted in order within each frame
- **Inner monologue** — generates speech AND text tokens in parallel streams. The text stream acts as an internal reasoning chain for semantic coherence. Not shown to the user — it's scaffolding for the model's own thinking
- **Full-duplex** — models both speakers simultaneously, always listening and potentially speaking. No strict turn-taking

### Mental model

**Cascaded = Unix philosophy** — small, specialized tools piped together. Lossy at boundaries, but modular, debuggable, and you can use the best tool for each job.

**Speech-to-speech = one model that natively speaks audio** — preserves everything end-to-end, but you give up modularity and interpretability.

## Choosing an architecture

The key question: does naturalness or control matter more for your use case?

| Use case | Architecture | Deciding factor |
|---|---|---|
| Therapy, coaching, mental health | Speech-to-speech | Emotional nuance is critical |
| Multilingual support | Speech-to-speech | Cross-language expressiveness |
| Premium / luxury customer experience | Speech-to-speech | Experience quality over cost |
| High-volume support (tier 1) | Cascaded | Cost and scale |
| Regulated industries (finance, healthcare, legal) | Cascaded | Auditability, compliance |
| Tool-heavy workflows | Cascaded | Text needed for function calls |
| Anything requiring audit trails | Cascaded | Full pipeline observability |

*Adapted from [Coval's architecture comparison](https://www.coval.dev/blog/speech-to-speech-vs-cascaded-voice-ai-which-architecture-should-you-deploy)*

## Complementary technologies

- **Egress** — recording and streaming agent conversations
- **Ingress** — bringing external media streams into the pipeline
- **RAG** — grounding responses in real-time data
- **Tool calls** — letting the agent take actions (API calls, database lookups, etc.)
- **Telephony** — connecting voice agents to phone systems via Twilio or native SIP

## Glossary

| Term | Definition |
|---|---|
| **Cascaded pipeline** | Voice agent architecture using separate models for STT, LLM, and TTS, connected in a streaming chain |
| **Codec** | Coder-decoder. Compresses data into a smaller representation and decompresses it back. MP3 is a traditional audio codec; EnCodec is a neural audio codec |
| **CNN** | Convolutional neural network. Slides learned filters across input data (images, spectrograms) to detect spatial patterns |
| **Endpointing** | Deciding when a user has finished their conversational turn, typically based on silence duration and/or linguistic cues |
| **Full-duplex** | Both parties can transmit simultaneously — listening and speaking at the same time, like a real conversation |
| **LLM** | Large language model. The "brain" of the agent — generates responses from text input |
| **MOS** | Mean Opinion Score. Human judges rate audio naturalness on a 1-5 scale |
| **Neural audio codec** | A learned compression scheme (e.g. EnCodec, Mimi) that converts raw audio into discrete codes via an encoder-decoder neural network |
| **Prosody** | Patterns of stress, intonation, pace, and phrasing in speech. Carries meaning that transcription discards |
| **RVQ** | Residual Vector Quantization. Compresses a vector into a sequence of codebook indices, each correcting the error of the previous |
| **Speaker embedding** | A fixed-size vector capturing what makes a voice sound like a particular person — timbre, pitch range, resonance, rhythm. Used for voice cloning and speaker identification |
| **Spectrogram** | A time × frequency representation of audio, visualized as an image. The input format for many audio ML models |
| **STT / ASR** | Speech-to-text / Automatic Speech Recognition. Converts audio to text |
| **Streaming** | Processing and delivering data incrementally as it's produced, rather than waiting for the complete result |
| **TTS** | Text-to-speech. Converts text to spoken audio |
| **TTFT** | Time to first token. How quickly a model starts producing output — critical for perceived responsiveness |
| **VAD** | Voice Activity Detection. Determines whether an audio signal contains human speech |
| **Voice cloning** | Using a speaker embedding extracted from a short audio sample to generate new speech in that voice |
| **WebRTC** | Web Real-Time Communication. Browser-native protocol for real-time audio/video, used by LiveKit |
| **WER** | Word Error Rate. The percentage of words transcribed incorrectly by an STT model |

## Resources

### Architecture and concepts
- [Coval: S2S vs Cascaded architecture comparison](https://www.coval.dev/blog/speech-to-speech-vs-cascaded-voice-ai-which-architecture-should-you-deploy) — good overview of when to use which
- [Coval: Voice AI evaluation metrics](https://www.coval.dev/blog/voice-ai-evaluation-in-2026-the-5-metrics-that-actually-predict-production-success)

### Papers
- [Voice Agent survey (2025)](https://arxiv.org/html/2603.05413v1) — comprehensive overview of the field
- [Moshi paper (Kyutai)](https://arxiv.org/abs/2410.00037) — full-duplex speech-to-speech, inner monologue, depth/temporal transformers
- [EnCodec (Meta)](https://arxiv.org/abs/2210.13438) — neural audio codec with RVQ, foundational for audio tokenization
- [Better Naturalness Evaluation of TTS Systems](https://ieeexplore.ieee.org/document/11362964)

### Frameworks and tools
- [LiveKit Agents docs](https://docs.livekit.io/agents/) — the framework we build with in this workshop
- [LiveKit Agents GitHub](https://github.com/livekit/agents) — source code, examples
- [Silero VAD](https://github.com/snakers4/silero-vad) — the standard VAD model, used by LiveKit and most voice agent frameworks

### Models and providers
- [Whisper (OpenAI)](https://github.com/openai/whisper) — open weight STT, the workhorse
- [Deepgram](https://deepgram.com/) — fast commercial STT, popular for low-latency pipelines
- [Cartesia](https://cartesia.ai/) — low-latency TTS, designed for real-time voice agents
- [Kokoro](https://github.com/hexgrad/kokoro) — open weight TTS, surprisingly good quality
- [ElevenLabs](https://elevenlabs.io/) — high-quality commercial TTS, voice cloning
- [Ultravox (Fixie)](https://github.com/fixie-ai/ultravox) — open weight, hybrid approach (audio features projected into LLM embedding space)
- [Moshi (Kyutai)](https://github.com/kyutai-labs/moshi) — fully open speech-to-speech

### Telephony
- [Twilio Voice](https://www.twilio.com/docs/voice) — telephony integration, connect voice agents to phone numbers
- [LiveKit SIP](https://docs.livekit.io/sip/) — native SIP/telephony support without a third-party provider
