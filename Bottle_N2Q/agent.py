from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from Bottle_N2Q.prompt import bottle_instructions


connection_params = SseConnectionParams(
    url="http://127.0.0.1:8080/mcp/sse/",   # ← MUST match server exactly
    headers={}                              # no auth needed unless you add it
)

mcp_tools = MCPToolset(
    connection_params=connection_params,
    tool_filter=["run_select_query"]
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="bottle",
    description="You are bottle a data analyst , whose job is to take in natural language query from user , write sql query to gather and generate insgihts and respond the relevent query",
    instruction=bottle_instructions,
    tools=[mcp_tools],
)
