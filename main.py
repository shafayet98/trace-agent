from dotenv import load_dotenv
load_dotenv()

from awslabs.mcp_lambda_handler import MCPLambdaHandler
from tools.extract import extract_receipt
from tools.expenses import save_expense, get_expenses, get_summary
from tools.budget import set_budget, check_budget

mcp = MCPLambdaHandler(name="Trace Agent", version="1.0.0")

mcp.tool()(extract_receipt)
mcp.tool()(save_expense)
mcp.tool()(get_expenses)
mcp.tool()(get_summary)
mcp.tool()(set_budget)
mcp.tool()(check_budget)

def lambda_handler(event, context):
    return mcp.handle_request(event, context)