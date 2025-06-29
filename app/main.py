import uvicorn
from fastapi import FastAPI

from app.routers.api import router as orders_router
from app.core.logging import logger

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.shared.exceptions import DataPreparationError, SchemaValidationError
import app.infrastructure.messaging.event_handlers  


app = FastAPI(
    title="Order Tax Processing Service",
    version="1.0.0",
    description="Microservice for ingesting Excel orders, calculating IBS/CBS taxes and persisting to MongoDB",
)


@app.exception_handler(SchemaValidationError)
async def schema_exception_handler(request: Request, exc: SchemaValidationError):
    return JSONResponse({"detail": str(exc)}, status_code=400)

@app.exception_handler(DataPreparationError)
async def data_prep_exception_handler(request: Request, exc: DataPreparationError):
    return JSONResponse({"detail": str(exc)}, status_code=500)

app.include_router(orders_router)

if __name__ == "__main__":
    logger.info("Starting Order Tax Processing Service...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
