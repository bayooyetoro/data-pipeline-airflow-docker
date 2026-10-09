import psycopg2
import os
from api_etl.utils import get_logger
from api_etl.custom_errors import ConfigurationError, DatabaseConnectionError, DatabaseOperationError

logger = get_logger(__name__)

def _required_env(name):
    value = os.getenv(name)
    if not value:
        raise ConfigurationError(f"Required environment variable {name} is not set")
    return value


def connect_to_db():
    try:
        return psycopg2.connect(
            host=_required_env("APP_DB_HOST"),
            port=os.getenv("APP_DB_PORT", "5432"),
            dbname=_required_env("APP_DB_NAME"),
            user=_required_env("APP_DB_USER"),
            password=_required_env("APP_DB_PASSWORD"),
        )
    except ConfigurationError:
        raise
    except psycopg2.Error as exc:
        raise DatabaseConnectionError(f"Failed to connect to the database: {exc}") from exc

def create_table(conn):
    try:
        print("Creating Table and Schema ... ")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE SCHEMA IF NOT EXISTS gold;

            CREATE TABLE IF NOT EXISTS gold.users_tbl (
                uuid SERIAL PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                user_name TEXT,
                email TEXT,
                address TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                phone_no TEXT,
                website TEXT,
                company TEXT,
                inserted_at TIMESTAMP DEFAULT NOW()
            );
            """
        )
        conn.commit()
        cursor.close()
        print("USERS_TBL table created successfully!")
    except psycopg2.Error as exc:
        conn.rollback()
        raise DatabaseOperationError(f"Unable to create the table and schema: {exc}") from exc

def load_database(conn, data):
    try:
        logger.info("Ingesting data into the database ...")

        cursor = conn.cursor()

        sql = """
        INSERT INTO gold.users_tbl (
            user_id,
            user_name,
            email,
            address,
            latitude,
            longitude,
            phone_no,
            website,
            company
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
            user_name = EXCLUDED.user_name,
            email = EXCLUDED.email,
            address = EXCLUDED.address,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            phone_no = EXCLUDED.phone_no,
            website = EXCLUDED.website,
            company = EXCLUDED.company;
        """

        records = [
            (
                row[0],              # user_id
                row[1],              # user_name
                row[3],              # email
                row[4],              # address
                float(row[5]),       # latitude
                float(row[6]),       # longitude
                row[7],              # phone_no
                row[8],              # website
                row[9],              # company
            )
            for row in data
        ]

        cursor.executemany(sql, records)

        conn.commit()
        cursor.close()

        logger.info(f"{len(records)} records upserted successfully")

    except (psycopg2.Error, TypeError, ValueError) as exc:
        conn.rollback()
        raise DatabaseOperationError(f"Failed to load database: {exc}") from exc

    finally:
        if "cursor" in locals() and not cursor.closed:
            cursor.close()
