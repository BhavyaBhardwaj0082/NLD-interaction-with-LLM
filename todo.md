# Experiment 5

## Natural Language Database Interaction with LLMs and MCP

### Objective:
To interact with databases using natural language queries powered by LLMs. Detailed Procedure:
- 1. Set up a MySQL/MongoDB database and populate it with sample data.
- 2. Integrate an LLM to convert natural language queries into SQL commands using MCP. (What do u mean MCP its protocol idiot)(could have just used simple tool to do the same waste)
- 3. Develop a Flask backend to interact with the database. (contradiction with point 2) (vague unclear)
- 4. Create a frontend for users to enter queries and view results. Reference: From Plain English to MongoDB:
    - Building a Natural Language
    - Database Interface with MCP | Charisol Pulse


```json
                Schema
                  ↓↓
user_query -> ( [Agent -> query -> MCP] -> <- [DB] ) -> response
```
## TODO
- (✔️) setup virtual Environment
- (✔️) Setup ADK Environment
- (✔️) Setup MCP Client
- (✔️) connect MCP as tool
