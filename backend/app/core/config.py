"""Application configuration."""

from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    app_name: str = "Payment Dispute Engine"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Server settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Database settings
    database_url: Optional[str] = None
    database_echo: bool = False
    
    # Azure settings
    azure_storage_connection_string: Optional[str] = None
    azure_service_bus_connection_string: Optional[str] = None
    
    # SLA settings (in hours)
    default_sla_hours: int = 72  # 3 days
    
    class Config:
        """Pydantic settings config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
