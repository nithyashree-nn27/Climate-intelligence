from pathlib import Path
import struct
import sys
import zlib

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.image_provenance import check_image_provenance
from app.main import app


def _one_pixel_png():
    def chunk(chunk_type, data):
        return (
            struct.pack(">I", len(data))
            + chunk_type
            + data
            + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00"))
        + chunk(b"IEND", b"")
    )


def _assert_provenance_unknown(result):
    assert result["status"] == "provenance_unknown"
    assert result["label"] == "Image provenance could not be verified"
    assert result["confidence"] == "low"
    assert result["method"] == "Unavailable"
    assert "does not establish that the image was created by a human" in result["limitations"]


def test_check_image_provenance_normal_image_without_live_detector(monkeypatch):
    monkeypatch.delenv("CLIMATEPULSE_DEMO_PROVENANCE", raising=False)

    result = check_image_provenance(_one_pixel_png(), "image/png")

    _assert_provenance_unknown(result)


def test_check_image_provenance_empty_image_bytes():
    result = check_image_provenance(b"", "image/jpeg")

    _assert_provenance_unknown(result)


def test_check_image_provenance_invalid_mime_type():
    result = check_image_provenance(b"sample-bytes", "text/plain")

    _assert_provenance_unknown(result)


def test_check_image_provenance_demo_mode(monkeypatch):
    monkeypatch.setenv("CLIMATEPULSE_DEMO_PROVENANCE", "true")

    result = check_image_provenance(b"sample-bytes", "image/jpeg")

    assert result["status"] == "demo_provenance_result"
    assert result["label"] == "Demo provenance result"


def test_report_endpoint_handles_gemini_failure(monkeypatch):
    monkeypatch.delenv("CLIMATEPULSE_DEMO_PROVENANCE", raising=False)
    monkeypatch.setattr(
        "app.reports.analyze_pollution_image",
        lambda **kwargs: (_ for _ in ()).throw(RuntimeError("quota exceeded")),
    )
    monkeypatch.setattr(
        "app.reports.get_current_air_quality",
        lambda **kwargs: {
            "source": "Open-Meteo / CAMS Global",
            "current": {
                "pm2_5": 60,
                "pm10": 75,
                "nitrogen_dioxide": 50,
            },
            "current_units": {
                "pm2_5": "µg/m³",
                "pm10": "µg/m³",
                "nitrogen_dioxide": "µg/m³",
            },
            "forecast_24h": {
                "time": ["2025-01-01T00:00", "2025-01-01T01:00"],
                "pm2_5": [30, 80],
                "pm10": [60, 100],
                "nitrogen_dioxide": [30, 50],
            },
        },
    )
    monkeypatch.setattr(
        "app.hotspots.get_current_air_quality",
        lambda **kwargs: {
            "source": "Open-Meteo / CAMS Global",
            "current": {
                "pm2_5": 60,
                "pm10": 75,
                "nitrogen_dioxide": 50,
            },
            "current_units": {
                "pm2_5": "µg/m³",
                "pm10": "µg/m³",
                "nitrogen_dioxide": "µg/m³",
            },
            "forecast_24h": {
                "time": ["2025-01-01T00:00", "2025-01-01T01:00"],
                "pm2_5": [30, 80],
                "pm10": [60, 100],
                "nitrogen_dioxide": [30, 50],
            },
        },
    )

    client = TestClient(app)
    response = client.post(
        "/reports/",
        files={"image": ("test.jpg", b"not-a-real-image", "image/jpeg")},
        data={"latitude": "13.0", "longitude": "77.5", "description": "Smoke haze visible."},
    )

    assert response.status_code == 200
    payload = response.json()
    _assert_provenance_unknown(payload["image_provenance"])
    assert payload["gemini_analysis"]["event_detected"] is False
    assert payload["status"] == "validated"
