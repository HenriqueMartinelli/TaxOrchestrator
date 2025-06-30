import polars as pl
from fastapi import UploadFile, BackgroundTasks

from app.infrastructure.pipeline.excel.excel_reader import ExcelReaderFactory
from app.infrastructure.pipeline.polars.polars_processor import PolarsProcessor
from app.infrastructure.database.mongo.orders_repository import OrdersRepository
from app.schemas.order_dto import ProcessResponseDTO
from app.shared.exceptions import SchemaValidationError, DataPreparationError
from app.core.logging import logger

from app.infrastructure.messaging.event_bus import EventBus

class ProcessOrdersUseCase:
    def __init__(
        self,
        reader_factory: ExcelReaderFactory,
        processor: PolarsProcessor,
        repo: OrdersRepository
    ):
        self.reader_factory = reader_factory
        self.processor = processor
        self.repo = repo

    async def execute(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks
    ) -> ProcessResponseDTO:
        logger.info("Start processing: %s", file.filename)

        reader = self.reader_factory.get_reader(file.filename)
        try:
            logger.info("Reading file with reader: %s", reader.__class__.__name__)
            df_pd = await reader.read(file)
        except SchemaValidationError as e:
            logger.error(f"Schema validation failed: {e}")
            raise

        try:
            logger.info("Converting DataFrame to LazyFrame")
            lazy_df = pl.from_pandas(df_pd).lazy()
        except Exception as e:
            logger.error("Failed to convert DataFrame to LazyFrame", exc_info=True)
            raise DataPreparationError("Error preparing data for processing")

        def _bg_task():
            try:
                logger.info("Starting background processing")
                records = self.processor.process(lazy_df)
                self.repo.insert_many(records)
                EventBus.publish("order.processed", {
                    "order_count": len(records),
                    "first_order_id": records[0]["order_id"]
                })
            except Exception as e:
                EventBus.publish("order.failed", {
                    "error": str(e),
                    "file": file.filename
                })
                logger.error(f"Background processing failed: {e}", exc_info=True)

        background_tasks.add_task(_bg_task)
        return ProcessResponseDTO(message="Processing started")
