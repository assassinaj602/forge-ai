from abc import ABC, abstractmethod
from typing import Dict, Any, Type
from pydantic import BaseModel, Field

class BaseTool(ABC):
    name: str
    description: str
    args_schema: Type[BaseModel]

    def get_json_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.args_schema.model_json_schema()
            }
        }

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        pass
