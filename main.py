from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI()

# Database connection (PostgreSQL)
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
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Pydantic models
class CyberSecurityMetric(BaseModel):
    name: str
    value: float
    category: str

class MaturityAssessmentRequest(BaseModel):
    program_data: str

# API Endpoints
@app.post("/metrics/add")
def add_metric(metric: CyberSecurityMetric):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO metrics (name, value, category) VALUES (%s, %s, %s)", 
        (metric.name, metric.value, metric.category)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Metric added successfully"}

@app.get("/metrics")
def get_metrics():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, value, category FROM metrics")
    metrics = cur.fetchall()
    cur.close()
    conn.close()
    return {"metrics": [{"name": m[0], "value": m[1], "category": m[2]} for m in metrics]}

@app.post("/assess")
def assess_m_
