# ReportAI
<div style="text-align: center;">
    <img alt="ReportAI Logo" src="report_ai/assets/reportAI-logo.png" width="200"/>
</div>

ReportAI is a Python-based tool that generates comprehensive PDF reports using AI. Simply input conversations with an AI
model in a structured format, and ReportAI will produce a detailed report complete with an executive summary, properly
formatted sections, tables, and figures. Using cleverly implemented techniques to deduplicate any repeated content in
the report, it ensures all the content are straight to the point while being descriptive without creating any repetition
on the report content.

## Features

- Generates detailed reports from AI-generated conversations.
- Produces sections with headers, tables, and figures.
- Customizable via environment variables.
- Easy to use with minimal setup.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ReportAI.git
cd ReportAI
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your .env (inside `report_ai` directory) file with the necessary API keys and model configurations:

```makefile
OPENAI_API_KEY={YOUR OPENAI API KEY}

ANTHROPIC_API_KEY={YOUR ANTHROPIC API KEY}

LLM={CHOICE OF LLM TO USE. Valid values are 'gpt', 'claude'}

GPT_MODEL={GPT MODEL TO USE IN CASE LLM IS SET TO 'gpt'. Valid values are 'gpt-3.5-turbo', 'gpt-4-turbo', 'gpt-4o'}

CLAUDE_MODEL={CLAUDE MODEL TO USE IN CASE LLM IS SET TO 'claude'. Valid values are 'claude-3-haiku', 'claude-3-opus'}
```

## Usage

Checkout `report.py` for an example on how to generate reports using your conversations.

## Contributing

1. Fork the repository.
2. Create a new feature branch (git checkout -b feature/new-feature).
3. Commit your changes (git commit -m 'Add some new feature').
4. Push to the branch (git push origin feature/new-feature).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

### This project is built using:

<a href="https://github.com/langchain/langchain" target="_blank">
    <img alt="LangChain Logo" src="report_ai/assets/langchain-logo-light.svg" width="100"/>
</a>
