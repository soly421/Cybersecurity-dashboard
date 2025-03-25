from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI()

# Database connection (PostgreSQL)
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASS"), 
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT")
    )

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
    cur.execute("INSERT INTO metrics (name, value, category) VALUES (%s, %s, %s)", 
                (metric.name, metric.value, metric.category))
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
    return {"metrics": metrics}

@app.post("/assess")
def assess_maturity(request: MaturityAssessmentRequest):
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[{"role": "system", "content": "Evaluate the cybersecurity program based on NIST CSF."},
                  {"role": "user", "content": request
