# Students Database CRUD Application

**EWB Edu Tech Pvt. Ltd. — Python Backend Development Internship**

A REST API for managing student records, built with **Python, FastAPI, SQLite and Pydantic**. The mandatory CRUD requirements are implemented; the optional Ollama AI extension is not required.

## Live Demo

- **Live API:** https://ewb-student-crud-api.onrender.com
- **Interactive Swagger documentation:** https://ewb-student-crud-api.onrender.com/docs
- **Health check:** https://ewb-student-crud-api.onrender.com/health

The health endpoint should return:

```json
{"status":"ok","database":"sqlite"}
```

> **Hosting note:** This demo uses Render's free web-service plan. Its local filesystem is ephemeral, so records stored in the deployed SQLite database may be lost when the service restarts or redeploys. Local SQLite storage persists across application restarts when the database file is retained. Use fictional data only in the public demo.

## Features

- Create, list, search/filter, retrieve, update and delete students.
- SQLite database created automatically.
- Student fields: unique ID, name, date of birth, unique email, optional phone and course.
- Validated request bodies and dates; duplicate email returns HTTP 409.
- Missing records return HTTP 404; paginated listing via `limit` and `offset`.
- Interactive Swagger documentation at `/docs`.
- Automated API tests and a GitHub Actions workflow.

## Requirements

Python 3.10+ (recommended: Python 3.11 or 3.12).

## Install and run locally

From the `ewb-student-crud` directory:

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the local API. SQLite database is created automatically at `students.db`. Set `STUDENT_DB_PATH` to change its location.

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

The examples below use the **live API**. Replace the sample data with fictional data of your own. You can also run the same requests against `http://127.0.0.1:8000` when testing locally.

Create a student:

```bash
curl -X POST "https://ewb-student-crud-api.onrender.com/students" \
  -H "Content-Type: application/json" \
  -d '{"name":"Maya Rao","date_of_birth":"2005-04-12","email":"maya.demo@example.com","phone":"+91 98765 43210","course":"Data Science"}'
```

List, search and retrieve:

```bash
curl "https://ewb-student-crud-api.onrender.com/students?search=Maya&limit=20&offset=0"
curl "https://ewb-student-crud-api.onrender.com/students/1"
```

Update and delete:

```bash
curl -X PUT "https://ewb-student-crud-api.onrender.com/students/1" \
  -H "Content-Type: application/json" \
  -d '{"course":"Python"}'

curl -X DELETE "https://ewb-student-crud-api.onrender.com/students/1"
```

> The numeric ID `1` is an example only. Use the ID returned by your own create request. Since this is a public demo, do not use real personal information or delete records that you did not create.

## Run tests

From the `ewb-student-crud` directory:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

GitHub Actions is configured to run the test suite when project files change on the submission branch.

## Data safety

Use fictional/demo data only. Do not commit real student personal information, database files, passwords or API keys. The database file is ignored by Git.

## Implementation notes

SQL statements use parameterized values to reduce SQL-injection risk. Dynamic update column names come only from a fixed allow-list of validated Pydantic fields. The AI extension is not included because it is optional in the assignment.
