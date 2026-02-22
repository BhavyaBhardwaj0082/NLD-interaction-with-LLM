# Natural Language to SQL

## Instructions

### 1. Setup Environment
```/dev/null/sh#L1-2
export GOOGLE_GENAI_USE_VERTEXAI=0
export GOOGLE_API_KEY=your_google_api_key
```

### 2. Install Dependencies
```/dev/null/sh#L1-1
pip install -r requirements.txt
```

### 3. Run MCP Server
```/dev/null/sh#L1-1
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### 4. Run ADK Agent
In a new terminal (from root directory):
```/dev/null/sh#L1-1
adk web
```

### 5. Check Schema (Optional)
```/dev/null/sh#L1-1
curl http://0.0.0.0:8080/schema > sqluniversity_schema.md
```

---

For agent behavior and role, see `Bottle_N2Q/prompt.py`.
