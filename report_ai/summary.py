from report_ai.section import additional_guidelines_with_figures
from report_ai.components.llms import invoke_llm
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

SUMMARIZE_CONVERSATION_SYSTEM_PROMPT_TEMPLATE = (
    "As an expert in summarizing bio-medical information, your task is to synthesize and condense key details from "
    "provided dialogue exchange between a user and an AI. Your goal is to integrate the data from all the messages "
    "in the conversation and create a focused summary without repetitions or broad descriptions that flawlessly caters "
    "to your target audience which comprises of C-level executives, crucial decision-makers, and the scientific "
    "community. Make every word count and make space with fusion, compression, and removal of uninformative phrases. "
    "The summary should be concise yet self-contained, e.g., easily understood without looking at the dialogue "
    "exchanges.Your target audience already know you're a language model and your capabilities and limitations, so "
    "don't remind them of that. They're familiar with ethical issues in general so you don't need to remind them about "
    "those either. Your summary should explicitly detail the key findings and not include any section headings. Return "
    "the summarized text only"
)

EXECUTIVE_SUMMARY_SYSTEM_PROMPT_TEMPLATE = (
    "You are an AI expert, specially trained in generating razor-sharp executive summaries for complex research "
    "reports that succinctly capture the essence of the findings. Your task is to craft an executive summary, "
    "ideally formatted in markdown, that flawlessly caters to your target audience which comprises of C-level "
    "executives, crucial decision-makers, and the scientific community. They already know you're a language model and "
    "your capabilities and limitations, so don't remind them of that. They're familiar with ethical issues in general "
    "so you don't need to remind them about those either.\n\n"
    "Your executive summary should adopt the following structural framework:\n"
    "- Introduction: Establish a clear and concise brief about the principal theme of the report and its ultimate "
    "objective. Ensure to provide the right context and basic understanding of the study.\n"
    "- Positive Insights: Here, your focus needs to be on condensing the pivotal positive revelations and arguments "
    "presented in the study, making sure to exhibit their potential benefits and strengths in regard to the subject "
    "matter enveloped by the report.\n "
    "- Areas of Concern: Address the key challenges and limitations that have been identified during the course of "
    "the study. Discuss these areas of improvement and describe any potential roadblocks or factors that may impede "
    "the application or successful implementation of these findings.\n"
    "- Key Findings: In this section, compress the major discoveries or neutral observations made during the "
    "research. Be sure to substantiate these findings with supporting data or formidable evidence, ensuring "
    "intellectual honesty and robustness of the research. Make space with fusion, compression, and removal of "
    "uninformative phrases like 'the article discusses'. It should be highly entity dense and concise yet "
    "self-contained.\n"
    "- Conclusion: Finally, compile the principal points, summarize the overall insights obtained, and propose areas "
    "that would benefit from further research, if applicable. Also, present a definitive Go/No-Go decision, rooted in "
    "the extensive study's findings and arguments. Validate this decision by reference to the evidence and arguments "
    "laid out in the executive summary.\n\n"
    "Your executive summary must adhere to the following guidelines:\n"
    "- **HTML Formatting**: Employ HTML elements for structuring your document. Use appropriate HTML syntax for "
    "headings, lists, emphasis, and tables to enhance readability and organization. Always start from the <body> "
    "element. No need to add initial HTML elements like <html>, <meta>. Use <h2> for section headings and <h3> for sub "
    "headings. Start with a <h2> heading 'Executive Summary'.\n"
    "- Each section should contain a maximum of 3-4 salient bullet points. Moreover, the content generated should be "
    "analytical, highly relevant, objective, and rife with details.\n"
    "{__ADDITIONAL_GUIDELINES__}"
    "Make sure to follow correct syntax for Mermaid code brackets wherever used. Do not mention the word 'Mermaid' in "
    "any of the text."
    "Abstain from general blanket statements and overused clichés and strive to provide unique insights based on a "
    "comprehensive analysis of the data provided."
)


async def generate_conversation_summary(serialized_conversation: str, llm):
    messages = [
        SystemMessage(
            content=SUMMARIZE_CONVERSATION_SYSTEM_PROMPT_TEMPLATE
        ),
        HumanMessage(
            content=serialized_conversation
        ),
    ]
    response = await invoke_llm(messages, llm=llm)
    return response.content


async def design_executive_summary(serialized_conversation: str, llm: BaseChatModel | None = None):
    SYSTEM_PROMPT = EXECUTIVE_SUMMARY_SYSTEM_PROMPT_TEMPLATE.format_map({
        "__ADDITIONAL_GUIDELINES__": additional_guidelines_with_figures
    })
    USER_PROMPT = await generate_conversation_summary(serialized_conversation, llm)

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        ),
        HumanMessage(
            content=USER_PROMPT
        ),
    ]
    response = await invoke_llm(messages, llm=llm)
    html_content = response.content
    return html_content.replace('&gt;', '>')  # Fix errors when arrows are generated incorrectly by LLM
