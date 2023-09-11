import os
import textwrap
from typing import List
from app.domain.entities.entities import Conversation, SearchRequest, SearchResponse
import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy.helpers import bulk

from app.infrastructure.services.openai_service import OpenAIService



system_message = """
You are a lawyer assistant and you are helping a lawyer to analyze a case.
Always answer in spanish.
If the information is not present in the case, just answer that the information is not present.
Here is part of the case description:
{case_description}
"""

class ProcessChatMsgUseCase:

    def __init__(self):
        api_token = os.environ.get("OPENAI_API_KEY")
        self.openai_service = OpenAIService(api_token)

    def execute(self, conversation: Conversation) -> str:
        
        alltext = conversation.sentencia_model.sentencia
        chunks = textwrap.wrap(alltext, 2000)
        result = list()
        count = 0
        chunk_answers = list()
        for chunk in chunks:
            count = count + 1
            sys_formated = system_message.format(case_description=chunk)
            # prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
            # summary = gpt3_completion(prompt)
            # print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
            # result.append(summary)

        sys_formated = system_message.format(case_description=conversation.sentencia_model.sentencia)
        chat_input = OpenAIService.build_messages_from_conversation(sys_formated, conversation.messages)
        print(chat_input)
        assistant_response = self.openai_service.get_completion_from_messages(chat_input)

        return assistant_response


