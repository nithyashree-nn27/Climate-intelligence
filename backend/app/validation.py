from typing import Any


def validate_pollution_event(
    gemini_analysis: dict[str, Any],
    environmental_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Combines citizen-image evidence with environmental signals.

    The score represents supporting evidence, not proof that
    the image itself caused or represents measured pollution.
    """

    score = 0
    reasons = []

    # --------------------------------------------------
    # 1. Gemini visual evidence
    # --------------------------------------------------

    if gemini_analysis.get("event_detected") is True:
        score += 30
        reasons.append(
            "Visual evidence is consistent with a potential pollution event."
        )

    if gemini_analysis.get("smoke_detected") is True:
        score += 20
        reasons.append(
            "Visible smoke/emission-like evidence detected."
        )

    severity = gemini_analysis.get("severity")

    if severity == "high":
        score += 15
    elif severity == "medium":
        score += 10
    elif severity == "low":
        score += 5

    # --------------------------------------------------
    # 2. Environmental evidence
    # --------------------------------------------------

    current = environmental_data.get("current", {})

    pm25 = current.get("pm2_5")
    pm10 = current.get("pm10")
    no2 = current.get("nitrogen_dioxide")

    environmental_signals = 0

    if pm25 is not None and pm25 >= 35:
        environmental_signals += 1
        score += 10
        reasons.append(
            "PM2.5 is elevated relative to the selected screening threshold."
        )

    if pm10 is not None and pm10 >= 50:
        environmental_signals += 1
        score += 10
        reasons.append(
            "PM10 is elevated relative to the selected screening threshold."
        )

    if no2 is not None and no2 >= 40:
        environmental_signals += 1
        score += 10
        reasons.append(
            "NO₂ is elevated relative to the selected screening threshold."
        )

    # --------------------------------------------------
    # 3. Limit score
    # --------------------------------------------------

    score = min(score, 100)

    # --------------------------------------------------
    # 4. Determine confidence
    # --------------------------------------------------

    if score >= 70:
        confidence = "high"
    elif score >= 45:
        confidence = "medium"
    else:
        confidence = "low"

    # --------------------------------------------------
    # 5. Evidence interpretation
    # --------------------------------------------------

    if environmental_signals > 0 and score >= 45:
        interpretation = (
            "Visual evidence and environmental signals are "
            "consistent with a potential localized pollution event."
        )

    elif score >= 45:
        interpretation = (
            "Visual evidence is consistent with a potential pollution "
            "event, but the available environmental signals do not "
            "strongly corroborate it."
        )

    else:
        interpretation = (
            "Available evidence is insufficient to strongly "
            "corroborate a localized pollution event."
        )

    # --------------------------------------------------
    # 6. Final result
    # --------------------------------------------------

    return {
        "evidence_score": score,
        "confidence": confidence,
        "environmental_signals": environmental_signals,
        "reasons": reasons,
        "interpretation": interpretation,
    }