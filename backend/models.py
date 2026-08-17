from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    location_name: Mapped[str] = mapped_column(String(120))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30), default="ONLINE")
    fps: Mapped[float] = mapped_column(Float, default=20.0)
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    detection_confidence: Mapped[float] = mapped_column(Float, default=0.0)


class TrafficSnapshot(Base):
    __tablename__ = "traffic_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(50), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total_vehicles: Mapped[int] = mapped_column(Integer, default=0)
    cars: Mapped[int] = mapped_column(Integer, default=0)
    motorcycles: Mapped[int] = mapped_column(Integer, default=0)
    buses: Mapped[int] = mapped_column(Integer, default=0)
    trucks: Mapped[int] = mapped_column(Integer, default=0)
    in_count: Mapped[int] = mapped_column(Integer, default=0)
    out_count: Mapped[int] = mapped_column(Integer, default=0)
    vehicles_per_minute: Mapped[float] = mapped_column(Float, default=0.0)
    avg_speed: Mapped[float] = mapped_column(Float, default=0.0)
    density: Mapped[float] = mapped_column(Float, default=0.0)
    congestion_level: Mapped[float] = mapped_column(Float, default=0.0)


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(50), index=True)
    location_name: Mapped[str] = mapped_column(String(120))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    risk_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(20))
    confidence: Mapped[float] = mapped_column(Float)
    factors: Mapped[dict] = mapped_column(JSON)
    trend: Mapped[str] = mapped_column(String(20), default="STABLE")


class Officer(Base):
    __tablename__ = "officers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    officer_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    station: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    current_assignment: Mapped[str | None] = mapped_column(String(120), nullable=True)
    shift: Mapped[str] = mapped_column(String(20), default="DAY")
    status: Mapped[str] = mapped_column(String(20), default="AVAILABLE")


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    camera_id: Mapped[str] = mapped_column(String(50), index=True)
    location: Mapped[str] = mapped_column(String(120))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    incident_type: Mapped[str] = mapped_column(String(60), default="TRAFFIC_RISK")
    risk_score: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(20))
    ai_confidence: Mapped[float] = mapped_column(Float)
    contributing_factors: Mapped[dict] = mapped_column(JSON)
    recommended_officer: Mapped[str | None] = mapped_column(String(100), nullable=True)
    selected_officer: Mapped[str | None] = mapped_column(String(100), nullable=True)
    approval_status: Mapped[str] = mapped_column(String(20), default="NEW")
    acknowledgement_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deployment_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resolution_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resolution_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    officer_id: Mapped[int] = mapped_column(ForeignKey("officers.id"))
    eta_minutes: Mapped[float] = mapped_column(Float)
    distance_km: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident")
    officer = relationship("Officer")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"))
    actual_incident: Mapped[bool] = mapped_column(Boolean)
    actual_severity: Mapped[str] = mapped_column(String(20))
    resolution_time_minutes: Mapped[float] = mapped_column(Float)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident")
