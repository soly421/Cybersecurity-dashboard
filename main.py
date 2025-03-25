from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base, ComplianceData
from models import ComplianceRequest, AssessmentRequest, User
from security import get_password_hash, verify_password, create_access_token
import openai
import os

# Initialize FastAPI
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# OpenAI API Key (set this in Render environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "CISO Cybersecurity Tool is running!"}

# NIST CSF LLM-Powered Assessment
@app.post("/nist-assessment/")
def generate_nist_assessment(request: AssessmentRequest, db: Session = Depends(get_db)):
    prompt = f"Analyze this cybersecurity data based on NIST CSF: {request.security_data}. Provide a detailed assessment."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert following NIST CSF guidelines
