import polars as pl
from datetime import datetime
import pandas as pd
from app.infrastructure.pipeline.excel.excel_reader import ExcelReaderFactory

def load_tax_rules() -> pl.DataFrame:
    import json
    from app.core.config import settings
    with open(settings.tax_rates_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pl.DataFrame(data)

class PolarsProcessor:
    def process(self, lazy_df: pl.LazyFrame) -> list[dict]:
        from app.services.tax_calculator import TaxCalculatorFactory
        df = TaxCalculatorFactory.get_strategy().apply(lazy_df)

        agg = (
            df.group_by("order_id")
              .agg([
                  pl.struct([
                      "product_id", "product_name","quantity", 
                      "unit_price", "ibs_rate", "cbs_rate",
                      "value_ibs_item", "value_cbs_item"
                  ]).alias("items"),
                  (pl.col("unit_price") * pl.col("quantity")).sum().alias("gross_total"),
                  pl.col("value_ibs_item").sum().alias("total_ibs"),
                  pl.col("value_cbs_item").sum().alias("total_cbs")
              ])
              .with_columns([
                  (pl.col("gross_total") + pl.col("total_ibs") + pl.col("total_cbs"))
                      .alias("order_total"),
                    pl.lit(datetime.utcnow()).alias("calculation_date"),
                    pl.lit("PROCESSED").alias("processing_status")
                ])
        )
        result = agg.collect()
        return result.to_dicts()
