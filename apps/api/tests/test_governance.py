import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
import os

# Add to path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.governance.middleware import GovernanceMiddleware

app = FastAPI()
app.add_middleware(GovernanceMiddleware)

@app.get("/test")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_governance_middleware_adds_audit_header():
    response = client.get("/test")
    assert response.status_code == 200
    assert "X-KSP-Governance-Audit-Id" in response.headers
