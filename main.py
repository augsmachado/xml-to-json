from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import status, convertions

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="XML/JSON Utility API",
    version="1.0.0",
    description="API for status, XML to JSON, and JSON to XML conversion"
)

# Allow CORS for all origins (optional, for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("API_KEY")
def require_api_key(x_api_key: str = Header(..., alias="X-API-KEY")):
    """
    Dependency to require API_KEY in the X-API-KEY header.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key."
        )
        
# Include routers
app.include_router(status.router)
app.include_router(
    convertions.router,
    dependencies=[Depends(require_api_key)]
)