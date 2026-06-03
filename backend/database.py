"""
Database setup and models for SQLite
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

DB_PATH = Path(__file__).parent / "app_config.db"


def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database schema"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compilations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            app_name TEXT NOT NULL,
            config_json TEXT NOT NULL,
            validation_passed BOOLEAN DEFAULT 0,
            repair_applied BOOLEAN DEFAULT 0,
            overall_score REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compilation_id INTEGER NOT NULL,
            stage_name TEXT NOT NULL,
            stage_output TEXT NOT NULL,
            execution_time REAL,
            status TEXT,
            error_message TEXT,
            FOREIGN KEY (compilation_id) REFERENCES compilations(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS validation_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compilation_id INTEGER NOT NULL,
            validation_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (compilation_id) REFERENCES compilations(id)
        )
    """)

    conn.commit()
    conn.close()


def save_compilation(
    prompt: str,
    app_name: str,
    config: Dict[str, Any],
    validation_passed: bool = False,
    repair_applied: bool = False,
    overall_score: float = 0.0
) -> int:
    """Save compilation result"""
    conn = get_db_connection()
    cursor = conn.cursor()

    config_json = json.dumps(config)

    cursor.execute("""
        INSERT INTO compilations 
        (prompt, app_name, config_json, validation_passed, repair_applied, overall_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (prompt, app_name, config_json, validation_passed, repair_applied, overall_score))

    conn.commit()
    compilation_id = cursor.lastrowid
    conn.close()

    return compilation_id


def save_pipeline_stage(
    compilation_id: int,
    stage_name: str,
    stage_output: Dict[str, Any],
    execution_time: float,
    status: str = "success",
    error_message: Optional[str] = None
):
    """Save pipeline stage execution"""
    conn = get_db_connection()
    cursor = conn.cursor()

    stage_output_json = json.dumps(stage_output, default=str)

    cursor.execute("""
        INSERT INTO pipeline_runs
        (compilation_id, stage_name, stage_output, execution_time, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (compilation_id, stage_name, stage_output_json, execution_time, status, error_message))

    conn.commit()
    conn.close()


def get_compilation(compilation_id: int) -> Optional[Dict[str, Any]]:
    """Get compilation by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM compilations WHERE id = ?", (compilation_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def get_compilation_history(limit: int = 50) -> list:
    """Get recent compilations"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, app_name, created_at, validation_passed, overall_score
        FROM compilations
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_pipeline_runs(compilation_id: int) -> list:
    """Get all pipeline stage runs for a compilation"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT stage_name, stage_output, execution_time, status, error_message
        FROM pipeline_runs
        WHERE compilation_id = ?
        ORDER BY id ASC
    """, (compilation_id,))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results
