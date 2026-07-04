from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.v1.router import api_router
from app.governance.middleware import GovernanceMiddleware
from app.core.database import engine
from app.models.base import Base
import app.models  # Import to register models with Base

# Initialize all database tables at startup
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")
except Exception as e:
    print(f"Error initializing database tables: {e}")


app = FastAPI(
    title="KSP Crime Intelligence Platform - API",
    description="Backend API for KSP Intelligence Platform on Zoho Catalyst",
    version="1.0.0"
)

# Governance Substrate middleware registered first to intercept/validate all responses
app.add_middleware(GovernanceMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include bundled API Routers
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "KSP Crime Intelligence API is running on Zoho Catalyst"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    # Catalyst AppSail typically sets the X-ZOHO-CATALYST-PORT or standard PORT environment variable
    port = int(os.environ.get("X_ZOHO_CATALYST_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
