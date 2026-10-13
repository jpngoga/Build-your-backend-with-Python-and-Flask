# CodeCraftHub Backend API

A REST API built with Python and Flask for managing online courses.
Course records are stored in a local JSON file.

## Features

- Create, read, update, and delete courses (CRUD).
- Validate course data and status values.
- Return appropriate HTTP status codes and JSON errors.
- Enable Cross-Origin Resource Sharing (CORS).
- View course statistics by status.

## Technologies

- Python
- Flask
- Flask-CORS
- JSON file storage

## Project Structure

```text
Build-your-backend-with-Python-and-Flask/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── courses.json
```

## Setup

Python 3.9 or newer is recommended, subject to dependency compatibility.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the API

```bash
python app.py
```

The development server runs at:

`http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/api/courses` | List all courses |
| GET | `/api/courses/<id>` | Get one course |
| POST | `/api/courses` | Create a course |
| PUT | `/api/courses/<id>` | Update a course |
| DELETE | `/api/courses/<id>` | Delete a course |
| GET | `/api/stats` | Get course statistics |

## Course Data

Example JSON request body:

```json
{
  "title": "Python for Beginners",
  "description": "Learn Python fundamentals",
  "instructor": "Alex Morgan",
  "duration": 6,
  "status": "Published"
}
```

Required fields:

- `title`: non-empty string
- `description`: non-empty string
- `instructor`: non-empty string
- `duration`: positive integer
- `status`: `Draft`, `Published`, or `Archived`

## Example Requests

Create a course:

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"title":"Python for Beginners","description":"Learn Python fundamentals","instructor":"Alex Morgan","duration":6,"status":"Published"}'
```

List courses:

```bash
curl -i http://127.0.0.1:5000/api/courses
```

Get statistics:

```bash
curl -i http://127.0.0.1:5000/api/stats
```

## Error Handling

- `400 Bad Request`: invalid JSON or course data.
- `404 Not Found`: course or endpoint not found.
- `405 Method Not Allowed`: unsupported HTTP method.

## Storage

Course records are stored in `data/courses.json`. The file is initialized automatically if it does not exist.

## Development Note

This project is intended for learning and local development. The Flask development server is not intended for production deployment.
