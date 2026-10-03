class ETLErrors(Exception):
    pass

class ExtractionError(ETLErrors):
    pass

class FileNotFoundError(ETLErrors):
    pass