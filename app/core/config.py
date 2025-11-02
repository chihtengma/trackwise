"""
Application configuration settings.

This module uses Pydantic Settings to manage environment variables
and application configuration in a type-safe way.

IMPORTANT: Copy .env.example to .env and configure your values!
"""

from typing import List, Optional
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Values are loaded in this priority order:
    1. Environment variables (highest priority)\
    2. .env file
    3. Default values in this class (lowest priority)
    """

    # ==================== Application Settings ====================
    APP_NAME: str = Field(
        default="TrackWise Transit AI Assistant",
        description="Application name",
    )
    APP_VERSION: str = Field(
        default="0.1.0",
        description="Application version",
    )
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode (False for production)",
    )
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, staging, or production",
    )

    # ==================== Server Settings ====================
    HOST: str = Field(default="0.0.0.0", description="Server host address")
    PORT: int = Field(default=8000, description="Server port")

    # ==================== Database Settings ====================
    DATABASE_URL: str = Field(
        ...,  # Must be set in .env or environment
        description="PostgreSQL database connection URL. REQUIRED in .env!",
    )
    DATABASE_ECHO: bool = Field(
        default=False,
        description=(
            "Enable SQLAlchemy query logging. "
            "True for development, False for production"
        ),
    )

    # ==================== Cache Settings ====================
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL for caching",
    )

    # ==================== Scheduler Settings ====================
    ENABLE_SCHEDULER: bool = Field(
        default=True, description="Enable APScheduler for background tasks"
    )
    MTA_REFRESH_INTERVAL_SECONDS: int = Field(
        default=60, description="Interval for MTA data refresh (seconds)"
    )
    CACHE_WARM_INTERVAL_MINUTES: int = Field(
        default=5, description="Interval for cache warming (minutes)"
    )

    # ==================== Security Settings ====================
    SECRET_KEY: str = Field(
        ...,  # Required! Must be set in .env
        min_length=32,
        description=(
            "Secret key for JWT tokens. REQUIRED in .env! "
            "Generate with: openssl rand -hex 32"
        ),
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm (HS256, RS256, etc.)",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="JWT token expiration time in minutes"
    )

    # ==================== MTA Subway GTFS-Realtime Settings ====================
    # NYC Subway - No API key required as of 2024!
    MTA_SUBWAY_GTFS_RT_BASE_URL: str = Field(
        default="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct",
        description="MTA Subway GTFS-Realtime base URL (no API key needed)",
    )
    MTA_SUBWAY_DEFAULT_FEED: str = Field(
        default="gtfs", description="Default subway feed ID (gtfs = all lines)"
    )

    # ==================== MTA Bus Time API (Optional) ====================
    MTA_BUS_API_KEY: Optional[str] = Field(
        default=None,
        description=(
            "MTA Bus Time API key (only if you want bus data). "
            "Get from: http://bustime.mta.info/"
        ),
    )
    MTA_BUS_API_BASE_URL: str = Field(
        default="http://bustime.mta.info/api/siri",
        description="MTA Bus Time API base URL",
    )

    # ==================== Weather API Settings ====================
    OPENWEATHER_API_KEY: str = Field(
        ...,  # Required!
        description=(
            "OpenWeatherMap API key. "
            "Get from: https://openweathermap.org/api REQUIRED in .env!"
        ),
    )
    OPENWEATHER_BASE_URL: str = Field(
        default="https://api.openweathermap.org/data/2.5",
        description="OpenWeatherMap base URL",
    )

    # ==================== CORS Settings ====================
    # Note: Using str to avoid JSON parsing, will be converted to List[str] in property
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        description="Comma-separated list of allowed origins for CORS",
    )

    # ==================== Logging Settings ====================
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )

    # ==================== Pydantic Configuration ====================
    model_config = SettingsConfigDict(
        env_file=".env",  # Load from .env file
        env_file_encoding="utf-8",
        case_sensitive=True,  # Environment variables are case-sensitive
        extra="ignore",  # Ignore extra fields in .env
    )

    # ==================== Validators ====================
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, val: str, info) -> str:
        """
        Validate SECRET_KEY meets security requirements.

        Args:
            val: The secret key value.
            info: Validation context.

        Returns:
            The validated secret key.

        Raises:
            ValueError: If secret key is insecure.
        """
        if val == "your-secret-key-change-this-in-production":
            raise ValueError(
                "SECRET_KEY is using default value! "
                "Generate a secure key with: openssl rand -hex 32"
            )
        return val

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, val: str) -> str:
        """
        Validate ENVIRONMENT is a valid value.

        Args:
            val: The environment value.

        Returns:
            The validated environment value.

        Raises:
            ValueError: If environment is not valid.
        """
        allowed_envs = ["development", "staging", "production"]
        if val.lower() not in allowed_envs:
            raise ValueError(
                f"ENVIRONMENT must be one of {allowed_envs}, " f"got '{val}'"
            )
        return val.lower()  # Always return lowercase for consistency

    # ==================== Properties ====================
    @property
    def allowed_origins_list(self) -> List[str]:
        """
        Parse ALLOWED_ORIGINS string into a list of origins.

        Returns:
            List of origin URLs parsed from comma-separated string
        """
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def database_url_async(self) -> str:
        """
        Convert PostgreSQL URL: to async format for async SQLAlchemy.

        Returns:
            Async PostgreSQL connection URL.

        Example:
            postgresql://user:password@localhost:5432/database
            -> postgresql+asyncpg://user:password@localhost:5432/database
        """
        return self.DATABASE_URL.replace(
            "postgresql://",
            "postgresql+asyncpg://",
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging environment."""
        return self.ENVIRONMENT.lower() == "staging"


# ==================== Initialize Settings ====================
def get_settings() -> Settings:
    """
    Get application settings intance.

    This function creates and validates settings from environment variables.
    If required variables are missing, it will raise a clear error message.

    Returns:
        Settings instance

    Raises:
        ValidationError: If required variables are missing or invalid.
    """
    try:
        return Settings()  # type: ignore[call-arg]
    except ValidationError as err:
        print("\n❌ Configuration Error!")
        print("=" * 50)

        for error in err.errors():
            # Get the field name from the error location
            field = error["loc"][0]
            # Get the error message
            msg = error["msg"]
            print(f"  • {field}: {msg}")
        print("\n" + "=" * 50)
        print(
            "💡 Solution: "
            "Copy .env.example to .env and configure your values. "
            "Run: cp .env.example .env"
        )
        raise


# Create a global settings instance
settings = get_settings()
