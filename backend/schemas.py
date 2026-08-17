from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    mode: str
    timestamp: datetime


class CameraOut(BaseModel):
    camera_id: str
    name: str
    location_name: str
    latitude: float
    longitude: float
    status: str
    fps: float
    last_update: datetime
    detection_confidence: float


class TrafficCurrentOut(BaseModel):
    camera_id: str
    total_vehicles: int
    cars: int
    motorcycles: int
    buses: int
    trucks: int
    in_count: int
    out_count: int
    vehicles_per_minute: float
    avg_speed: float
    density: float
    congestion_level: float
    fps: float
    warning: str | None = None


class RiskFactor(BaseModel):
    name: str
    contribution: float


class RiskOut(BaseModel):
    camera_id: str
    location_name: str
    risk_score: float = Field(ge=0, le=100)
    risk_level: str
    confidence: float = Field(ge=0, le=100)
    trend: str
    factors: list[RiskFactor]


class OfficerOut(BaseModel):
    officer_id: str
    name: str
    station: str
    latitude: float
    longitude: float
    availability: bool
    current_assignment: str | None
    shift: str
    status: str


class OfficerRecommendationRequest(BaseModel):
    incident_id: str
    latitude: float
    longitude: float
    priority: int = 1


class OfficerCandidate(BaseModel):
    officer_id: str
    name: str
    distance_km: float
    eta_minutes: float
    status: str
    reason: str


class OfficerRecommendationOut(BaseModel):
    recommendation: OfficerCandidate | None
    alternatives: list[OfficerCandidate]
    escalation_required: bool
    message: str


class IncidentOut(BaseModel):
    incident_id: str
    camera_id: str
    location: str
    timestamp: datetime
    incident_type: str
    risk_score: float
    risk_level: str
    ai_confidence: float
    contributing_factors: dict
    recommended_officer: str | None
    selected_officer: str | None
    approval_status: str
    rejection_reason: str | None


class IncidentDecisionRequest(BaseModel):
    officer_id: str | None = None
    reason: str | None = None


class ResolveIncidentRequest(BaseModel):
    resolution_status: str
    actual_incident: bool
    actual_severity: str
    resolution_time_minutes: float
    note: str | None = None


class SimulationInput(BaseModel):
    vehicle_density: float = Field(ge=0, le=1)
    average_speed: float = Field(ge=0)
    weather: str
    congestion: float = Field(ge=0, le=1)
    abnormal_movement: bool


class DashboardSummary(BaseModel):
    total_vehicles: int
    average_speed: float
    congestion: float
    active_incidents: int
    high_risk_locations: int
    demo_mode: bool
