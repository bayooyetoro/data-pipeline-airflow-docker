from api_etl.utils import get_logger
from api_etl.extract import fetch_data_from_api
from api_etl.transform import transform_raw_data
from api_etl.load import connect_to_db, create_table, load_database

url="https://jsonplaceholder.typicode.com/users"
logger = get_logger(__name__)


def main():
    db_conn = None
    try:
        logger.info("Extraction starting")
        fetch_data_from_api(url)

        transformed_data = transform_raw_data()

        db_conn = connect_to_db()
        create_table(db_conn)
        load_database(db_conn, transformed_data)

        logger.info("ETL completed")
    except Exception:
        logger.exception("ETL job failed")
        raise
    finally:
        if db_conn is not None:
            db_conn.close()

if __name__ == "__main__":
    main()
