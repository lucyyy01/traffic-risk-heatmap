from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI Traffic Risk & Police Deployment"
    backend_port: int = 8000
    frontend_port: int = 5173
    database_url: str = "sqlite:///./backend/traffic_risk.db"
    model_path: str = "backend/models/yolo11n.pt"
    confidence_threshold: float = 0.35
    demo_mode: bool = True
    allowed_origins: str = "http://localhost:5173"
    api_key: str = "demo-control-room-key"
    default_fps: int = 20
    frame_skip: int = 2
    abnormal_persistence_seconds: int = 5
    risk_low_max: int = 30
    risk_moderate_max: int = 60
    risk_high_max: int = 80


settings = Settings()
