# Students Database CRUD Application

**EWB Edu Tech Pvt. Ltd. — Python Backend Development Internship**

A REST API for managing student records, built with **Python, FastAPI, SQLite and Pydantic**. This implements the mandatory assignment; the optional Ollama AI extension is intentionally not required.

## Features
- Create, list, search/filter, retrieve, update and delete students.
- SQLite persistence across application restarts.
- Student fields: unique ID, name, date of birth, unique email, optional phone and course.
- Validated request bodies and dates; duplicate email returns HTTP 409.
- Missing records return HTTP 404; paginated listing via `limit` and `offset`.
- Interactive Swagger documentation at `/docs`.
- Automated API tests.

## Requirements
Python 3.10+ (recommended: Python 3.11 or 3.12).

## Install and run
From this directory:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API. SQLite database is created automatically at `students.db`. Set `STUDENT_DB_PATH` to change its location.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome |
| GET | `/health` | Health check |
| POST | `/students` | Create student |
| GET | `/students` | List; optional `search`, `course`, `limit`, `offset` |
| GET | `/students/{student_id}` | Retrieve one student |
| PUT | `/students/{student_id}` | Update supplied fields |
| DELETE | `/students/{student_id}` | Delete student |

## Example requests

Create a student:

```bash
curl -X POST http://127.0.0.1:8000/students -H "Content-Type: application/json" -d "{\"name\":\"Maya Rao\",\"date_of_birth\":\"2005-04-12\",\"email\":\"maya@example.com\",\"phone\":\"+91 98765 43210\",\"course\":\"Data Science\"}"
```

List and search:

```bash
curl "http://127.0.0.1:8000/students?search=Maya&limit=20&offset=0"
curl http://127.0.0.1:8000/students/1
```

Update and delete:

```bash
curl -X PUT http://127.0.0.1:8000/students/1 -H "Content-Type: application/json" -d "{\"course\":\"Python\"}"
curl -X DELETE http://127.0.0.1:8000/students/1
```

## Run tests

```bash
python -m pytest -q
```

## Data safety
Use fictional/demo data only. Do not commit real student personal information, database files, passwords or API keys. The database file is ignored by Git.

## Implementation notes
SQL statements use parameterized values to reduce SQL-injection risk. Dynamic update column names come only from a fixed allow-list of validated Pydantic fields. The AI extension is not included because it is optional in the assignment.
