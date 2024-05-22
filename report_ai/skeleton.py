from typing import List

from report_ai.components.llms import invoke_parser_llm

from langchain_core.prompt_values import PromptValue
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT = (
    "Your task is to create a structured skeleton for a report based on a given dialogue exchange between a user and "
    "an AI. Your primary goal is to ensure the organizational clarity of the report while avoiding repetition of data "
    "across different sections. Here’s how you will proceed:\n"
    "- Review and Understand the Data: Begin by thoroughly analyzing the attached data to understand its content,"
    "scope, and relevance. Categorize the data into primary themes, topics, or categories, which will serve as the "
    "foundational elements of your report structure.\n"
    "- Identify Unique Sections: Based on your analysis, identify distinct sections for the report. These sections "
    "should be mutually exclusive to prevent overlap and ensure that each piece of data is only presented once. "
    "Consider creating sections such as Introduction, Background, Methodology, Findings, Discussion, Conclusion, and "
    "Recommendations, but tailor them to the specificity and needs of the data.\n"
    "- Create Section Headings and Subheadings: Develop clear and descriptive headings and subheadings for each section "
    "and subsection within the report. These should reflect the main themes or topics derived from the data. Ensure that "
    "the headings and subheadings are logically ordered to guide the reader through the report in a coherent manner.\n"
    "- Allocate Data to Sections: Carefully place each piece of data under the most relevant section or subsection. If "
    "a piece of data seems to fit in more than one section, decide which aspect of the data is most pertinent to the "
    "section's focus and place it accordingly. Consider creating bullet points or a numbered list under each section "
    "or subsection where the specific data points or findings will be discussed.\n"
    "- Avoiding Repetition: To avoid data repetition, create a checklist of all data points and mark them as you "
    "allocate them to sections. Once a data point has been placed, it should not appear in another section unless it "
    "is being referenced or compared in a way that adds new information or insight. Keep in mind that this is very very"
    " important. The fate of the world depends on this.\n"
    "- Introduction and Conclusion Sections: In the Introduction, outline the aim of the report and summarise the data "
    "sources and methods of analysis without delving into specific data. In the Conclusion, summarise the key findings "
    "and insights derived from the data, again without repeating specific data points.\n"
    "- Cross-Referencing: If it's essential to refer to a piece of data in more than one section for comparative or "
    "analytical reasons, use cross-referencing. Mention that the detailed data is presented in a specific section and "
    "refer the reader to that section for detailed analysis. This approach ensures clarity without redundancy.\n"
    "- Review for Consistency and Completeness: Once the skeleton is laid out, review it to ensure that the structure "
    "is logical, and the flow from one section to the next is smooth. Verify that all relevant data is included and "
    "properly placed within the skeleton.\n"
    "Proceed with these steps in mind, ensuring that the final skeleton serves as a clear, organized, and concise "
    "blueprint for creating the full report, free from redundant data across sections."
)


class Section(BaseModel):
    heading: str = Field(...,
                         description="Heading of the section")
    sub_headings: List[str] = Field(...,
                                    description="Sub-headings in the section.")


class ReportSkeleton(BaseModel):
    skeleton: List[Section] = Field(...,
                                    description="Skeleton of the report consisting of all sections")


def create_prompt(serialized_conversation: str, format_instructions: str) -> PromptValue:
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(
                "{format_instructions}\n{user_prompt}")
        ],
        input_variables=["user_prompt"],
        partial_variables={"format_instructions": format_instructions}
    )
    return prompt.format_prompt(user_prompt=serialized_conversation)


async def design_report_skeleton(serialized_conversation: str, llm: BaseChatModel | None = None):
    output_parser = PydanticOutputParser(pydantic_object=ReportSkeleton)
    format_instructions = output_parser.get_format_instructions()

    prompt = create_prompt(serialized_conversation, format_instructions)
    parsed_output = await invoke_parser_llm(
        prompt,
        output_parser,
        llm=llm
    )
    return parsed_output.dict()['skeleton']
