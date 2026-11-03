"""A small, local student information system for an institute."""
from __future__ import annotations

import argparse
import csv
import io
import os
import sqlite3
from datetime import date
from functools import wraps
from pathlib import Path

from flask import (Flask, Response, abort, flash, g, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("STUDENT_DB", ROOT / "students.db"))
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-key-change-this")


def connect_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY, student_no TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL, last_name TEXT NOT NULL,
            email TEXT NOT NULL DEFAULT '', phone TEXT NOT NULL DEFAULT '',
            program TEXT NOT NULL, year_level INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL, semester TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
            grade REAL, UNIQUE(student_id, course_id)
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
            course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
            class_date TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('Present','Absent','Late')),
            UNIQUE(student_id, course_id, class_date)
        );
        CREATE INDEX IF NOT EXISTS idx_students_name ON students(last_name, first_name);
        CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(class_date);
        """)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.before_request
def open_db():
    g.db = connect_db()


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_student(student_id):
    student = g.db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if student is None:
        abort(404)
    return student


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = g.db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username", "").strip(),)).fetchone()
 if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(request.args.get("next") or url_for("dashboard"))
        flash("Username or password is incorrect.", "error")
    return render_template("login.html")
