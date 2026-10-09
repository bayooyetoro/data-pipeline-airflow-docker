import json
from pathlib import Path
from api_etl.custom_errors import TransformationError
from api_etl.utils import get_logger

RAW_DIR = Path(__file__).resolve().parent.parent.parent /"data"
logger = get_logger(__name__)


def transform_raw_data():
    raw_data = RAW_DIR.resolve() / "raw_data.json"
    cleaned_data = []
    try:
        if not raw_data.is_file():
            raise TransformationError(f"Raw data file not found: {raw_data}")
        else:
            with raw_data.open("r", encoding="utf-8") as f:
                raw_file = json.load(f)
                for item in raw_file:
                    address = (
                        f"{item.get('address', {}).get('street', "")} "
                        f"{item.get('address', {}).get('suite', "")} "
                        f"{item.get('address', {}).get('city', "")}, "
                        f"{item.get('address', {}).get('zipcode', "")}"
                    )

                    record = (
                        item.get("id"),
                        str(item.get("name", "")).strip(),
                        str(item.get("username", "")).strip().lower(),
                        str(item.get("email", "")).strip().lower(),
                        address,
                        item.get("address", {}).get("geo", {}).get("lat"),
                        item.get("address", {}).get("geo", {}).get("lng"),
                        item.get("phone", ""),
                        str(f'https://www.{item.get("website", "").lower().strip()}'),
                        item.get("company", {}).get("name", "")
                    )

                    if record[0] is not None:
                        cleaned_data.append(record)

                logger.info(f"Successfully transformed {len(cleaned_data)} records.")
                return cleaned_data

    except TransformationError:
        raise
    except (OSError, json.JSONDecodeError, TypeError, AttributeError) as exc:
        raise TransformationError(f"Failed to transform {raw_data}: {exc}") from exc
