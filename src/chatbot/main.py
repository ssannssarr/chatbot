from __future__ import annotations
import httpx
from rich.console import Console
from rich.markdown import Markdown as md
from typing import Any
import os

console = Console()

def config() -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = "openrouter/free"

    return {
        "api_key": api_key,
        "model": model,
    }


def to_llm(
        chat: list[dict[str, Any]]
) -> dict[str, Any]:
    cfg = config()
    payload = {
        "model": cfg["model"],
        "messages": chat
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg["api_key"]}"
    }

    res = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60.0
    )
    res.raise_for_status()

    return res.json()["choices"][0]["message"]["content"]

chat = []

def add(
        role: str,
        content: str,
):
    chat.append({
        "role": role,
        "content": content
    })


def main():
    print("="*60)
    print(" "*20,"MY CHATBOT")
    print("="*60)
    print("Type your message, Ctrl+D or Ctrl+C to quit.\n")

    try:
        while True:
            try:
                prmpt = input(": ")
            except EOFError:
                break
            if not prmpt.strip():
                continue
            add(
                role="user",
                content=prmpt
            )
            try:
                res = to_llm(chat=chat)
            except httpx.TimeoutException:
                console.print("[red]Request timed out, try again.[/red]")
                chat.pop()
                continue
            except httpx.HTTPStatusError as err:
                console.print(f"[red]API error {err.response.status_code}: {err.response.text}[/red]")
                chat.pop()
                continue
            console.print(md(res))
            add(
                role="assistant",
                content=res
            )
    except KeyboardInterrupt:
        pass

    print("\nBye!")

if __name__ == "__main__":
    main()
