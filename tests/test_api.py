import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestHealth:
    async def test_health(self, client: AsyncClient):
        r = await client.get("/health")
        assert r.status_code == 200
        assert r.json()["service"] == "warden-tensor"

@pytest.mark.asyncio
class TestCameras:
    async def test_register_validation(self, client: AsyncClient):
        r = await client.post("/api/v1/cameras", json={})
        assert r.status_code == 422

    async def test_list(self, client: AsyncClient):
        r = await client.get("/api/v1/cameras")
        assert r.status_code == 501

@pytest.mark.asyncio
class TestDetections:
    async def test_list(self, client: AsyncClient):
        r = await client.get("/api/v1/detections")
        assert r.status_code == 501

@pytest.mark.asyncio
class TestAlerts:
    async def test_list(self, client: AsyncClient):
        r = await client.get("/api/v1/alerts")
        assert r.status_code == 501

@pytest.mark.asyncio
class TestNetwork:
    async def test_events(self, client: AsyncClient):
        r = await client.get("/api/v1/network/events")
        assert r.status_code == 501
    async def test_anomalies(self, client: AsyncClient):
        r = await client.get("/api/v1/network/anomalies")
        assert r.status_code == 501
