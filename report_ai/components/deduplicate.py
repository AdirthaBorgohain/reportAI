from report_ai.components.llms import invoke_llm
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

SYSTEM_PROMPT = (
    "Your task is to streamline TEXT2, removing any overlap with TEXT1 while maintaining the integrity and coherence "
    "of the content. Return only the revised TEXT2. If there's no overlap between TEXT1 and TEXT2, return TEXT2 "
    "unchanged.\n"
    "Make sure you strictly follow the guidelines below:\n"
    "- **Initial Reading**: Carefully read through both TEXT1 and TEXT2. Pay attention to all details, including text, "
    "figures, tables, and codes.\n"
    "- **Identify Duplications**: Locate any duplicated or very similar content in TEXT2 that appears in TEXT1, "
    "including repeated sentences, paraphrased ideas, figures, tables, and code sections.\n"
    "- **Edit to Remove Duplications**:\n"
    "   - **Rephrase**: Change the wording of sentences in TEXT2 that convey the same ideas as in TEXT1, ensuring the "
    "original meaning is still clear.\n"
    "   - **Remove Redundancies**: Eliminate parts of TEXT2 that are repetitive and don't add value.\n"
    "   - **Adjust Figures/Tables**: If TEXT2 includes identical figures or tables as TEXT1, alter or omit them if "
    "they don't contribute new insights.\n"
    "- **Ensure Mermaid Figure Standardization**: Take care to keep all mermaid diagram codes within a "
    "<div class='mermaid'> HTML element. It needs to have the standardized tag and class.\n"
    "- **Ensure Coherence**: Check that TEXT2 flows logically after edits. Information should progress smoothly "
    "without abrupt changes.\n"
    "- **Avoid Empty Sections**: Verify that there are no empty or nonsensical sections in TEXT2 after making edits.\n"
    "- **Avoid Unnecessary Additions**: Do not insert new sections like 'Final Thoughts' or 'Conclusion' unless they "
    "were already in TEXT2.\n"
    "- **Final Check**: Review TEXT2 one last time to ensure all duplications have been removed and the text remains "
    "clear and purposeful. It is important that you do not explicitly mention the words 'TEXT1' or 'TEXT2' anywhere in "
    "your revised TEXT2."
)
USER_PROMPT_TEMPLATE = "### TEXT1 ###\n{__TEXT1__}\n\n---------------\n\n ### TEXT2 ###\n{__TEXT2__}"


async def deduplicate_section(section_content: str, serialized_report: str, llm: BaseChatModel | None = None):
    USER_PROMPT = USER_PROMPT_TEMPLATE.format_map({
        '__TEXT1__': serialized_report,
        '__TEXT2__': section_content
    })

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        ),
        HumanMessage(
            content=USER_PROMPT
        ),
    ]
    response = await invoke_llm(messages, llm=llm)
    return response.content
