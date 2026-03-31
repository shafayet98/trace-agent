from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from tools.extract import extract_receipt
from tools.expenses import save_expense, get_expenses, get_summary
from tools.budget import set_budget, check_budget


mcp = FastMCP("Trace Agent")

# registering tools here:
mcp.tool()(extract_receipt)
mcp.tool()(save_expense)
mcp.tool()(get_expenses)
mcp.tool()(get_summary)
mcp.tool()(set_budget)
mcp.tool()(check_budget)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=8000)
