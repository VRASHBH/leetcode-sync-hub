from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI(title="LeetCode Sync Hub")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "database/solutions.db"


# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS solutions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_name TEXT,
        difficulty TEXT,
        language TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- MODELS ---------------- #

class Solution(BaseModel):
    problem_name: str
    difficulty: str
    language: str


# ---------------- ROUTES ---------------- #

@app.get("/")
def home():
    return {
        "project": "LeetCode Sync Hub",
        "status": "Running"
    }


@app.get("/stats")
def stats():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM solutions")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM solutions WHERE difficulty='Easy'")
    easy = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM solutions WHERE difficulty='Medium'")
    medium = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM solutions WHERE difficulty='Hard'")
    hard = cur.fetchone()[0]

    conn.close()

    return {
        "total_solved": total,
        "easy": easy,
        "medium": medium,
        "hard": hard
    }


@app.post("/add-solution")
def add_solution(solution: Solution):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO solutions(problem_name,difficulty,language)
    VALUES(?,?,?)
    """, (
        solution.problem_name,
        solution.difficulty,
        solution.language
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Solution Added Successfully"
    }


@app.get("/solutions")
def get_solutions():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT problem_name,difficulty,language
    FROM solutions
    """)

    rows = cur.fetchall()

    conn.close()

    return rows