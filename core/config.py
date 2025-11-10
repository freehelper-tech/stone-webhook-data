"""
Configurações do Dashboard Impulso Stone
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Configurações principais da aplicação"""
    
    # Aplicação
    APP_NAME: str = "Dashboard Impulso Stone"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Segurança
    SECRET_KEY: str = "your-secret-key-here"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # SQL Server (Azure) - Connection String direta
    AZURE_SQL_CONNECTION_STRING: str = (
        "mssql+pyodbc://usr_free_helper:23%403ryR2"
        "@dev-free-helper.database.windows.net:1433/dashboardImpulso"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&Encrypt=yes"
        "&TrustServerCertificate=no"
        "&Connection+Timeout=30"
    )
    
    # SQL Server (Fallback - componentes individuais)
    SQL_SERVER: str = "localhost"
    SQL_DATABASE: str = "dashboardImpulso"
    SQL_USERNAME: str = "sa"
    SQL_PASSWORD: str = ""
    SQL_DRIVER: str = "ODBC Driver 18 for SQL Server"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def sql_connection_string(self) -> str:
        """
        Obter connection string do SQL Server
        Prioridade: AZURE_SQL_CONNECTION_STRING do .env, senão constrói a partir dos componentes
        """
        # Se tem AZURE_SQL_CONNECTION_STRING, usar ela diretamente
        if self.AZURE_SQL_CONNECTION_STRING and self.AZURE_SQL_CONNECTION_STRING.strip():
            conn = self.AZURE_SQL_CONNECTION_STRING.strip()
            if "ConnectionTimeout=" in conn and "Connection+Timeout=" not in conn:
                conn = conn.replace("ConnectionTimeout=", "Connection+Timeout=")
            return conn
        
        # Senão, construir a partir dos componentes
        return (
            f"mssql+pyodbc://{self.SQL_USERNAME}:{self.SQL_PASSWORD}"
            f"@{self.SQL_SERVER}/{self.SQL_DATABASE}"
            f"?driver={self.SQL_DRIVER.replace(' ', '+')}"
            f"&TrustServerCertificate=yes"
        )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignorar campos extras do .env
    )


# Instância global das configurações
settings = Settings()
