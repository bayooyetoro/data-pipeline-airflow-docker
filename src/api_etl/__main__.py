from api_etl.utils import *
from api_etl.extract import *
from api_etl.custom_errors import *



url="https://jsonplaceholder.typicode.com/users"
logger = get_logger(__name__)

def main():
    try:
        logger.info("Extraction Starting ....")
        fetch_data_from_api(url)
        logger.info("Extraction Completed!")
    except Exception as e:
        raise ExtractionError(f"Extraction failed: {e}")

if __name__ == "__main__":
    main()
