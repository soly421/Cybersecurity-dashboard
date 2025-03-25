from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://postgres:Aightson1!@db.gwandgydnaeommvslqzo.supabase.co:5432/postgres"  

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Compliance Data Model
class ComplianceData(Base):
    __tablename__ = "compliance_data"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    description = Column(Text)

# Compliance Report Model
class ComplianceReport(Base):
    __tablename__ = "compliance_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_name = Column

