import os
import openai
import requests
import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Dict, Any
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, ComplianceData, ComplianceReport

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Pydantic models for incoming data validation
class ComplianceRequest(BaseModel):
    organization_id: str
    standards: Dict[str, Any]

# Helper functions to interact with NIST, ISO APIs
def fetch_compliance_data_from_nist(organization_id: str):
    # Placeholder API call - Replace with actual NIST API call
    return {"nist_csf": "Level 3", "nist_800_53": True, "nist_ai_rmf_compliance": True}

def fetch_compliance_data_from_iso(organization_id: str):
    # Placeholder API call - Replace with actual ISO API call
    return {"iso27001_compliance": True}

# Generate compliance report using OpenAI
def generate_compliance_report(data: Dict[str, Any]) -> str:
    prompt = f"""
    Generate a detailed compliance report based on the following data:
    NIST CSF Level: {data['nist_csf']}
    NIST 800-53 Compliance: {data['nist_800_53']}
    ISO 27001 Compliance: {data['iso27001_compliance']}
    NIST AI RMF Compliance: {data['nist_ai_rmf_compliance']}

    The report should be suitable for senior executive audiences and focus on areas that need attention.
    """

    try:
        response = openai.Completion.create(
            engine="gpt-4",  # Ensure to use the latest engine (e.g., GPT-4)
            prompt=prompt,
            max_tokens=1500,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

# Endpoint for generating a compliance report
@app.post("/generate_report/")
async def generate_report(request: ComplianceRequest, db: Session = Depends(get_db)):
    try:
        # Fetching compliance data from external sources
        nist_data = fetch_compliance_data_from_nist(request.organization_id)
        iso_data = fetch_compliance_data_from_iso(request.organization_id)
        
        # Combine the compliance data from different standards
        combined_data = {
            "nist_csf": nist_data["nist_csf"],
            "nist_800_53": nist_data["nist_800_53"],
            "iso27001_compliance": iso_data["iso27001_compliance"],
            "nist_ai_rmf_compliance": nist_data["nist_ai_rmf_compliance"]
        }

        # Generate the compliance report using OpenAI
        report = generate_compliance_report(combined_data)

        # Store the report in the database (for historical records and audit)
        new_report = ComplianceReport(
            organization_id=request.organization_id,
            report=report,
            standards=json.dumps(combined_data)
        )
        db.add(new_report)
        db.commit()

        return {"status": "success", "report": report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating compliance report: {str(e)}")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database (create tables)
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
