import base64
import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


load_dotenv()


class PollutionAnalysis(BaseModel):
    event_detected: bool = Field(
        description="Whether the image contains visual evidence consistent "
                    "with a possible environmental event."
    )

    smoke_detected: bool = Field(
        description="Whether visible smoke or a smoke-like plume is present."
    )

    possible_source: Literal[
        "industrial",
        "vehicle",
        "open_burning",
        "dust",
        "construction",
        "unknown"
    ]

    severity: Literal[
        "low",
        "medium",
        "high",
        "unclear"
    ]

    relevance: Literal[
        "low",
        "medium",
        "high"
    ]

    evidence: str = Field(
        description="Brief description of the visual evidence observed."
    )


api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def analyze_pollution_image(
    image_bytes: bytes,
    mime_type: str,
    description: str = ""
) -> PollutionAnalysis:

    if client is None:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = f"""
You are an environmental observation assistant for ClimatePulse,
an AI-powered pollution intelligence platform designed for India.

Analyze the submitted citizen image.

Your task is to identify ONLY visual evidence that may be
consistent with a pollution-related environmental event.

Important rules:

1. Do not claim that the image proves actual air pollution.
2. Do not invent AQI, PM2.5, weather, or sensor measurements.
3. Base the analysis only on visible evidence.
4. If the pollution source cannot be determined, use "unknown".
5. If the image is unclear, reflect uncertainty using the severity
   or relevance fields.
6. Distinguish visible smoke/haze/dust from confirmed pollution.

Citizen description:
{description}
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image",
                "data": image_base64,
                "mime_type": mime_type
            }
        ],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": PollutionAnalysis.model_json_schema()
        }
    )

    return PollutionAnalysis.model_validate_json(
        interaction.output_text
    )