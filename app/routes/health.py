from fastapi import APIRouter
from app.db import neo4j_conn, opensearch_conn

router = APIRouter()

@router.get("/healthz", tags=["Health Check"])
def health_check():
    neo4j_status = "connected" if neo4j_conn.is_healthy() else "unreachable"
    opensearch_status = "connected" if opensearch_conn.is_healthy() else "unreachable"
    status = "ok" if neo4j_status == "connected" and opensearch_status == "connected" else "error"
    return {
        "status": status,
        "neo4j": neo4j_status,
        "opensearch": opensearch_status
    }