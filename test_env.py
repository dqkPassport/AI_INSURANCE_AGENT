from app.core.settings import settings

print("DB:", settings.database_url)
print("Model:", settings.openai_model)
print("Key exists:", bool(settings.openai_api_key))
