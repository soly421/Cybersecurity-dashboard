from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from typing import Dict

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Cybersecurity Program Management API")

# Authentication Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock user database
users_db = {
    "admin": {"username": "admin", "password": "securepass", "role": "admin"}
}

# Pydantic Models
class UserLogin(BaseModel):
    username: str
    password: str

class NISTAssessmentRequest(BaseModel):
    controls: Dict[str, str]  # Control areas mapped to responses

class AssessmentResult(BaseModel):
    maturity_score: float
    recommendations: str

# Token endpoint
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": form_data.username, "token_type": "bearer"}

# Secure route example
@app.get("/secure-data")
async def get_secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a secure endpoint", "user": token}

# NIST CSF Assessment
@app.post("/nist-assessment", response_model=AssessmentResult)
async def nist_assessment(request: NISTAssessmentRequest):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Evaluate the following NIST CSF controls:\n{request.controls}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in cybersecurity compliance."},
                  {"role": "user", "content": prompt}]
    )

    return AssessmentResult(
        maturity_score=85.0,  # Example score
        recommendations=response["choices"][0]["message"]["content"]
    )

# Root endpoint
@app.get("/")
def home():
    return {"message": "Cybersecurity Program API is running!"}
