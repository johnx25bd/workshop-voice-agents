# Phase 3: Add tool calling

Your agent can talk, but it can't *do* anything. In this phase, you'll give it the ability to call functions  - tools that let it take actions or look up information.

## How tool calling works in a cascaded pipeline

In the cascaded architecture, tool calling is natural because the LLM is already working with text:

1. User speaks → STT transcribes to text
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
        # In a real agent, this would call a weather API
        return f"It's 18°C and partly cloudy in {city}."
```

Key details:
- The `@function_tool` decorator registers the method as a callable tool
- The **docstring** is what the LLM sees  - write it clearly so the model knows when to use this tool
- **Type hints** on the parameters tell the LLM what arguments to provide
- The return value is passed back to the LLM as context for its response
- `RunContext` provides access to session state if you need it

## Your turn

Add one or more tools to your agent. Some ideas depending on your persona:

- **A lookup tool**  - search a dictionary, get a fact, check a price
- **A calculation tool**  - convert units, calculate a tip, estimate cooking time
- **A state tool**  - remember something the user said, keep a list, track a count
- **A creative tool**  - roll dice, draw a tarot card, generate a random recipe suggestion

Try to build at least one tool that fits your agent's persona. The tool doesn't need to call a real external API  - returning a hardcoded or computed string is fine for learning.

<details>
<summary>Hints</summary>

- You need to import `function_tool` from `livekit.agents`
- The tool method must be `async` and on your `Agent` class
- The first two params are always `self` and `context: RunContext`
- Additional params are the tool's arguments (with type hints)
- Return a string  - this is what the LLM sees as the tool result

</details>

<details>
<summary>Example: detective with a case file lookup</summary>

```python
from livekit.agents import Agent, RunContext, function_tool


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Detective Murphy, a hardboiled private eye.
            You can look up case files when someone mentions a name or case number.
            You speak in short, clipped sentences with a noir tone.""",
        )
        self.case_notes = []

    @function_tool
    async def lookup_case(self, context: RunContext, name: str) -> str:
        """Look up a case file by the suspect or client's name.

        Args:
            name: The name of the person to look up.
        """
        cases = {
            "martinez": "Sofia Martinez. Last seen near the docks, Tuesday night. Known associate of Big Eddie.",
            "chen": "Robert Chen. Filed a missing persons report for his business partner. Story doesn't add up.",
            "johnson": "Deceased. Found in the warehouse district. Case closed  - officially.",
        }
        result = cases.get(name.lower())
        if result:
            return f"Case file found: {result}"
        return f"No file on anyone named {name}. Either they're clean or they're careful."

    @function_tool
    async def take_note(self, context: RunContext, note: str) -> str:
        """Write something down in the case notebook.

        Args:
            note: The note to record.
        """
        self.case_notes.append(note)
        return f"Noted. That's {len(self.case_notes)} entries in the notebook."
```

</details>

<details>
<summary>Go deeper: Tool calling with external APIs</summary>

For a real agent, you'd call external services from your tools. The pattern is the same  - just add async HTTP calls:

```python
import httpx

@function_tool
async def get_weather(self, context: RunContext, city: str) -> str:
    """Get the current weather for a city."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://wttr.in/{city}?format=3")
        return resp.text
```

Be mindful of latency  - the user is waiting in silence while your tool runs. External API calls should be fast (under 1-2 seconds) or you should have the agent say something like "let me check on that" first.

</details>

## Test it

1. Add your tool(s) to your agent class
2. Run `uv run python agent.py dev`
3. Have a conversation that would naturally trigger the tool
4. Watch the console output  - you'll see when the LLM decides to call your tool

Does the LLM use the tool when you expect? Does it pass reasonable arguments? You may need to refine your docstring to guide the model.

## Checkpoint

Your agent can now take actions  - it's not just a voice chatbot, it's an agent that can do things. This is the fundamental difference between a chatbot and an agent.

Notice how tool calling works seamlessly in the cascaded pipeline  - the LLM processes text, so function calls are natural. In the next phase, you'll see what happens when we remove the text stage entirely.

When you're ready, move on to **[Phase 4: Realtime models](phase-4.md)**.
