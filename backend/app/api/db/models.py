from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import datetime

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    skills = relationship("Skill", back_populates="role")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    name = Column(String, index=True)
    role = relationship("Role", back_populates="skills")
    resources = relationship("Resource", back_populates="skill")

# Analyses table
class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    score = Column(Integer)
    found = Column(JSON)
    missing = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
