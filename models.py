from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ComplianceData(Base):
    __tablename__ = "compliance_data"

    id = Column(Integer, primary_key=True, index=True)
    control = Column(String, index=True)
    description = Column(String)
    maturity_level = Column(Float)

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"

    id = Column(Integer, primary_key=True, index=True)
    assessment_date = Column(String)
    overall_score = Column(Float)
