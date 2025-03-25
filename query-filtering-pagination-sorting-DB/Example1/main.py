from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from database import Task

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks")
def get_tasks(
    search: str = Query(None, description="Search by task title"),
    completed: bool = Query(None, description="Filter by completion status"),
    sort: str = Query("created_at", description="Sort by field (priority, created_at)"),
    limit: int = Query(10, ge=1, le=100, description="Limit number of tasks"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
):
    # Start the query
    query = db.query(Task)

    # Apply filtering
    if completed is not None:
        query = query.filter(Task.completed == completed)

    # Apply sorting
    if sort == "priority":
        query = query.order_by(Task.priority.desc())
    else:
        query = query.order_by(Task.created_at.desc())  # Default sorting

    # Apply pagination
    tasks = query.offset(offset).limit(limit).all()

    # Apply searching (case-insensitive)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    return query.all()
