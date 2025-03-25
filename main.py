from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base, ComplianceData
from schemas import ComplianceRequest, AssessmentRequest
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
                {"role": "system", "content": "You are a cybersecurity expert following NIST CSF guidelines."},
                {"role": "user", "content": prompt}
            ]
        )
        assessment_result = response["choices"][0]["message"]["content"]
        return {"nist_assessment": assessment_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

# Fetch Compliance Data
@app.get("/compliance/")
def get_compliance_data(db: Session = Depends(get_db)):
    return db.query(ComplianceData).all()

# User Registration
@app.post("/register/")
def register_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"}

# User Login
@app.post("/login/")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
