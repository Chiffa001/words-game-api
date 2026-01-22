from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.routes import healthmonitor_route
from app.services.auth_service import AuthService


def test_health_check_bypasses_auth():
    app = FastAPI(dependencies=[Depends(AuthService.validate_tg_hash)])
    app.include_router(healthmonitor_route.router)

    with TestClient(app) as client:
        response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == "I'm healthy"
