"""Shared LLM client using the Claude Code CLI (claude -p).

Uses the Claude Max subscription (OAuth login) — never API credits.
ANTHROPIC_API_KEY is explicitly stripped from the subprocess environment
to prevent accidental billing against API credits.
"""

import json
import logging
import os
import subprocess

log = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-6"


def call_llm(prompt: str, *, system_prompt: str = "", model: str = DEFAULT_MODEL) -> str:
    """Call Claude via the `claude -p` CLI and return the text response.

    Prompts are passed via stdin to avoid shell argument length limits.
    ANTHROPIC_API_KEY is stripped from the environment to force subscription
    auth instead of API credits.

    Args:
        prompt: The user prompt.
        system_prompt: Optional system prompt.
        model: Model alias or full name (default: claude-sonnet-4-6).

    Returns:
        The model's text response as a string.

    Raises:
        subprocess.CalledProcessError: If the CLI exits with a non-zero code.
        ValueError: If the response JSON is missing the expected 'result' field.
        FileNotFoundError: If the `claude` CLI is not installed or not on PATH.
    """
    cmd = [
        "claude", "-p",
        "--model", model,
        "--output-format", "json",
        "--no-session-persistence",
        "--tools", "",
    ]
    if system_prompt:
        cmd.extend(["--system-prompt", system_prompt])

    # Strip ANTHROPIC_API_KEY to force subscription auth (ADR-002)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

    log.debug("Calling claude CLI: model=%s, prompt_len=%d", model, len(prompt))

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"claude CLI returned non-JSON output: {result.stdout[:200]!r}"
        ) from exc

    # Handle both response formats:
    # - dict with "result" key (API-key auth)
    # - list of event objects (subscription auth / streaming JSON)
    if isinstance(data, list):
        for event in data:
            if event.get("type") == "result":
                if event.get("is_error"):
                    raise ValueError(
                        f"claude CLI returned error: {event.get('result', '')[:200]}"
                    )
                return event["result"]
        raise ValueError(
            f"claude CLI response missing 'result' event in stream"
        )

    if "result" not in data:
        raise ValueError(
            f"claude CLI response missing 'result' field: {list(data.keys())}"
        )

    return data["result"]
