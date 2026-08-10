from datetime import datetime, timezone
from typing import Dict, Any
from pydantic import BaseModel, Field
from app.services.tools.base import BaseTool

class CalculatorArgs(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate, e.g., '12 * 45 + 100'")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Safely evaluates basic mathematical arithmetic expressions."
    args_schema = CalculatorArgs

    async def execute(self, expression: str) -> Dict[str, Any]:
        try:
            # Safe restricted mathematical evaluation
            allowed_chars = "0123456789+-*/(). "
            if not all(c in allowed_chars for c in expression):
                return {"error": "Invalid characters in mathematical expression"}
            result = eval(expression, {"__builtins__": {}})
            return {"expression": expression, "result": result}
        except Exception as e:
            return {"error": f"Evaluation error: {str(e)}"}

class DateTimeArgs(BaseModel):
    timezone_name: str = Field("UTC", description="Timezone name, default 'UTC'")

class DateTimeTool(BaseTool):
    name = "current_datetime"
    description = "Returns current date, time, and UTC timestamp information."
    args_schema = DateTimeArgs

    async def execute(self, timezone_name: str = "UTC") -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "iso_timestamp": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "timezone": timezone_name
        }
