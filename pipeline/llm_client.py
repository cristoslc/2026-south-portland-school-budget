"""Shared LLM client using the Claude Code CLI (claude -p).

Replaces direct Anthropic SDK calls. Requires `claude` to be installed and
authenticated via `claude login` — no ANTHROPIC_API_KEY needed.
"""

import json
import logging
import subprocess

log = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-6"


def call_llm(prompt: str, *, system_prompt: str = "", model: str = DEFAULT_MODEL) -> str:
    """Call Claude via the `claude -p` CLI and return the text response.

    Prompts are passed via stdin to avoid shell argument length limits.

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

    log.debug("Calling claude CLI: model=%s, prompt_len=%d", model, len(prompt))

    result = subprocess.run(
        cmd,
        input=prompt,
        capture_output=True,
        text=True,
        check=True,
    )

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"claude CLI returned non-JSON output: {result.stdout[:200]!r}"
        ) from exc

    if "result" not in data:
        raise ValueError(
            f"claude CLI response missing 'result' field: {list(data.keys())}"
        )

    return data["result"]
