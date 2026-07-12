# 🤝 Contributing to A.I.M. Flight Recorder

First off, thank you for considering contributing to the Flight Recorder! 

This skill is designed to be a transparent window into the often opaque world of agentic trajectories. Whether you're fixing a bug, adding a new extraction feature, or improving the markdown formatting, your help is appreciated.

## Getting Started

1. **Fork the Repository**: Start by forking the `aim-flight-recorder` repository to your GitHub account.
2. **Clone and Install**:
   ```bash
   git clone https://github.com/<your-username>/aim-flight-recorder.git
   cd aim-flight-recorder
   
   # Symlink it to your local Antigravity environment to test live!
   ln -s $(pwd) ~/.gemini/antigravity-cli/skills/aim-flight-recorder
   ```

## Development Workflow

1. **Create a Branch**: Always branch out before making changes. If you are using the A.I.M. Exoskeleton locally, just run `aim-flight-recorder bug` and `aim-flight-recorder fix <id>`.
2. **Test Your Changes**: Run your modifications locally against real `.jsonl` session data. You can easily find active UUIDs by running `python3 scripts/list_sessions.py`.
3. **Commit**: Write clear, descriptive commit messages.
4. **Push & Pull Request**: Push your branch up to your fork and open a Pull Request against the `main` branch of the original repository.

## Contribution Guidelines

- **Keep Dependencies Zero**: The Flight Recorder scripts should ideally only rely on the Python Standard Library (`os`, `sys`, `json`, `argparse`, `glob`, `datetime`) to ensure it runs out-of-the-box in any standard Linux environment without requiring a complex `pip install` or `requirements.txt`.
- **Maintain Markdown Integrity**: The primary output of this tool is a `.md` file. Always ensure your changes emit properly formatted GitHub Flavored Markdown (e.g., closing code blocks, properly escaping agent text).
- **Update SKILL.md**: If you add new CLI arguments or modes to `flight_recorder.py`, you **MUST** update the documentation in `SKILL.md` so that the AI Agents know how to use your new feature!

## Reporting Bugs

If you find a parsing error or a session log that crashes the script:
- Open an Issue on GitHub.
- Include the specific `type` of the JSON block that caused the crash (if known). Do not upload your full `transcript.jsonl` publicly if it contains sensitive API keys or private codebase code!
