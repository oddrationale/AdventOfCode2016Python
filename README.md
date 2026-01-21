# Advent of Code 2016

Python solutions for [Advent of Code 2016](https://adventofcode.com/2016) using Python.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### 1. Install uv

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Configure Advent of Code Session

To automatically fetch puzzle inputs, you need your Advent of Code session token:

1. Log in to [adventofcode.com](https://adventofcode.com)
2. Open browser DevTools (F12)
3. Go to Application/Storage → Cookies → `https://adventofcode.com`
4. Copy the value of the `session` cookie
5. Create a `.env` file in the project root:

```bash
AOC_SESSION=your_session_token_here
```

⚠️ **Never commit your `.env` file to version control!**

## Running Solutions

Run any day's solution using:

```bash
uv run --env-file .env day01.py
```

Replace `day01.py` with the appropriate day file (e.g., `day02.py`, `day03.py`, etc.).


## Dependencies

- **[advent-of-code-data](https://github.com/wimglenn/advent-of-code-data)** - Automatic puzzle input fetching
- **Python 3.11+** - For modern type hints and features

