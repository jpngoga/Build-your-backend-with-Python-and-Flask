
import json
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = Path(__file__).parent / "data" / "courses.json"
VALID_STATUSES = {"Draft", "Published", "Archived"}


def load_courses():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")

    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_courses(courses):
    DATA_FILE.write_text(
        json.dumps(courses, indent=2),
        encoding="utf-8",
    )


def validate_course(data, existing=None):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object."

    existing = existing or {}
    course = {}

    for field in ("title", "description", "instructor"):
        value = data.get(field, existing.get(field, ""))

        if not isinstance(value, str) or not value.strip():
            return None, f"{field} must be a non-empty string."

        course[field] = value.strip()

    duration = data.get("duration", existing.get("duration"))

    if (
        isinstance(duration, bool)
        or not isinstance(duration, int)
        or duration <= 0
    ):
        return None, "duration must be a positive integer."

    course["duration"] = duration

    status = data.get("status", existing.get("status", "Draft"))

    if not isinstance(status, str) or status not in VALID_STATUSES:
        return None, "status must be Draft, Published, or Archived."

    course["status"] = status
    return course, None


def find_course(courses, course_id):
    return next(
        (course for course in courses if course["id"] == course_id),
        None,
    )


@app.get("/")
def home():
    return jsonify({
        "message": "Welcome to CodeCraftHub API",
        "courses_endpoint": "/api/courses",
    }), 200


@app.get("/api/courses")
def get_courses():
    courses = load_courses()
    return jsonify({
        "success": True,
        "count": len(courses),
        "data": courses,
    }), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    course = find_course(load_courses(), course_id)

    if course is None:
        return jsonify({
            "success": False,
            "error": "Course not found.",
        }), 404

    return jsonify({"success": True, "data": course}), 200


@app.post("/api/courses")
def create_course():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "success": False,
            "error": "Provide a valid JSON request body.",
        }), 400

    course_data, error = validate_course(data)

    if error:
        return jsonify({"success": False, "error": error}), 400

    courses = load_courses()
    next_id = max((c["id"] for c in courses), default=0) + 1

    course = {"id": next_id, **course_data}
    courses.append(course)
    save_courses(courses)

    return jsonify({
        "success": True,
        "message": "Course created successfully.",
        "data": course,
    }), 201


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "success": False,
            "error": "Provide a valid JSON request body.",
        }), 400

    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "success": False,
            "error": "Course not found.",
        }), 404

    course_data, error = validate_course(data, course)

    if error:
        return jsonify({"success": False, "error": error}), 400

    course.update(course_data)
    save_courses(courses)

    return jsonify({
        "success": True,
        "message": "Course updated successfully.",
        "data": course,
    }), 200


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    courses = load_courses()
    course = find_course(courses, course_id)

    if course is None:
        return jsonify({
            "success": False,
            "error": "Course not found.",
        }), 404

    courses.remove(course)
    save_courses(courses)

    return jsonify({
        "success": True,
        "message": "Course deleted successfully.",
    }), 200


@app.get("/api/stats")
def get_stats():
    courses = load_courses()

    return jsonify({
        "success": True,
        "total": len(courses),
        "by_status": {
            status: sum(
                1 for course in courses
                if course.get("status") == status
            )
            for status in sorted(VALID_STATUSES)
        },
    }), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found.",
    }), 404


@app.errorhandler(405)
def method_not_allowed(_error):
    return jsonify({
        "success": False,
        "error": "HTTP method not allowed.",
    }), 405


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
