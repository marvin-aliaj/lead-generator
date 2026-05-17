from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_whatsapp_number: str
    resend_api_key: str
    resend_from_email: str = "noreply@visto.al"
    base_url: str
    nextjs_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
