import sqlite3

DB_NAME = "interview.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        score REAL,
        evaluation TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_interview(role, score, evaluation):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interviews(role, score, evaluation)
        VALUES (?, ?, ?)
        """,
        (role, score, evaluation)
    )

    conn.commit()
    conn.close()


def get_all_interviews():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM interviews"
    )

    data = cursor.fetchall()

    conn.close()

    return data