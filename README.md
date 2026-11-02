# 🤖 chatbot — AI-CLUB Workshop Project

A minimal terminal chatbot built as part of the **AI-CLUB workshop**: a tiny CLI
 REPL that talks to the [OpenRouter](https://openrouter.ai) chat-completions API and
 remembers the whole conversation.

## What it does

- Runs an interactive REPL (`:` prompt) in your terminal
- Keeps multi-turn memory: user **and** assistant messages are stored
- Renders model replies as Markdown (via [Rich](https://github.com/Textualize/rich))
- Handles API errors, timeouts, and `Ctrl+C` / `Ctrl+D` gracefully

## Setup

Requirements: [uv](https://docs.astral.sh/uv/) and Python `>= 3.14` (uv will handle the rest).

```bash
# 1. Install dependencies
uv sync

# 2. Get a free API key from https://openrouter.ai/keys
export OPENROUTER_API_KEY="sk-or-..."

# 3. Run the chatbot
uv run chatbot
# or, equivalently:
uv run python -m chatbot.main
```

## Usage example

```
============================================================
                     MY CHATBOT
============================================================
Type your message, Ctrl+D or Ctrl+C to quit.

: Say hi in 3 words
Hello there! 👋
:
```

## How it works

The whole app lives in ~70 lines in [`src/chatbot/main.py`](src/chatbot/main.py):

| Function | Purpose |
|---|---|
| `config()` | Reads `OPENROUTER_API_KEY` from the environment and sets the model (`openrouter/free`) |
| `to_llm(chat)` | POSTs the message history to OpenRouter's `/chat/completions` endpoint and returns the assistant's reply text |
| `add(role, content)` | Appends a message to the running conversation history |
| `main()` | The REPL loop: read input → append → call the API → print the reply (as Markdown) → append the reply to history |

Request flow:

```
: You type something
      │
      ▼
 add("user", <your message>)
      │
      ▼
 to_llm(chat) ──► POST https://openrouter.ai/api/v1/chat/completions
      │                { "model": ..., "messages": chat }
      ▼
 reply = choices[0].message.content
      │
      ▼
 Rich renders it as Markdown
      │
      ▼
 add("assistant", reply)  ◄── so the model remembers its own answers next turn
```

## Workshop concepts demonstrated

- **Chat message format** — the `role` / `content` list (`system`, `user`, `assistant`) used by all major LLM APIs
- **Conversation state** — why the assistant's own replies must go back into the history for multi-turn chat
- **HTTP from Python** — POSTing JSON with `httpx`, sending auth headers
- **Graceful failure** — timeouts, nonzero status codes, and keyboard interrupts handled deliberately instead of crash dumps

## Ideas for further work

- [ ] Streaming replies token-by-token
- [ ] A `system` prompt to give the bot a personality
- [ ] Switch models by selecting from OpenRouter's model list
- [ ] Save / resume conversations to a file
- [ ] A small [Textual](https://github.com/Textualize/textual) TUI instead of `input()`

---

*Built at the AI-CLUB workshop — fork it, break it, improve it! 🚀*
