from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://postgres:Aightson1!@db.gwandgydnaeommvslqzo.supabase.co:5432/postgres"  
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Compliance Data Model
class ComplianceData(Base):
    __tablename__ = "compliance_data"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    description = Column(Text)

# Create database tables
Base.metadata.create_all(bind=engine)
