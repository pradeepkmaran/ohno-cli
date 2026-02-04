#!/usr/bin/env python3

import sys
import os
import shlex
import subprocess

# ---------------------------------------------------------------------------
# Capture caller working directory (IMPORTANT)
# ---------------------------------------------------------------------------
CALLER_CWD = os.getcwd()

import ollama  # works because wrapper uses venv python

MODEL = "llama3.2:3b"

SYSTEM_PROMPT = (
    "You are a Linux shell expert.\n"
    f"The user is currently in the directory:\n{CALLER_CWD}\n\n"
    "Convert the user's request into a SINGLE Linux shell command.\n"
    "The command MUST assume it is executed from that directory.\n"
    "Output ONLY the raw command.\n"
    "No explanation, no markdown, no backticks.\n"
)

DESTRUCTIVE_COMMANDS = {
    "rm", "mv", "cp", "mkdir", "touch", "sed", "chmod", "chown",
    "ln", "dd", "truncate", "nano", "vim", "vi", "tee",
}


def is_dangerous(cmd: str) -> bool:
    try:
        tokens = shlex.split(cmd)
    except ValueError:
        return True

    for token in tokens:
        if token in (">", ">>"):
            return True
        if token in DESTRUCTIVE_COMMANDS:
            return True
    return False


def generate_command(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    text = (response.message.content or "").strip()

    if text.startswith("```"):
        text = "\n".join(text.splitlines()[1:-1]).strip()

    if not text:
        print("❌ Model returned empty command")
        sys.exit(1)

    return text


def run_command(cmd: str):
    try:
        tokens = shlex.split(cmd)
    except ValueError as e:
        print(f"❌ Parse error: {e}")
        sys.exit(1)

    needs_shell = any(op in cmd for op in ("|", "&&", "||", ";", "$(", "`"))

    try:
        if needs_shell:
            subprocess.run(cmd, shell=True, check=True, cwd=CALLER_CWD)
        else:
            subprocess.run(tokens, check=True, cwd=CALLER_CWD)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed ({e.returncode})")
        sys.exit(e.returncode)


def main():
    if len(sys.argv) < 2:
        print("Usage: ohno <prompt>")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    command = generate_command(prompt)

    print(f"cmd > {command}")

    if is_dangerous(command):
        confirm = input("⚠️  This may modify files. Continue? (y/n): ").lower()
        if confirm != "y":
            print("❌ Aborted.")
            sys.exit(0)

    run_command(command)


if __name__ == "__main__":
    main()
