import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

class OpenSearchQuery:
    def __init__(self, region, service, endpoint, index_name):
        self.region = region
        self.service = service
        self.endpoint = endpoint
        self.index_name = index_name

        self.credentials = boto3.Session().get_credentials()
        self.aws_auth = AWS4Auth(
            self.credentials.access_key,
            self.credentials.secret_key,
            self.region,
            self.service,
            session_token=self.credentials.token,
        )

        self.es = Elasticsearch(
            hosts=[{"host": self.endpoint, "port": 443}],
            http_auth=self.aws_auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

    def query(self, search_query):
        try:
            response = self.es.search(index=self.index_name, body=search_query)
            return response["hits"]["hits"]
        except Exception as e:
            print(f"Error executing OpenSearch query: {str(e)}")
            return []

if __name__ == "__main__":
    region = "your-aws-region"
    service = "es"
    endpoint = "your-opensearch-endpoint-url"
    index_name = "your-opensearch-index-name"
    
    # Initialize the OpenSearchQuery object
    opensearch_query = OpenSearchQuery(region, service, endpoint, index_name)
    
    # Example search query
    search_query = {
        "query": {
            "match": {
                "field_name": "search_keyword"
            }
        }
    }
    
    # Execute the query and print the results
    results = opensearch_query.query(search_query)
    print(results)
