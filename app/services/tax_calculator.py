import polars as pl

class TaxStrategy:
    def apply(self, df: pl.LazyFrame) -> pl.LazyFrame:
        raise NotImplementedError

class DefaultTaxStrategy(TaxStrategy):
    def __init__(self, rates_df: pl.LazyFrame):
        self.rates_df = rates_df

    def apply(self, df: pl.LazyFrame) -> pl.LazyFrame:
        return (
            df.join(
                self.rates_df,
                on=["product_type", "category_fiscal", "origin_state", "destination_state"],
                how="left"
            )
            .with_columns([
                (pl.col("unit_price") * pl.col("quantity") * pl.col("ibs_rate"))
                    .alias("value_ibs_item"),
                (pl.col("unit_price") * pl.col("quantity") * pl.col("cbs_rate"))
                    .alias("value_cbs_item")
            ])
        )

class TaxCalculatorFactory:
    @staticmethod
    def get_strategy() -> TaxStrategy:
        from app.infrastructure.pipeline.polars.polars_processor import load_tax_rules
        rates_df = load_tax_rules().lazy()
        return DefaultTaxStrategy(rates_df)
