from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_whatsapp_number: str
    base_url: str

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
