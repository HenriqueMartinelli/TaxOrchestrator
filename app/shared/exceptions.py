class SchemaValidationError(Exception):
    """Planilha Excel não atende ao esquema esperado."""

class ProcessingError(Exception):
    """Erro genérico no processamento do pipeline."""

class DataPreparationError(Exception):
    """Erro no pré-processamento de dados para Polars."""
