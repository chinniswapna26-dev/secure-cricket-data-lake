
import sqlite3
import os
import psycopg2
from psycopg2.extras import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "cricket_users.db")
DATABASE_URL = os.environ.get("DATABASE_URL")


class PostgreSQLConnection:
    def __init__(self, url):
        self.connection = psycopg2.connect(
            url,
            cursor_factory=DictCursor,
            sslmode="require"
        )

    def execute(self, query, params=()):
        query = query.replace("?", "%s")
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


def get_connection():
    if DATABASE_URL:
        return PostgreSQLConnection(DATABASE_URL)

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    if DATABASE_URL:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Read-only User',
                mfa_secret TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Read-only User',
                mfa_secret TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    admin_username = os.environ.get("ADMIN_USERNAME", "").strip()

    if admin_username:
        connection.execute(
            "UPDATE users SET role = 'Administrator' WHERE username = ?",
            (admin_username,)
        )

    connection.commit()
    connection.close()


def create_user(username, password, role="Read-only User"):
    connection = get_connection()

    try:
        password_hash = generate_password_hash(password)

        connection.execute(
            """INSERT INTO users (username, password_hash, role)
               VALUES (?, ?, ?)""",
            (username, password_hash, role)
        )

        connection.commit()
        return True

    except (sqlite3.IntegrityError, psycopg2.IntegrityError):
        return False

    finally:
        connection.close()


def get_user(username):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()
    return user


def verify_password(user, password):
    return check_password_hash(user["password_hash"], password)


def save_mfa_secret(username, secret):
    connection = get_connection()

    connection.execute(
        "UPDATE users SET mfa_secret = ? WHERE username = ?",
        (secret, username)
    )

    connection.commit()
    connection.close()


def count_users():
    connection = get_connection()
    count = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]
    connection.close()
    return count


def get_all_users():
    connection = get_connection()
    users = connection.execute(
        "SELECT id, username, role, created_at FROM users"
    ).fetchall()
    connection.close()
    return users


def update_user_role(user_id, role):
    allowed_roles = [
        "Administrator",
        "Data Analyst",
        "Coach",
        "Read-only User"
    ]

    if role not in allowed_roles:
        return False

    connection = get_connection()
    connection.execute(
        "UPDATE users SET role = ? WHERE id = ?",
        (role, user_id)
    )

    connection.commit()
    connection.close()
    return True
