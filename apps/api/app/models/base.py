from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from app.core.config import settings

Base = declarative_base()

# Dialect-appropriate default for updated_at fields
if settings.DB_PROVIDER == "sqlite":
    UPDATE_TIMESTAMP_DEFAULT = text("CURRENT_TIMESTAMP")
else:
    UPDATE_TIMESTAMP_DEFAULT = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

