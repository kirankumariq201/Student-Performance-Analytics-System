"""EWB Edu Tech internship: Students Database CRUD API."""
from contextlib import asynccontextmanager
from datetime import date
import os
import sqlite3
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

DB_PATH = Path(os.getenv("STUDENT_DB_PATH", str(Path(__file__).resolve().parent.parent / "students.db")))

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(length(trim(name)) BETWEEN 1 AND 100),
                date_of_birth TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                phone TEXT,
                course TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="EWB Students Database CRUD API", version="1.0.0",
              description="Student record management using FastAPI and SQLite.", lifespan=lifespan)

class StudentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    email: EmailStr
    phone: str | None = Field(default=None, max_length=25)
    course: str | None = Field(default=None, max_length=100)

    @field_validator("phone")
    @classmethod
    def phone_has_valid_characters(cls, value):
        if value is not None and value and not all(c.isdigit() or c in "+- ()" for c in value):
            raise ValueError("Phone may contain digits, spaces, +, -, and parentheses only")
        return value or None

class StudentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: date | None = None
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=25)
    course: str | None = Field(default=None, max_length=100)

    @field_validator("phone")
    @classmethod
    def phone_has_valid_characters(cls, value):
        if value is not None and value and not all(c.isdigit() or c in "+- ()" for c in value):
            raise ValueError("Phone may contain digits, spaces, +, -, and parentheses only")
        return value or None

class StudentOut(BaseModel):
    id: int
    name: str
    date_of_birth: date
    email: EmailStr
    phone: str | None
    course: str | None
    created_at: str

def row_to_student(row):
    return dict(row)

@app.get("/", tags=["Health"])
def root():
    return {"message": "EWB Students CRUD API is running", "docs": "/docs", "health": "/health"}

@app.get("/health", tags=["Health"])
def health():
    with connect() as conn:
        conn.execute("SELECT 1").fetchone()
    return {"status": "ok", "database": "sqlite"}

@app.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: StudentCreate):
    if student.date_of_birth > date.today():
        raise HTTPException(status_code=422, detail="Date of birth cannot be in the future")
    try:
        with connect() as conn:
            cursor = conn.execute(
                "INSERT INTO students (name, date_of_birth, email, phone, course) VALUES (?, ?, ?, ?, ?)",
                (student.name, student.date_of_birth.isoformat(), str(student.email).lower(),
                 student.phone, student.course))
            row = conn.execute("SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)).fetchone()
            return row_to_student(row)
    except sqlite3.IntegrityError as exc:
        if "email" in str(exc).lower():
            raise HTTPException(status_code=409, detail="A student with this email already exists") from exc
        raise HTTPException(status_code=400, detail="Student record violates a database constraint") from exc

@app.get("/students", response_model=list[StudentOut], tags=["Students"])
def list_students(search: str | None = Query(default=None, max_length=100),
                  course: str | None = Query(default=None, max_length=100),
                  limit: Annotated[int, Query(ge=1, le=100)] = 100,
                  offset: Annotated[int, Query(ge=0)] = 0):
    sql = "SELECT * FROM students WHERE 1=1"
    params = []
    if search:
        sql += " AND (name LIKE ? OR email LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if course:
        sql += " AND course = ?"
        params.append(course)
    sql += " ORDER BY id LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    with connect() as conn:
        return [row_to_student(r) for r in conn.execute(sql, params).fetchall()]

@app.get("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def get_student(student_id: int):
    with connect() as conn:
        row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return row_to_student(row)

@app.put("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def update_student(student_id: int, updates: StudentUpdate):
    changes = updates.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Provide at least one field to update")
    if "name" in changes and changes["name"] is None:
        raise HTTPException(status_code=422, detail="Name cannot be null")
    if "email" in changes and changes["email"] is None:
        raise HTTPException(status_code=422, detail="Email cannot be null")
    if "date_of_birth" in changes:
        dob = changes["date_of_birth"]
        if dob is None or dob > date.today():
            raise HTTPException(status_code=422, detail="Provide a valid date of birth that is not in the future")
        changes["date_of_birth"] = dob.isoformat()
    if changes.get("email") is not None:
        changes["email"] = str(changes["email"]).lower()
    allowed = {"name", "date_of_birth", "email", "phone", "course"}
    assignments = ", ".join(f"{key} = ?" for key in changes if key in allowed)
    values = [changes[key] for key in changes if key in allowed]
    try:
        with connect() as conn:
            existing = conn.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
            if existing is None:
                raise HTTPException(status_code=404, detail="Student not found")
            conn.execute(f"UPDATE students SET {assignments} WHERE id = ?", (*values, student_id))
            row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            return row_to_student(row)
    except sqlite3.IntegrityError as exc:
        if "email" in str(exc).lower():
            raise HTTPException(status_code=409, detail="A student with this email already exists") from exc
        raise HTTPException(status_code=400, detail="Student record violates a database constraint") from exc

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int):
    with connect() as conn:
        cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
