from pydantic_settings import BaseSettings
from typing import List
from urllib.parse import quote_plus


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "password"
    db_name: str = "pupil_study"
    cors_origins: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        # URL-encode the password to handle special characters like @
        encoded_password = quote_plus(self.db_password)
        return f"mysql+pymysql://{self.db_user}:{encoded_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def cors_origins_list(self) -> List[str]:
        # return [origin.strip() for origin in self.cors_origins.split(",")]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]



settings = Settings()
