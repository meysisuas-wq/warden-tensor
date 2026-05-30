import pytest
from src.alerts.manager import AlertManager

class TestAlertManagerIntegration:
    @pytest.mark.asyncio
    async def test_create_alert(self):
        m = AlertManager()
        alert = await m.create_alert(alert_type="intrusion", level="critical",
                                     title="Perimeter breach", camera_id="cam-001", zone="entrance", confidence=0.95)
        assert alert is not None
        assert alert["status"] == "active"

    @pytest.mark.asyncio
    async def test_acknowledge(self):
        m = AlertManager()
        alert = await m.create_alert(alert_type="motion", level="info", title="Motion", camera_id="cam-002", confidence=0.8)
        assert await m.acknowledge_alert(alert["id"], "admin") is True

    @pytest.mark.asyncio
    async def test_resolve(self):
        m = AlertManager()
        alert = await m.create_alert(alert_type="object", level="warning", title="Bag", camera_id="cam-003", confidence=0.88)
        assert await m.resolve_alert(alert["id"], "False alarm") is True

    @pytest.mark.asyncio
    async def test_cooldown(self):
        m = AlertManager()
        a1 = await m.create_alert(alert_type="motion", level="info", title="M", camera_id="c1", zone="z1", confidence=0.7)
        a2 = await m.create_alert(alert_type="motion", level="info", title="M", camera_id="c1", zone="z1", confidence=0.7)
        assert a1 is not None
        assert a2 is None

    @pytest.mark.asyncio
    async def test_filtering(self):
        m = AlertManager()
        await m.create_alert(alert_type="intrusion", level="critical", title="C", camera_id="c1", confidence=0.95)
        await m.create_alert(alert_type="motion", level="info", title="I", camera_id="c2", confidence=0.7)
        assert len(m.get_active_alerts(level="critical")) == 1
        assert len(m.get_active_alerts()) == 2
