from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ✅ Replace with your actual database URL
DATABASE_URL = "postgresql://postgres:Aightson1!@db.gwandgydnaeommvslqzo.supabase.co:5432/postgres"  

# ✅ Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# ✅ Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Define the base class for models
Base = declarative_base()

# ✅ Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
