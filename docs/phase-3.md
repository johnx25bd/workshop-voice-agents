# Phase 3: Add tool calling

Your agent can talk, but it can't *do* anything. In phase 2 you gave it knowledge through the system prompt, but that knowledge is static - baked in at startup. In this phase, you'll give it the ability to call functions: tools that let it retrieve live information or take actions in the world.

## What are tools?

Tool calling is the mechanism that lets an LLM do things beyond generating text. The LLM decides it needs external information or wants to trigger an action, emits a structured function call, your code executes it, and the result goes back to the LLM to inform its response.

Tools generally fall into two categories:

- **Retrieval** - fetching information the agent doesn't have in its system prompt. Checking a database, looking up a price, getting live data. This is the core of what people call **retrieval-augmented generation (RAG)** - the agent retrieves context at runtime to generate a better response. If you've heard of [MCP (Model Context Protocol)](https://modelcontextprotocol.io/), it's a standardized way to connect tools and data sources to LLMs.
- **Actions** - doing something with side effects. Sending an email, creating a calendar invite, placing an order, transferring a call. The agent isn't just answering questions, it's making things happen.

Both use the same mechanism in code, but they carry very different risks. A retrieval tool that looks up the weather is low-stakes. An action tool that sends an email on someone's behalf needs serious thought about security and reliability.

## Security and reliability

Be thoughtful here. A voice agent with tool access can take actions in the real world based on what someone says over a microphone. Consider:

- **Authentication** - who is the caller? Should the agent verify identity before accessing sensitive data or taking actions?
- **Scope** - limit what each tool can do. A tool that reads from a database is safer than one that writes to it
- **Confirmation** - for consequential actions, have the agent confirm before executing ("I'm about to send that email to sarah@example.com. Should I go ahead?")
- **Error handling** - what happens when a tool fails? The user is waiting in silence. The agent should handle failures gracefully
- **Latency** - the user waits while tools execute. Keep calls fast (under 1-2 seconds) or have the agent say something like "let me check on that" first

## How tool calling works in the pipeline

In the cascaded architecture, tool calling fits naturally because the LLM already works with text:

1. User speaks, STT transcribes to text
2. LLM sees the text and decides it needs to call a tool
3. LLM emits a function call (tool name + arguments) instead of a regular response
4. Your code executes the function and returns the result to the LLM
5. LLM uses the result to generate a spoken response
6. TTS converts the response to audio

LiveKit Agents handles steps 2-5 automatically. You just define the tools.

## Define a tool

Tools are methods on your `Agent` class, decorated with `@function_tool`. The LLM reads the docstring and type hints to understand when and how to use the tool.

Here's the pattern:

```python
from livekit.agents import Agent, RunContext, function_tool

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful assistant that can look up information.",
        )

    @function_tool
    async def get_weather(self, context: RunContext, city: str) -> str:
        """Get the current weather for a city.

        Args:
            city: The name of the city to check weather for.
        """
        # In a real agent, this would call a weather API.
        # Here we simulate the response.
        current_temp = 18  # would come from API
        conditions = "partly cloudy"  # would come from API
        return f"It's currently {current_temp}°C and {conditions} in {city}."
```

Key details:
- The `@function_tool` decorator registers the method as a callable tool
- The **docstring** is what the LLM reads to decide when to use the tool. Write it clearly
- **Type hints** on the parameters tell the LLM what arguments to provide
- The return value goes back to the LLM as context for generating a response
- `RunContext` provides access to session state if you need it

## Your turn

Add one or more tools to your agent. Think about what fits the scenario you built in phase 2:

- **A retrieval tool** - look up a class schedule, check appointment availability, get a product price. This is RAG in action
- **A state tool** - remember something the caller said, keep a list, take a message
- **An action tool** - book an appointment, send a notification (simulate these for now, don't wire up real services in the workshop)

The tool doesn't need to call a real external API. Simulating the response is fine for learning the pattern. The important thing is understanding how the LLM decides when to call a tool and how results flow back.

<details>
<summary>Hints</summary>

- You need to import `function_tool` from `livekit.agents`
- The tool method must be `async` and on your `Agent` class
- The first two params are always `self` and `context: RunContext`
- Additional params are the tool's arguments (with type hints)
- Return a string - this is what the LLM sees as the tool result

</details>

<details>
<summary>Example: gym agent with class schedule lookup and message taking</summary>

```python
from livekit.agents import Agent, RunContext, function_tool


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are the voice assistant for FitSpace gym.
            You can look up the class schedule and take messages for staff.
            Only discuss gym-related topics.""",
        )
        self.messages = []

    @function_tool
    async def check_class_schedule(self, context: RunContext, day: str) -> str:
        """Check what classes are available on a given day.

        Args:
            day: The day of the week to check (e.g. "monday", "tuesday").
        """
        schedule = {
            "monday": "Spin 6:30am, HIIT 12pm",
            "tuesday": "Yoga 7pm, HIIT 12pm",
            "wednesday": "Spin 6:30am, HIIT 12pm",
            "thursday": "Yoga 7pm, HIIT 12pm",
            "friday": "Spin 6:30am, HIIT 12pm",
            "saturday": "HIIT 10am, Yoga 2pm",
            "sunday": "Yoga 10am",
        }
        classes = schedule.get(day.lower())
        if classes:
            return f"Classes on {day}: {classes}"
        return f"No classes found for {day}. We're open Monday through Sunday."

    @function_tool
    async def take_message(self, context: RunContext, name: str, message: str) -> str:
        """Take a message for the front desk staff.

        Args:
            name: The caller's name.
            message: The message to leave.
        """
        self.messages.append({"name": name, "message": message})
        return f"Message recorded from {name}. The team will see this when the front desk opens."
```

</details>

<details>
<summary>Go deeper: Connecting real APIs and MCP</summary>

For a production agent, tools would call real services:

```python
import httpx

@function_tool
async def get_weather(self, context: RunContext, city: str) -> str:
    """Get the current weather for a city."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://wttr.in/{city}?format=3")
        return resp.text
```

For standardized tool integration, look at [MCP (Model Context Protocol)](https://modelcontextprotocol.io/). MCP defines a standard way for LLMs to connect to data sources and tools, so you can plug in existing MCP servers rather than writing custom tool functions for everything.

</details>

## Test it

1. Add your tool(s) to your agent class
2. Run `uv run python agent.py dev`
3. Have a conversation that would naturally trigger the tool
4. Watch the console output - you'll see when the LLM decides to call your tool

Does the LLM use the tool when you expect? Does it pass reasonable arguments? Try edge cases. You may need to refine your docstring or system prompt to guide when and how tools get used.

## Checkpoint

Your agent can now do things, not just talk. It can retrieve information at runtime and take actions. This is the fundamental difference between a chatbot and an agent.

Notice how tool calling fits naturally in the cascaded pipeline because the LLM works with text, so function calls are straightforward. In the next phase, you'll see what happens when we remove the text stage entirely.

When you're ready, move on to **[Phase 4: Realtime models](phase-4.md)**.
