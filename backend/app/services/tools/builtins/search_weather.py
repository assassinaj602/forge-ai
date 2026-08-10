from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.services.tools.base import BaseTool

class WebSearchArgs(BaseModel):
    query: str = Field(..., description="Search query string")
    max_results: Optional[int] = Field(3, description="Maximum number of search results to return")

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Searches the web for up-to-date information on a given topic."
    args_schema = WebSearchArgs

    async def execute(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        # Simulated search result provider
        results = [
            {
                "title": f"Search Result 1 for '{query}'",
                "snippet": f"Detailed technical insights about {query} from search provider.",
                "url": f"https://example.com/search?q={query}"
            },
            {
                "title": f"Documentation: {query}",
                "snippet": f"Official developer reference guide for {query}.",
                "url": f"https://docs.example.com/{query}"
            }
        ]
        return {"query": query, "results": results[:max_results]}

class WeatherArgs(BaseModel):
    location: str = Field(..., description="City or region name, e.g. 'San Francisco, CA'")

class WeatherTool(BaseTool):
    name = "weather_search"
    description = "Fetches current weather conditions and forecasts for a specified location."
    args_schema = WeatherArgs

    async def execute(self, location: str) -> Dict[str, Any]:
        return {
            "location": location,
            "temperature": "22°C / 71°F",
            "condition": "Sunny with clear skies",
            "humidity": "45%",
            "wind_speed": "12 km/h"
        }
