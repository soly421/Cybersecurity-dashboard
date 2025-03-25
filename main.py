from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import openai
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI(
    title="Cybersecurity API",
    version="1.0",
    docs_url="/docs",  # Enables Swagger UI
    redoc_url="/redoc",  # Enables alternative API docs
    openapi_url="/openapi.json"  # Ensures OpenAPI schema is available
)

# Fix CORS issues for accessing the API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure environment variables are set
required_env_vars = ["DB_NAME", "DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "OPENAI_API_KEY"]
for var in required_env_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

# Custom OpenAPI Schema to fix empty /docs issue
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cybersecurity API",
        version="1.0",
        description="API for cybersecurity program management",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Root endpoint
@app.get("/")
def home():
    return {"message": "Cybersecurity API is running!"}

# Database connection function
def get_db_connection():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"), 
            user=os.getenv("DB_USER"), 
            password=os.getenv("DB_PASS"), 
            host=os.getenv("DB_HOST"), 
            port=os.getenv("DB_PORT")
        )
    except Exception as e:
        raise
