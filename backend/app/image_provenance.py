import os
from typing import Any


PROVENANCE_LABELS = {
    "google_ai_watermark_detected": "Google AI-generated/edited provenance detected",
    "google_ai_watermark_not_detected": "No Google AI watermark detected",
    "provenance_unknown": "Image provenance could not be verified",
    "demo_provenance_result": "Demo provenance result",
}

LIMITATIONS = (
    "This prototype does not have live Google SynthID verification. Absence of "
    "verification does not establish that the image was created by a human."
)


def _demo_mode_enabled() -> bool:
    value = os.getenv("CLIMATEPULSE_DEMO_PROVENANCE", "").strip().lower()
    return value in {"1", "true", "yes", "demo"}


def check_image_provenance(image_bytes: bytes, mime_type: str) -> dict[str, Any]:
    """
    Return a structured image-provenance assessment.

    This demo intentionally avoids claiming definitive AI generation from visual
    analysis alone. We only surface a concrete Google AI watermark result when a
    live detection pipeline is available; otherwise we return a careful non-
    detection or unknown result.
    """
    if not image_bytes:
        return {
            "status": "provenance_unknown",
            "label": PROVENANCE_LABELS["provenance_unknown"],
            "confidence": "low",
            "method": "Unavailable",
            "limitations": LIMITATIONS,
        }

    if mime_type and not mime_type.startswith("image/"):
        return {
            "status": "provenance_unknown",
            "label": PROVENANCE_LABELS["provenance_unknown"],
            "confidence": "low",
            "method": "Unavailable",
            "limitations": LIMITATIONS,
        }

    if _demo_mode_enabled():
        return {
            "status": "demo_provenance_result",
            "label": PROVENANCE_LABELS["demo_provenance_result"],
            "confidence": "high",
            "method": "Demo mode",
            "limitations": (
                "This is a demo-only provenance result and is not a live SynthID "
                "inspection. The prototype does not have live Google SynthID verification; "
                "absence of verification does not establish human origin."
            ),
        }

    return {
        "status": "provenance_unknown",
        "label": PROVENANCE_LABELS["provenance_unknown"],
        "confidence": "low",
        "method": "Unavailable",
        "limitations": LIMITATIONS,
    }
