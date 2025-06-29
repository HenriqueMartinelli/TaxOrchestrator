import pandas as pd
from fastapi import UploadFile
from io import BytesIO
from app.shared.exceptions import SchemaValidationError

class ExcelReader:
    REQUIRED_COLUMNS = [
        "order_id", "product_id", "quantity", "unit_price",
        "product_type", "category_fiscal", "origin_state", "destination_state"
    ]

    async def read(self, file: UploadFile) -> pd.DataFrame:
        data = await file.read()
        df = pd.read_excel(BytesIO(data))
        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise SchemaValidationError(f"Missing columns: {missing}")
        return df

class ExcelReaderFactory:
    def get_reader(self, filename: str) -> ExcelReader:
        return ExcelReader()
