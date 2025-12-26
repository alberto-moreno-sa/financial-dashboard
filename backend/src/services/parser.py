import json
import pandas as pd
from fastapi import UploadFile, HTTPException

class PortfolioParser:
    @staticmethod
    async def parse_json(file: UploadFile) -> dict:
        if file.content_type != "application/json":
            raise HTTPException(400, "JSON required")
        content = await file.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise HTTPException(400, "Invalid JSON")