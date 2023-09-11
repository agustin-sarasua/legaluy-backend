from typing import List
from app.domain.entities.entities import SearchRequest, SearchResponse, SentenciaModel
import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy.helpers import bulk

host = 'search-jurisprudencia-e6bo6poynsg5wfdnqggt4xp2uu.us-east-1.es.amazonaws.com' # e.g. my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
print(credentials)
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
index_name = 'jurisprudencia'
# url = host + '/' + index + '/_search'

class SearchBJNUseCase:

    def __init__(self):
        # Create the client.
        self.client = OpenSearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            http_compress = True, # enables gzip compression for request bodies
            connection_class = RequestsHttpConnection
        )

    def execute(self, search_request: SearchRequest) -> SearchResponse:
        # Specify the index you want to search in

        # Define the search query
        search_query = {
            "query": {
                "simple_query_string": {
                    "query": search_request.text,
                    "fields": ["sentencia"]
                }
            }
        }

        # Execute the search query
        response = self.client.search(index=index_name, body=search_query, size=25)

        # print(response)
        sentencias = []
        if "hits" in response and "hits" in response["hits"]:
            hits = response["hits"]["hits"]
            total_hits = response["hits"]["total"]["value"]
            for hit in hits:
                source_data = hit["_source"]
                sentencia = SentenciaModel(**source_data)
                sentencias.append(sentencia)

            self.client.close()
            # print(hits, total_hits, sentencias)
            return SearchResponse(hits=len(hits), total_hits=total_hits, results=sentencias)
        
        self.client.close()
        return SearchResponse(hits=0, total_hits=0, results=sentencias)


