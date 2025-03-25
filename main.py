from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Cybersecurity API is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
