# ReportAI

<img alt="reportAI Logo" src="https://raw.githubusercontent.com/AdirthaBorgohain/ReportAI/main/report_ai/assets/logos/reportAI-logo-light.png" width="200"/>

reportAI is a Python-based tool that generates comprehensive PDF research reports using AI. Simply input conversations 
with an AI model in a structured format, and reportAI will produce a detailed report complete with an executive summary, 
properly formatted sections, tables, and figures. Using cleverly implemented techniques to deduplicate any repeated 
content in the report, it ensures all the content are straight to the point while being descriptive without creating 
any repetition on the report content. The final output is a PDF of around 9-15 pages depending on the number of messages 
passed for report generation.

## Features

- Generates detailed research reports from AI-generated conversations.
- Produces sections with headers, tables, and figures.
- Customizable via environment variables.
- Easy to use with minimal setup.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AdirthaBorgohain/reportAI.git
cd reportAI
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

## Sample Report

A sample generated report generated using the messages in `report.py` can be found in `report_ai/reports/sample.pdf`.

Here are some screenshots of the sample report:

<img alt="Report Cover" src="https://raw.githubusercontent.com/AdirthaBorgohain/ReportAI/main/report_ai/assets/screenshots/1.png" width="500"/>

<img alt="Report Content" src="https://raw.githubusercontent.com/AdirthaBorgohain/ReportAI/main/report_ai/assets/screenshots/2.png" width="500"/>

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
    <img alt="LangChain Logo" src="https://raw.githubusercontent.com/AdirthaBorgohain/ReportAI/main/report_ai/assets/logos/langchain-logo-light.svg" width="100"/>
</a>
