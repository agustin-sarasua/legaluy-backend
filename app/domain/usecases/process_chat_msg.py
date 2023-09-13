import os
import textwrap
from typing import List
from app.domain.entities.entities import (
    Conversation,
    Message,
    SearchRequest,
    SearchResponse,
)
import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy.helpers import bulk
import re
from app.infrastructure.services.openai_service import OpenAIService

MAX_CONTEXT_LENGTH = 9000


system_message = """
You are a lawyer assistant and you are helping a lawyer to analyze a case.
Always answer in spanish.
If the information is not present in the case, just answer that the information is not present.
Here is the case description:
{case_description}
"""

summarize_system_message = """
You are a lawyer assistant and you are helping a lawyer to analyze a case.
Always answer in spanish.

Summarize the following information about a case. 
If there are important details that could answer the question "{question}", include them.
Do not include the question in the summary.

Here is the infromation:
{paragraph}
"""


class ProcessChatMsgUseCase:
    def __init__(self):
        api_token = os.environ.get("OPENAI_API_KEY")
        self.openai_service = OpenAIService(api_token)

    def preprocess_text(self, text: str):
        # Remove extra blank lines
        text = re.sub(r"\n\s*\n", "\n", text)
        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)
        return text

    def summarize_sentencia_for_user_question(self, text: str, question: str):
        chunks = textwrap.wrap(text, 25000)
        # previus_summary = ""
        sumaries = list()
        for idx, chunk in enumerate(chunks):
            sys_formated = summarize_system_message.format(
                paragraph=chunk, question=question
            )
            # user_message_text = user_message.format(paragraph=chunk)
            # user_msg = Message(role="user", text=user_message_text)
            messages = self.openai_service.build_messages_from_conversation(
                sys_formated, []
            )
            # print(f"Messages chunk {idx}:", messages)
            summary = self.openai_service.get_completion_from_messages(
                messages=messages, max_tokens=1000
            )
            print(f"Summary chunk {idx}:", summary)
            # previus_summary = summary
            sumaries.append(summary)
        return "\n".join(sumaries), sumaries

    def answer_question(self, summary: str, question: str):
        sys_formated = system_message.format(case_description=summary)
        user_msg = Message(role="user", text=question)
        messages = self.openai_service.build_messages_from_conversation(
            sys_formated, [user_msg]
        )
        print(f"Messages answer question:", messages)
        answer = self.openai_service.get_completion_from_messages(
            messages=messages, max_tokens=1000
        )
        return answer

    def execute(self, conversation: Conversation) -> str:
        alltext = conversation.sentencia_model.sentencia

        alltext = self.preprocess_text(alltext)

        num_words = len(alltext.split())
        summary = alltext
        if num_words > MAX_CONTEXT_LENGTH:
            summary = self.summarize_sentencia_for_user_question(
                alltext, conversation.messages[0].text
            )

        return self.answer_question(summary, conversation.messages[0].text)
