import os
from typing import List
from json.decoder import JSONDecodeError
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type

from report_ai.common.utils import configs  # Needed to initialize ENV variables
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.messages.base import BaseMessage
from langchain.pydantic_v1 import ValidationError
from langchain.output_parsers import OutputFixingParser
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models.chat_models import BaseChatModel

openai = {
    'gpt-3.5-turbo': ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7),
    'gpt-4-turbo': ChatOpenAI(model_name='gpt-4-turbo', temperature=0.7),
    'gpt-4o': ChatOpenAI(model_name='gpt-4o', temperature=0.7)
}

anthropic = {
    'claude-3-haiku': ChatAnthropic(model='claude-3-haiku-20240307', temperature=0.7),
    'claude-3-opus': ChatAnthropic(model='claude-3-opus-20240229', temperature=0.7)
}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.2),
       retry=(retry_if_exception_type((JSONDecodeError, ValidationError))))
async def invoke_parser_llm(prompt, output_parser, llm: BaseChatModel | None):
    llm = llm or openai[os.getenv('GPT_MODEL', 'gpt-4o')]
    output = await llm.ainvoke(prompt.to_messages())
    try:
        parsed_output = output_parser.parse(output.content)
    except OutputParserException:
        fixing_parser = OutputFixingParser.from_llm(parser=output_parser, llm=llm)
        parsed_output = fixing_parser.parse(output.content)
    return parsed_output


async def invoke_llm(messages: List[BaseMessage], llm: BaseChatModel | None):
    llm = llm or openai[os.getenv('GPT_MODEL', 'gpt-4o')]
    return await llm.ainvoke(messages)


__all__ = ['openai', 'anthropic', 'invoke_parser_llm', 'invoke_llm']
