import re
import sqlite3
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport

from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.requests import Request

# -----------------------------------
# Configuration
# -----------------------------------

DB_URI = "file:sqluniversity.db?mode=ro"
MAX_RETURN_ROWS = 5000  # prevents accidental massive fetch

mcp = FastMCP("SQL-University-ReadOnly-Server")

# -----------------------------------
# SQLite Helper (Read Only + Engine Guard)
# -----------------------------------

def get_connection():
    conn = sqlite3.connect(DB_URI, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Enforce read-only at SQLite execution layer (cannot be bypassed)
    conn.execute("PRAGMA query_only = ON;")

    return conn

# -----------------------------------
# Query Validation (Semantic Read-Only)
# -----------------------------------

# -----------------------------------
# Query Validation (Read-Only Semantic Check)
# -----------------------------------

WRITE_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter",
    "create", "replace", "truncate",
    "attach", "detach", "reindex",
    "vacuum", "analyze",
    "pragma", "transaction", "commit", "rollback",
    "savepoint", "release",
}


def _strip_sql_comments(sql: str) -> str:
    # Remove /* */ comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.S)

    # Remove -- comments
    sql = re.sub(r"--.*?$", "", sql, flags=re.M)

    return sql


def validate_query(query: str):
    if not query or not query.strip():
        raise ValueError("Empty query.")

    # Remove comments to avoid hidden attacks
    cleaned = _strip_sql_comments(query)

    # Normalize for analysis (NOT execution)
    normalized = re.sub(r"\s+", " ", cleaned).strip().lower()

    # Must BEGIN with SELECT or WITH (CTEs allowed)
    if not (normalized.startswith("select") or normalized.startswith("with")):
        raise ValueError("Only read-only SELECT queries are allowed.")

    # Token-level detection prevents false positives
    tokens = set(re.findall(r"\b[a-z_]+\b", normalized))

    forbidden = WRITE_KEYWORDS.intersection(tokens)
    if forbidden:
        raise ValueError(f"Forbidden operation detected: {', '.join(sorted(forbidden))}")

# -----------------------------------
# MCP TOOL — READ ONLY SQL ACCESS
# -----------------------------------

@mcp.tool()
async def run_select_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute a SAFE read-only SQL query.

    Supports:
    - Multiline SQL
    - WITH CTEs
    - Joins, windows, aggregations
    - Comments

    Blocks:
    - Any mutation or DDL
    - PRAGMA / transaction control
    - Multi-statements
    """

    try:
        validate_query(query)

        conn = get_connection()
        cur = conn.execute(query)

        rows = cur.fetchmany(MAX_RETURN_ROWS)
        result = [dict(r) for r in rows]

        conn.close()
        return result

    except Exception as e:
        raise ValueError(f"Query failed: {str(e)}")

# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI(title="University SQL MCP Server")

@app.get("/")
async def root():
    return {"status": "running"}

# -----------------------------------
# SCHEMA ENDPOINT (LLM-Friendly Markdown)
# -----------------------------------

@app.get("/schema", response_class=Response)
async def get_database_schema():

    SAMPLE_LIMIT = 5
    LOW_CARDINALITY_THRESHOLD = 25
    MAX_PROFILE_ROWS = 200_000

    try:
        conn = get_connection()
        cur = conn.cursor()

        tables = cur.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """).fetchall()

        md: list[str] = []
        md.append("# Database Semantic Schema (LLM Optimized)\n")

        for (table,) in tables:
            md.append(f"## Table: `{table}`\n")

            row_count = cur.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
            md.append(f"**Row Count:** {row_count}\n")

            cols = cur.execute(f'PRAGMA table_info("{table}")').fetchall()

            md.append("| Column | Type | PK | Nullable |")
            md.append("|--------|------|----|----------|")

            for c in cols:
                md.append(
                    f"| {c[1]} | {c[2] or '—'} | {bool(c[5])} | {not bool(c[3])} |"
                )

            md.append("")

            fks = cur.execute(f'PRAGMA foreign_key_list("{table}")').fetchall()
            if fks:
                md.append("**Relationships:**")
                for fk in fks:
                    md.append(f"- `{table}.{fk[3]}` → `{fk[2]}.{fk[4]}`")
                md.append("")

            md.append("---\n")

        conn.close()
        return Response("\n".join(md), media_type="text/markdown")

    except Exception as e:
        raise HTTPException(500, str(e))

# -----------------------------------
# MCP SSE Bridge
# -----------------------------------

def create_mcp_sse_app(mcp_instance: FastMCP):
    transport = SseServerTransport("/messages/")

    async def handle_sse_connection(request: Request):
        async with transport.connect_sse(
            request.scope, request.receive, request._send
        ) as (read_stream, write_stream):

            await mcp_instance._mcp_server.run(
                read_stream,
                write_stream,
                mcp_instance._mcp_server.create_initialization_options(),
            )

    routes = [
        Route("/sse/", endpoint=handle_sse_connection, methods=["GET"]),
        Mount("/messages/", app=transport.handle_post_message),
    ]

    return Starlette(routes=routes)

app.mount("/mcp", create_mcp_sse_app(mcp))
