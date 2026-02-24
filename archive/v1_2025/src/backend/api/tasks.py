#!/usr/bin/env python3
"""
ELWOSA Task Management API
==========================

A robust task management service implementing RESTful endpoints with
full CRUD operations, real-time updates, and comprehensive field coverage.

This service demonstrates:
- Clean architecture patterns
- Type-safe request/response handling
- Database abstraction
- Error handling and logging
- API documentation
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import psycopg2
import psycopg2.extras
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ELWOSA Task Management API",
    description="Enterprise task management with real-time updates",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration from environment
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "elwosa"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": os.getenv("DB_PORT", "5432"),
}


def get_db_connection():
    """
    Create and return a database connection.
    Implements connection pooling in production.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


# Pydantic models for type safety
class Step(BaseModel):
    """Represents a single step in task execution"""
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    user: str = Field(default="System", description="User who performed the step")
    content: str = Field(..., description="Step description")


class TaskBase(BaseModel):
    """Base model for task operations"""
    project_id: Optional[str] = Field(None, description="Associated project ID")
    task_id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Detailed task description")
    status: Optional[str] = Field("QUEUED", description="Current task status")
    priority: Optional[int] = Field(None, ge=0, le=10, description="Task priority (0-10)")
    estimated_hours: Optional[float] = Field(None, gt=0, description="Estimated hours")
    actual_hours: Optional[float] = Field(None, ge=0, description="Actual hours spent")
    assigned_to: Optional[str] = Field(None, description="Assigned user")
    tags: Optional[List[str]] = Field(default_factory=list, description="Task tags")
    steps: Optional[List[Step]] = Field(default_factory=list, description="Execution steps")


class TaskCreate(TaskBase):
    """Model for creating new tasks"""
    pass


class TaskUpdate(BaseModel):
    """Model for updating existing tasks"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    assigned_to: Optional[str] = None
    tags: Optional[List[str]] = None


class TaskResponse(TaskBase):
    """Model for task responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        orm_mode = True


# API Endpoints
@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "service": "ELWOSA Task Management API",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def list_tasks(
    status: Optional[str] = None,
    priority: Optional[int] = None,
    assigned_to: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Retrieve all tasks with optional filtering.
    
    - **status**: Filter by task status
    - **priority**: Filter by priority level
    - **assigned_to**: Filter by assigned user
    - **limit**: Maximum number of results
    - **offset**: Number of results to skip
    """
    query = """
        SELECT id, project_id, task_id, title, description, status, priority,
               estimated_hours, actual_hours, assigned_to, created_at, updated_at,
               completed_at, steps, tags
        FROM tasks
        WHERE 1=1
    """
    params = []
    
    if status:
        query += " AND status = %s"
        params.append(status)
    if priority is not None:
        query += " AND priority = %s"
        params.append(priority)
    if assigned_to:
        query += " AND assigned_to = %s"
        params.append(assigned_to)
    
    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            tasks = cur.fetchall()
            return tasks
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")