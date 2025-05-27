from fastapi import APIRouter
from app.db import neo4j_conn

router = APIRouter()

@router.get("/healthz", tags=["Health Check"])
def health_check():
    if neo4j_conn.is_healthy():
        return {"status": "ok", "neo4j": "connected"}
    return {"status": "error", "neo4j": "unreachable"}