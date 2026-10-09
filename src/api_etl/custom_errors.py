class ETLErrors(Exception):
    """Base exception for expected ETL failures."""

class ExtractionError(ETLErrors):
    """Raised when source data cannot be extracted."""

class TransformationError(ETLErrors):
    """Raised when raw data cannot be read or transformed."""

class DatabaseConnectionError(ETLErrors):
    """Raised when a database connection cannot be established."""

class DatabaseOperationError(ETLErrors):
    """Raised when a database operation fails."""

class ConfigurationError(ETLErrors):
    """Raised when required configuration is missing."""
