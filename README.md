# ohno

`ohno` is a local CLI tool that lets you run Linux shell commands using natural language prompts.
It converts plain English into a single shell command and executes it safely from your current directory.

---

## Features

- Run shell commands using natural language
- Works from any directory
- No need to activate a virtual environment
- Uses a local LLM via Ollama
- Warns before executing destructive commands
- Executes commands in the caller’s working directory

---

## Requirements

- Linux or macOS
- Python 3.9+
- Ollama installed and running
- A local model (default: `llama3.2:3b`)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/pradeepkmaran/ohno-cli.git
cd ohno-cli
```

### 2. Create virtual environment

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### 3. Install the CLI globally

From inside the project directory:

```bash
chmod +x ohno
sudo ln -sf "$(pwd)/ohno" /usr/local/bin/ohno
```

---

## Usage

Run from any directory:

```bash
ohno list files
ohno count directories
ohno find all txt files
```

For commands that may modify files, confirmation is required before execution.

---

## How it works

- `ohno` is a global shell wrapper
- It always runs the project’s virtual environment Python
- The current working directory is preserved
- The LLM converts the prompt into a single shell command
- The command is executed locally

---

## Safety

Commands that involve file modification or redirection require manual confirmation before execution.

This tool does not run commands automatically without user approval.

---

## Configuration

- Model can be changed in `ohno.py`
- Safety rules are defined in `DESTRUCTIVE_COMMANDS`
- The system prompt can be customized for stricter behavior
