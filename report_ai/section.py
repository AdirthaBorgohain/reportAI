from typing import Dict
from report_ai.components.llms import invoke_llm
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

SECTION_SYSTEM_PROMPT_TEMPLATE = (
    "Your task is to develop the {__SECTION_HEADING__} portion of a Research Report. You will be provided with an "
    "outline of the section requirements and a dialogue exchange between a user and an AI, which contains relevant "
    "information and insights for your section. Utilize this conversation judiciously to enrich your content. This "
    "section will be structured around key points listed under the following sub headings: {__SUB_SECTION_HEADINGS__}. "
    "Strictly stick to creating content with the given sub headings only.\n"
    "In crafting the {__SECTION_HEADING__} section, please ensure to incorporate the following elements effectively:\n"
    "- **Structured Content**: Organize your section according to the specified sub headings. Each subheading "
    "should address a distinct aspect of the section, presenting information in a logical and cohesive manner.\n"
    "**Key Considerations**:\n"
    "- **HTML Formatting**: Employ HTML elements for structuring your document. Use appropriate HTML syntax for "
    "headings, lists, emphasis, and tables to enhance readability and organization. Always start from the <body> "
    "element. No need to add initial HTML elements like <html>, <meta>. Use <h2> for section headings and <h3> for sub "
    "headings.\n"
    "{__ADDITIONAL_GUIDELINES__}"
    "Remember, the goal is to create a section that is not only informative but also engaging and visually "
    "appealing. To accomplish this, balance your textual content {__CONTENT_ADJECTIVE__} and ensure your section is "
    "meticulously organized and formatted.\n\n"
    "This is what the current report looks like:\n{__SERIALIZED_REPORT__}\n\n IMPORTANT: Keep in mind, it is very very "
    "important that you do not repeat any of the content or information already in the current report. This includes "
    "all figures, tables and texts. Be extra careful on this as the fate of the world depends on this."
)

additional_guidelines_with_figures = (
    "- **Utilization of Tables**: Wherever possible, synthesize data and findings into tables. Tables should be "
    "clearly labeled and include captions summarizing the data they present. Do not number the tables.\n"
    "- **Mermaid Graphics**: If relevant & necessary, integrate Mermaid diagrams to visually represent processes, "
    "relationships, or data structures relevant to your section. Ensure these graphics are pertinent to the content "
    "and effectively aid in conveying complex information simplistically. Do not repeat the same mermaid figures which "
    "are already present in the current report. Remember to always enclose each node label within quotation marks. Put "
    "all mermaid code under a CSS class called 'mermaid'\n\n"
)


async def design_section(serialized_conversation: str, section_dict: Dict, serialized_report: str,
                         llm: BaseChatModel | None = None) -> (str, str):
    if section_dict['heading'] in ["Introduction", "Conclusion"]:
        SYSTEM_PROMPT = SECTION_SYSTEM_PROMPT_TEMPLATE.format_map({
            "__SECTION_HEADING__": section_dict['heading'],
            "__SUB_SECTION_HEADINGS__": "; ".join(section_dict['sub_headings']),
            "__SERIALIZED_REPORT__": serialized_report,
            "__ADDITIONAL_GUIDELINES__": "",
            "__CONTENT_ADJECTIVE__": "well"
        })
    else:
        SYSTEM_PROMPT = SECTION_SYSTEM_PROMPT_TEMPLATE.format_map({
            "__SECTION_HEADING__": section_dict['heading'],
            "__SUB_SECTION_HEADINGS__": "; ".join(section_dict['sub_headings']),
            "__SERIALIZED_REPORT__": serialized_report,
            "__ADDITIONAL_GUIDELINES__": additional_guidelines_with_figures,
            "__CONTENT_ADJECTIVE__": "with visual elements"
        })

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        ),
        HumanMessage(
            content=serialized_conversation
        ),
    ]
    response = await invoke_llm(messages, llm=llm)
    html_content = response.content
    return html_content.replace('&gt;', '>')  # Fix errors when arrows are generated incorrectly by LLM
