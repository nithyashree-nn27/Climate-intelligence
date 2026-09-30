# 🌍 ClimatePulse
### AI-Powered Pollution Intelligence & Early Warning Platform

ClimatePulse is an AI-powered environmental intelligence platform designed to detect, analyze, predict, and communicate neighborhood-level pollution risks.

The platform combines:

- 📷 Citizen-submitted images
- 🤖 Gemini multimodal AI analysis
- 🌫️ Real-time and forecast environmental data
- 📊 Evidence-based pollution scoring
- 📈 24-hour pollution forecasting
- 📍 Pollution hotspot detection
- 🚨 Automated municipal alerts
- 🗺️ Interactive hotspot visualization
- 🏛️ Municipal command-center dashboard

The goal is to move from **reactive pollution reporting** to **proactive, evidence-based environmental monitoring**.

---

# 🎯 Problem Statement

Urban pollution can change significantly between neighborhoods and over short periods of time.

Traditional monitoring systems may rely on a limited number of fixed monitoring stations. This can make it difficult to identify localized pollution events such as:

- Dense smoke
- Industrial emissions
- Traffic-related pollution
- Construction dust
- Waste-burning indicators
- Temporary pollution spikes

Citizen reports provide valuable local observations, but a photograph alone does not provide enough information to determine the severity of an environmental event.

ClimatePulse addresses this by combining **visual evidence + environmental measurements + temporal forecasting**.

---

# 💡 Solution

ClimatePulse follows an evidence-fusion approach.

A citizen can submit a photograph along with location information.

The system then:

1. Receives the citizen report.
2. Sends the image to Gemini for visual analysis.
3. Identifies pollution-related visual evidence.
4. Retrieves environmental conditions for the reported coordinates.
5. Combines citizen evidence with environmental measurements.
6. Calculates a pollution/hotspot risk score.
7. Generates a 24-hour pollution forecast.
8. Determines whether a municipal alert should be generated.
9. Displays the result on the ClimatePulse dashboard.

This creates a pipeline from:

**Citizen Observation → AI Analysis → Environmental Evidence → Risk Assessment → Forecast → Municipal Action**

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │       CITIZEN           │
                    │                         │
                    │  Upload Image +         │
                    │  Location / Report      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    │                         │
                    │   Report Processing     │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
     ┌─────────────────────┐          ┌─────────────────────┐
     │   Gemini Vision AI  │          │ Environmental Data  │
     │                     │          │                     │
     │ Smoke Detection     │          │ PM2.5               │
     │ Event Detection     │          │ PM10                │
     │ Source Classification│         │ NO₂                 │
     │ Severity Assessment │          │ O₃                  │
     └──────────┬──────────┘          │ Temperature         │
                │                     │ Wind                 │
                │                     └──────────┬──────────┘
                │                                │
                └──────────────┬─────────────────┘
                               ▼
                    ┌─────────────────────────┐
                    │    Evidence Fusion      │
                    │                         │
                    │ Citizen + AI +          │
                    │ Environmental Evidence  │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
     ┌─────────────────────┐          ┌─────────────────────┐
     │  Hotspot Detection  │          │  24-Hour Forecast   │
     │                     │          │                     │
     │ Pollution Score     │          │ PM2.5 Trend         │
     │ Risk Level          │          │ Peak Risk           │
     │ Location            │          │ Forecast Risk       │
     └──────────┬──────────┘          └──────────┬──────────┘
                │                                │
                └──────────────┬─────────────────┘
                               ▼
                    ┌─────────────────────────┐
                    │   Municipal Alert       │
                    │                         │
                    │ Priority                │
                    │ Recommended Action      │
                    │ Risk Summary            │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   ClimatePulse UI       │
                    │                         │
                    │ Map + Hotspots           │
                    │ Forecast Chart           │
                    │ Environmental Data       │
                    │ AI Analysis              │
                    │ Command Center           │
                    └─────────────────────────┘
```

---

# 🔄 End-to-End Workflow

## 1. Citizen Report

The user submits an environmental image through the ClimatePulse frontend.

The report can contain:

- Image
- Latitude
- Longitude
- Timestamp
- Citizen-provided information

The frontend sends the report to the FastAPI backend.

---

## 2. AI Image Analysis

The backend processes the submitted image using Gemini's multimodal capabilities.

Gemini can analyze images directly and return structured information.

The current analysis can identify information such as:

```text
event_detected
smoke_detected
possible_source
severity
relevance
visual_evidence
```

Example conceptual output:

```json
{
  "event_detected": true,
  "smoke_detected": true,
  "possible_source": "industrial",
  "severity": "high",
  "relevance": "high",
  "visual_evidence": [
    "dense smoke plume",
    "visible atmospheric haze"
  ]
}
```

This converts an unstructured image into structured environmental evidence.

---

# 🌫️ Environmental Intelligence

ClimatePulse retrieves environmental information using the Open-Meteo APIs.

The current implementation uses:

- PM2.5
- PM10
- Nitrogen Dioxide (NO₂)
- Ozone (O₃)
- Temperature
- Wind Speed
- Wind Direction

Open-Meteo's Air Quality API provides current and hourly air-quality variables and uses CAMS atmospheric-composition forecasts as a data source.

The backend sends:

```text
latitude
longitude
```

and retrieves environmental conditions for that location.

---

# 📊 Evidence Fusion

A key part of ClimatePulse is that the system does not depend only on the citizen image or only on environmental measurements.

Instead, it combines multiple evidence sources.

```text
Citizen Report
      +
Gemini Visual Evidence
      +
Environmental Conditions
      +
24-Hour Pollution Forecast
      ↓
Evidence Fusion
      ↓
Pollution Risk
```

This allows the platform to distinguish between:

- A visual report with weak environmental evidence
- A pollution spike with no citizen report
- A citizen report supported by elevated pollutant values
- A location where current pollution is moderate but the forecast indicates increasing risk

---

# 📍 Pollution Hotspot Detection

The `hotspots.py` module evaluates multiple locations.

Each location is evaluated using available environmental and citizen-report evidence.

The system produces information such as:

```text
Location
Pollution Score
Risk Level
Environmental Evidence
Citizen Evidence
Forecast Information
```

The frontend then displays these locations as pollution hotspots on the interactive map.

The system currently supports arbitrary latitude/longitude locations, rather than being restricted to a single city.

---

# 📈 24-Hour Pollution Forecast

ClimatePulse analyzes hourly pollution data to estimate near-term pollution risk.

The current forecast module evaluates:

- PM2.5
- PM10
- NO₂

The forecast produces:

```text
Forecast Risk Score
Forecast Risk Level
Peak Forecast Time
Peak PM2.5
PM2.5 Trend
Reasons
```

The current risk classification is:

```text
High     → score >= 70
Medium   → score >= 40
Low      → score < 40
```

The frontend displays the PM2.5 forecast as a 24-hour line chart.

Example concept:

```text
PM2.5
  │
45│                 ●
  │              ●     ●
35│          ●
  │       ●
25│   ●
  │
  └────────────────────────
     Now       +12h     +24h
```

The chart is implemented using native SVG rather than depending on an external charting library.

---

# 🚨 Automated Municipal Alerts

ClimatePulse includes an automated municipal alert layer.

The alert engine considers both:

```text
Current Risk
      +
Forecast Risk
      ↓
Alert Priority
```

Alert levels:

```text
HIGH
MEDIUM
LOW
```

### High Risk

The system recommends prioritizing inspection of the reported area and reviewing possible local pollution sources.

### Medium Risk

The system recommends monitoring the area and considering field inspection if additional evidence is received.

### Low Risk

The system continues environmental monitoring without indicating immediate municipal action.

The generated alert contains:

```text
Alert Status
Priority
Location
Pollution Score
Current Risk
Forecast Risk
Forecast Score
Recommended Action
Alert Message
```

---

# Municipal Command Center

The frontend contains a Municipal Command Center designed to provide a quick operational view.

It displays:

- Overall alert status
- Highest-risk location
- Current risk
- Forecast risk
- Pollution score
- Recommended municipal action

The dashboard selects the highest-scoring detected hotspot to provide a simple command-center summary.

---

# Interactive Hotspot Map

The frontend visualizes detected pollution locations on a map.

The map allows the user to understand:

- Where pollution risk is concentrated
- Which locations have higher scores
- Which locations require attention
- How different locations compare geographically

The platform is designed to support neighborhood-level environmental intelligence rather than only city-level averages.

---

# Frontend

The current frontend is implemented as:

```text
frontend/
└── index.html
```

The dashboard contains sections for:

- ClimatePulse overview
- Pollution hotspot map
- Environmental conditions
- AI image analysis
- Evidence fusion
- Pollution forecast
- Municipal alert
- Municipal Command Center

The frontend communicates with the FastAPI backend using HTTP requests.

---

# ⚙️ Backend

The backend is implemented using **FastAPI**.

Current structure:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── reports.py
│   ├── gemini_vision.py
│   ├── environment.py
│   ├── validation.py
│   ├── forecast.py
│   ├── hotspots.py
│   ├── image_provenance.py
│   └── alerts.py
│
├── tests/
│   └── test_image_provenance.py
│
└── venv/
```

---

# Backend Module Responsibilities

## `main.py`

Main FastAPI application.

Responsibilities:

- Start the API
- Configure CORS
- Serve the frontend root
- Provide health check
- Provide environmental endpoint
- Provide hotspot endpoint
- Register report routes

---

## `reports.py`

Handles citizen environmental reports.

The report workflow connects:

```text
Image
 ↓
Gemini Analysis
 ↓
Environmental Data
 ↓
Validation / Evidence Fusion
 ↓
Forecast
 ↓
Hotspot
 ↓
Municipal Alert
```

---

## `gemini_vision.py`

Responsible for AI-based visual analysis.

It sends environmental images to Gemini and extracts structured environmental evidence.

Gemini supports multimodal image understanding and structured output schemas, making it suitable for converting visual input into predictable application data.

---

## `environment.py`

Responsible for retrieving environmental data.

Current external data source:

```text
Open-Meteo Air Quality API
Open-Meteo Weather API
```

The module retrieves:

```text
PM2.5
PM10
NO₂
O₃
Temperature
Wind Speed
Wind Direction
```

It also retrieves hourly pollution information used by the forecast module.

---

## `forecast.py`

Processes hourly environmental data and calculates:

```text
Risk Score
Risk Level
Peak Pollution Period
PM2.5 Change
Forecast Reasons
```

---

## `hotspots.py`

Detects pollution hotspots across requested locations.

It combines environmental data with available citizen-report evidence.

---

## `alerts.py`

Generates municipal alerts from current and forecast risk.

The alert engine determines:

```text
Priority
Recipient
Location
Current Risk
Forecast Risk
Recommended Action
```

---

## `validation.py`

Provides validation logic for incoming environmental/report information.

It helps keep the processing pipeline structured before evidence is passed into subsequent modules.

---

## `image_provenance.py`

Provides image-provenance related information.

### Current limitation

The current implementation should **not be interpreted as a live Google SynthID verification service**.

If a report indicates that no watermark was detected, this should be treated as provenance information rather than proof that an image is authentic or AI-generated.

---

# 🔌 API Endpoints

## Health Check

```http
GET /health
```

Example:

```json
{
  "status": "healthy"
}
```

---

## Current Environment

```http
GET /environment/current?latitude=12.9716&longitude=77.5946
```

Returns environmental conditions and forecast data for the requested coordinates.

---

## Hotspot Detection

```http
POST /hotspots
```

Accepts a list of locations and evaluates their pollution risk.

Conceptual request:

```json
[
  {
    "latitude": 12.9716,
    "longitude": 77.5946
  }
]
```

---

## Citizen Report

The report endpoint is registered through:

```python
app.include_router(reports_router)
```

It handles the integrated report-processing workflow.

---

## API Documentation

FastAPI automatically provides interactive API documentation.

When running locally:

```text
http://127.0.0.1:8000/docs
```

---

# Technology Stack

## Frontend

- HTML
- CSS
- JavaScript
- Interactive map
- SVG-based pollution forecast visualization

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- Requests

## AI

- Google Gemini
- Gemini multimodal image understanding
- Structured AI output

## Environmental Data

- Open-Meteo Air Quality API
- Open-Meteo Weather API
- CAMS atmospheric-composition forecast data

## Development

- Git
- GitHub
- Python virtual environment
- REST APIs

---

# Local Setup

## Prerequisites

Install:

- Python 3.10+
- Git
- A Gemini API key for AI image analysis

---

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Climate-intelligence
```

---

## 2. Create the Python Virtual Environment

From the backend directory:

```bash
cd backend
python -m venv venv
```

---

## 3. Activate the Virtual Environment

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell activation is unavailable, the project can also use the Python executable directly:

```powershell
.\venv\Scripts\python.exe
```

---

## 4. Install Dependencies

Install the required packages:

```bash
pip install fastapi uvicorn python-multipart python-dotenv google-genai pydantic requests
```

---

# Environment Variables

Create a `.env` file inside the backend directory if your Gemini configuration requires it.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

### Important

Never commit your actual API key to GitHub.

Add `.env` to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# Run the Backend

From:

```text
D:\Climate-intelligence\backend
```

run:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Run the Frontend

From the frontend directory:

```text
D:\Climate-intelligence\frontend
```

run:

```powershell
..\backend\venv\Scripts\python.exe -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

The frontend communicates with the FastAPI backend running on port `8000`.

Because different ports are different browser origins, CORS is configured in FastAPI to permit frontend-to-backend communication during development.

---

# Testing

The project contains automated tests under:

```text
backend/tests/
```

Run the tests using:

```powershell
.\venv\Scripts\python.exe -m pytest
```

The implemented test suite has been used to validate the image-provenance functionality and the overall backend changes made during development.

---

# Example Local Workflow

Once both servers are running:

### Step 1

Open:

```text
http://127.0.0.1:5500
```

### Step 2

Submit an environmental image.

### Step 3

The frontend sends the report to FastAPI.

### Step 4

Gemini analyzes the image.

### Step 5

The backend retrieves environmental conditions.

### Step 6

Evidence is combined.

### Step 7

The hotspot risk is calculated.

### Step 8

The 24-hour pollution forecast is generated.

### Step 9

The municipal alert engine determines the alert priority.

### Step 10

The frontend displays:

```text
AI Analysis
     +
Environmental Conditions
     +
Evidence Fusion
     +
Pollution Forecast
     +
Hotspot Risk
     +
Municipal Alert
```

---

# Example Data Flow

```text
User uploads image
        │
        ▼
FastAPI / Report API
        │
        ▼
Gemini Vision
        │
        ├── Smoke detected?
        ├── Event detected?
        ├── Possible source?
        └── Severity?
        │
        ▼
Environmental API
        │
        ├── PM2.5
        ├── PM10
        ├── NO₂
        ├── O₃
        ├── Temperature
        └── Wind
        │
        ▼
Evidence Fusion
        │
        ▼
Pollution Score
        │
        ├───────────────┐
        ▼               ▼
Hotspot Detection   24h Forecast
        │               │
        └───────┬───────┘
                ▼
        Municipal Alert
                │
                ▼
        ClimatePulse UI
```

---

# Why Evidence Fusion?

A single data source can be incomplete.

For example:

```text
Image only
    ↓
Visual evidence but limited environmental context
```

or:

```text
Sensor/environmental data only
    ↓
Pollution measurement but limited information about the local event
```

ClimatePulse combines both:

```text
Visual Evidence
       +
Environmental Evidence
       +
Temporal Forecast
       ↓
More contextualized pollution-risk assessment
```

This approach is intended to support better prioritization of areas requiring environmental attention.

---

# Future Extensions

The architecture can be extended with additional environmental data sources.

Potential future integrations include:

- Satellite-derived pollution observations
- Sentinel-5P data
- More weather variables
- Historical pollution datasets
- Traffic data
- Industrial-zone information
- Citizen sensor networks
- Geospatial clustering
- Machine-learning forecasting models
- Municipality notification integrations
- Long-term pollution trend analysis

These are extensions of the current architecture and should not be interpreted as currently active integrations unless enabled in the deployed system.

---

# Responsible AI & Data Considerations

ClimatePulse treats AI analysis as an evidence-generation component rather than an absolute ground truth.

AI predictions and visual classifications should be interpreted alongside environmental measurements.

The platform is designed to support municipal decision-making rather than automatically making enforcement decisions.

Potential future improvements include:

- Confidence calibration
- Human review workflows
- False-positive monitoring
- Historical model evaluation
- Explainable risk scoring
- Data-quality validation
- Image provenance verification

---

# Current Limitations

The current prototype has several limitations:

1. Environmental data depends on the availability and resolution of the external API.
2. AI visual analysis depends on Gemini availability and API quotas.
3. The current forecast logic is a risk-scoring approach rather than a trained long-term forecasting model.
4. Image provenance is not equivalent to verified SynthID detection.
5. Municipal alerts are generated as prototype recommendations and are not directly connected to a municipal authority system.
6. The current prototype uses external environmental APIs rather than a dedicated physical sensor network.
7. Historical model evaluation and large-scale production validation are future improvements.

---

# Vision

ClimatePulse aims to create a scalable environmental intelligence layer that connects:

```text
Citizens
   ↓
AI
   ↓
Environmental Data
   ↓
Predictive Intelligence
   ↓
Municipal Authorities
   ↓
Faster Environmental Response
```

The long-term vision is to enable cities to identify emerging pollution hotspots earlier, understand the evidence behind them, and prioritize environmental monitoring and response.

---

# Project

**Project:** ClimatePulse  
**Theme:** Clean Air & Clear Streets / Environmental Intelligence  
**Category:** AI for Communities  
**Core Technologies:** Gemini + FastAPI + Open-Meteo + JavaScript  
**Platform:** Web Application

---

# Quick Start

```bash
# Clone
git clone <YOUR_REPOSITORY_URL>

# Enter project
cd Climate-intelligence

# Backend
cd backend

# Create environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn python-multipart python-dotenv google-genai pydantic requests

# Run backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

In another terminal:

```bash
cd Climate-intelligence\frontend

..\backend\venv\Scripts\python.exe -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

##  References

- Google Gemini API — Image Understanding
- Google Gemini API — Structured Outputs
- Open-Meteo Air Quality API
- FastAPI CORS Documentation
- FastAPI Static Files Documentation
