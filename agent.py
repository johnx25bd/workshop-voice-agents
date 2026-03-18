"""
Voice Agent — Workshop Skeleton

This file will become your voice agent. By the end of phase 1,
it will listen to your voice, think with an LLM, and speak back.

Follow the tutorial at docs/phase-1.md to build it out step by step.
"""

from dotenv import load_dotenv

load_dotenv()

# Phase 1: Build a cascaded voice agent
# ──────────────────────────────────────
#
# 1. Import the LiveKit agents framework and plugins
#    - You'll need: agents, AgentServer, AgentSession, Agent, room_io
#    - Plugins: silero (for VAD), noise_cancellation
#
# 2. Define your Agent class
#    - Inherit from Agent
#    - Set instructions that tell the LLM how to behave
#    - Keep responses concise — this is voice, not text
#
# 3. Create an AgentServer and define a session handler
#    - Configure the cascaded pipeline: STT, LLM, TTS, VAD
#    - Start the session with room connection and audio options
#    - Generate an initial greeting
#
# 4. Run the app
#    - Use the LiveKit CLI runner to start your agent
#
# See docs/phase-1.md for detailed guidance, or check the solution
# dropdown if you get stuck.
