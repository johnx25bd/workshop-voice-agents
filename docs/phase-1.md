# Phase 1: Build a voice agent

By the end of this phase, you'll have a working voice agent running in your browser  - you talk, it listens, thinks, and speaks back.

## What we're building

A **cascaded pipeline** voice agent. Audio flows through separate, specialized models:

```
Your voice → [VAD] → [STT] → [LLM] → [TTS] → Agent speaks
```

- **VAD** (Voice Activity Detection)  - detects when you're speaking
- **STT** (Speech-to-Text)  - transcribes your speech to text
- **LLM** (Large Language Model)  - generates a response
- **TTS** (Text-to-Speech)  - converts the response to spoken audio

LiveKit Agents orchestrates this pipeline for you and handles the WebRTC audio connection between your browser and the agent.

## Architecture

Two things are running:

1. **LiveKit Cloud**  - handles the real-time audio connection (WebRTC). Think of it as the "phone line" between your browser and your agent
2. **Your agent** (Python, running locally)  - connects to LiveKit Cloud, receives audio, runs the pipeline, sends audio back

The browser connects to LiveKit Cloud, and your agent connects to LiveKit Cloud. LiveKit routes audio between them. You don't need to build a frontend  - LiveKit provides the [Agents Playground](https://agents-playground.livekit.io) as a browser UI.

## Setup check

Before writing code, make sure your environment is ready:

```bash
# Verify Python version (need 3.9+)
python --version

# Verify dependencies are installed (use uv run if you installed with uv)
uv run python -c "import livekit.agents; print('livekit-agents installed')"

# Verify your .env file has the required keys
cat .env
```

You should have `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, and `OPENAI_API_KEY` set.

<details>
<summary>Troubleshooting setup</summary>

- **Import error with `python`**: if you installed with `uv`, use `uv run python` instead of `python` - uv manages its own virtual environment
- **Import error with `uv run`**: run `uv sync` again
- **If you used pip**: make sure you activated the venv first (`source .venv/bin/activate`)
- **Missing API keys**: check `.env.example` for the required variables

</details>

## Build your agent

Open `agent.py`. You'll see a skeleton with comments describing what to build. Here's what each piece does:

### Step 1: Imports

You need the LiveKit agents framework and some plugins. The key pieces are:

- `Agent`  - base class for your agent's behavior and instructions
- `AgentServer`  - the server that manages connections to LiveKit
- `AgentSession`  - configures the pipeline (which STT, LLM, TTS to use)
- `silero`  - the VAD plugin (detects when you're speaking)
- `noise_cancellation`  - cleans up audio input

### Step 2: Define your agent

Create a class that inherits from `Agent`. The most important thing here is the `instructions` parameter  - this is the system prompt that tells the LLM how to behave. Keep responses concise and avoid formatting (no markdown, no emoji)  - this is voice, not text.

### Step 3: Create the server and session

The `AgentServer` manages connections. You define a session handler that:

- Configures which models to use for each pipeline stage
- Starts the session with a room connection
- Generates an initial greeting so the agent speaks first

For the cascaded pipeline, you'll set:
- `stt`  - speech-to-text provider (e.g. `openai.STT(model="gpt-4o-transcribe")`)
- `llm`  - language model (e.g. `"openai/gpt-4.1-mini"`)
- `tts`  - text-to-speech provider (e.g. `openai.TTS(voice="coral")`)
- `vad`  - voice activity detection (Silero)

### Step 4: Run the app

The LiveKit CLI runner handles startup, connection management, and graceful shutdown.

### Try it yourself

Using the skeleton comments in `agent.py` and the guidance above, try to fill in the code. You're building about 30 lines of Python.

<details>
<summary>Hints</summary>

- The `Agent` class takes `instructions` as a keyword argument in `__init__`
- `AgentSession` takes the model config as keyword arguments: `stt=`, `llm=`, `tts=`, `vad=`
- STT and TTS use plugin instances: `openai.STT(model="gpt-4o-transcribe")`, `openai.TTS(voice="coral")`
- LLM can be a string: `"openai/gpt-4.1-mini"`
- `silero.VAD.load()` gives you the VAD instance
- `session.start()` takes `room=ctx.room` and `agent=YourAgent()`
- `session.generate_reply()` makes the agent speak first
- `agents.cli.run_app(server)` starts everything

</details>

<details>
<summary>Solution: complete agent.py</summary>

```python
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import openai, noise_cancellation, silero

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful voice AI assistant.
            You provide clear, concise answers to questions.
            Keep your responses short and conversational  - this is a voice interaction,
            not a text chat. Avoid any formatting, symbols, or emoji.""",
        )


server = AgentServer()


@server.rtc_session(agent_name="voice-agent")
async def session_handler(ctx: agents.JobContext):
    session = AgentSession(
        stt=openai.STT(model="gpt-4o-transcribe"),
        llm="openai/gpt-4.1-mini",
        tts=openai.TTS(voice="coral"),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
```

</details>

## Run your agent

Start the agent in development mode:

```bash
# If you installed with uv:
uv run python agent.py dev

# If you installed with pip (venv activated):
python agent.py dev
```

Then open the [LiveKit Agents Playground](https://agents-playground.livekit.io) in Chrome. Connect it to your LiveKit Cloud project and click "Connect." You should be able to talk to your agent.

<details>
<summary>Go deeper: Build your own frontend</summary>

The playground is convenient for development, but if you want a standalone frontend you can customize, clone the React starter:

```bash
git clone https://github.com/livekit-examples/agent-starter-react.git
cd agent-starter-react
npm install
npm run dev
```

</details>

You can also test without a browser using console mode:

```bash
uv run python agent.py console   # or just: python agent.py console
```

This lets you type text input and hear the agent's audio response through your speakers.

## What just happened?

If it's working, trace the flow:

1. Your microphone captures audio → sent to LiveKit Cloud via WebRTC
2. LiveKit routes the audio to your Python agent
3. **Silero VAD** detects that you're speaking
4. **OpenAI GPT-4o Transcribe** converts your speech to text
5. **OpenAI GPT-4.1 mini** generates a text response
6. **OpenAI TTS** converts the response to speech audio
7. Audio streams back through LiveKit to your browser speakers

All of this is streaming  - TTS starts generating audio from the LLM's first tokens, before the full response exists. That's why the response feels fast despite going through four models.

## Checkpoint

Your `agent.py` should now be a working voice agent. You should be able to have a basic conversation with it. If it's not working, compare your code to the solution above and check your `.env` configuration.

When you're ready, move on to **[Phase 2: Make it yours](phase-2.md)**.

<details>
<summary>Go deeper: How does LiveKit connect everything?</summary>

LiveKit uses **WebRTC** (Web Real-Time Communication)  - a browser-native protocol for real-time audio/video. The same tech powers Google Meet and Discord.

When your agent calls `session.start(room=ctx.room)`, it joins a LiveKit **room** as a participant  - just like a human joining a video call. Your browser is another participant in the same room. LiveKit handles the audio routing, encoding, network transport, and echo cancellation.

The `AgentServer` listens for new room sessions. When a browser connects to your LiveKit project, the server spins up your session handler, which creates the agent and joins the room. The `@server.rtc_session` decorator is what ties your handler function to incoming connections.

</details>

<details>
<summary>Go deeper: Run LiveKit locally</summary>

LiveKit Cloud is the easiest way to get started, but LiveKit is open source and can be self-hosted. To run it locally with Docker:

```bash
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  livekit/livekit-server --dev
```

Then set your `.env` to point at your local server:
```
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

See the [LiveKit self-hosting docs](https://docs.livekit.io/home/self-hosting/local/) for more details.

</details>
