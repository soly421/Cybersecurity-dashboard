from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Change this to your actual database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ComplianceData(Base):
    __tablename__ = "compliance_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class ComplianceReport(Base):
    __tablename__ = "compliance_report"
    id = Column(Integer, primary_key=True, index=True)
    details = Column(String)

# Create the tables
Base.metadata.create_all(bind=engine)
