# Solana MCP & AI Integration Platform

This repository contains a comprehensive suite of Solana blockchain programs and Python AI/MCP (Model Context Protocol) integration tools.

## Project Structure

- `/solana` - Solana blockchain programs and client applications
  - `/programs` - Smart contracts written in Rust for the Solana blockchain
  - `/clients` - JavaScript/TypeScript clients to interact with the Solana programs
- `/python` - Python-based AI and MCP implementation
  - `/mcp` - Model Context Protocol implementation
  - `/ai` - Artificial Intelligence models and utilities
  - `/utils` - Shared utilities and helpers
- `/docs` - Documentation for the project
- `/scripts` - Utility scripts for the project

## Features

- Solana Programs for decentralized AI model management
- Model Context Protocol implementation for efficient AI model utilization
- Integration between blockchain and AI systems
- Advanced data processing and analysis tools

## Getting Started

See the documentation in the `/docs` folder for setup instructions and usage examples.

## Generating Commit History

This repository includes a script to generate fake commit history for demo or testing purposes. The script creates meaningful commits with actual code changes to simulate real development activity.

### Prerequisites

- Python 3.6 or higher
- Git

### Running the Script

```bash
cd repo
python scripts/generate_commits.py
```

### Options

- `--start-date`: Start date in YYYY-MM-DD format (default: 2025-01-11)
- `--end-date`: End date in YYYY-MM-DD format (default: 2025-04-25)
- `--min-commits`: Minimum commits per day (default: 1)
- `--max-commits`: Maximum commits per day (default: 5)
- `--repo-root`: Root directory of the repository (default: .)

Example:

```bash
python scripts/generate_commits.py --start-date 2025-01-11 --end-date 2025-04-25 --min-commits 2 --max-commits 6
```

This will generate between 2 and 6 commits per day, from January 11, 2025, to April 25, 2025, with random changes to the codebase.

## License

MIT License 