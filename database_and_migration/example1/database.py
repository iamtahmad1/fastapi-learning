from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
DATABASE_URL = "postgresql://testuser:testpass@10.114.104.157/todo_db"

# Create Database Engine
engine = create_engine(DATABASE_URL)

# Base Class for Models
Base = declarative_base()

# Create Session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Define Task Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
