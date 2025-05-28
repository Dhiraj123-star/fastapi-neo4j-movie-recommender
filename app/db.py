from neo4j import GraphDatabase
from dotenv import load_dotenv
from opensearchpy import OpenSearch
import os
import time
from opensearchpy.exceptions import ConnectionError as OpenSearchConnectionError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def is_healthy(self):
        try:
            self.query("RETURN 1 AS result")
            return True
        except Exception:
            return False

class OpenSearchConnection:
    def __init__(self, host, index_name, max_retries=12, initial_delay=5):
        self.index_name = index_name
        self.client = None
        self.host = host
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.connected = False

    def connect(self):
        if self.connected:
            return
        # Exponential backoff retry
        for attempt in range(self.max_retries):
            delay = self.initial_delay * (2 ** attempt)  # Exponential backoff: 5s, 10s, 20s, etc.
            try:
                self.client = OpenSearch(hosts=[self.host])
                # Verify connection with cluster health
                health = self.client.cluster.health()
                if health["status"] in ["yellow", "green"]:
                    self.connected = True
                    logger.info("Connected to OpenSearch")
                    return
                else:
                    logger.warning(f"OpenSearch cluster not ready (status: {health['status']}), retrying...")
            except OpenSearchConnectionError as e:
                logger.error(f"OpenSearch connection attempt {attempt + 1}/{self.max_retries} failed: {str(e)}")
            time.sleep(delay)
        raise Exception(f"Failed to connect to OpenSearch after {self.max_retries} attempts")

    def ensure_index(self):
        if not self.connected:
            self.connect()
        # Create index if it doesn't exist
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {
                            "movie_id": {"type": "keyword"},
                            "title": {"type": "text"}
                        }
                    }
                }
            )
            logger.info(f"Created OpenSearch index: {self.index_name}")

    def index_movie(self, movie_id: str, title: str):
        self.ensure_index()
        document = {
            "movie_id": movie_id,
            "title": title
        }
        self.client.index(index=self.index_name, body=document, id=movie_id)
        logger.info(f"Indexed movie {movie_id} in OpenSearch")

    def search_movies(self, query: str):
        self.ensure_index()
        search_body = {
            "query": {
                "match": {
                    "title": {
                        "query": query,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }
        response = self.client.search(index=self.index_name, body=search_body)
        return [
            {"movie_id": hit["_id"], "title": hit["_source"]["title"]}
            for hit in response["hits"]["hits"]
        ]

    def is_healthy(self):
        try:
            self.connect()
            self.client.cluster.health()
            return True
        except Exception:
            return False

# Fetch credentials from environment variables
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST")
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX")

neo4j_conn = Neo4jConnection(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
opensearch_conn = OpenSearchConnection(OPENSEARCH_HOST, OPENSEARCH_INDEX)