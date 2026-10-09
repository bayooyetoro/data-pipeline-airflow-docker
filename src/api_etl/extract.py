import requests
import json
from api_etl.utils import get_logger
from typing import Dict, Any
from pathlib import Path
from api_etl.custom_errors import ExtractionError

RAW_FILE = Path(__file__).resolve().parent.parent.parent /"data/raw_data.json"
logger = get_logger(__name__)

def fetch_data_from_api(url:str, token=None) -> list[Dict[str, Any]]:
    """Fetches data from an API endpoint

    Parameters:
        url(str): the url link
        token(str, optional): the token key needed for api auth

    Returns:
        api_dataset(json): the dataset fetched from the api endpoint
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    try:
        api_response = requests.get(url, headers=headers, timeout=20)
        api_response.raise_for_status()
        api_data = api_response.json()

        RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
        with RAW_FILE.open("w", encoding="utf-8") as raw_file:
            json.dump(api_data, raw_file, indent=2)
    except (requests.RequestException, ValueError, OSError) as exc:
        raise ExtractionError(f"Failed to extract API data: {exc}") from exc

    logger.info("Successfully extracted %s records.", len(api_data))
    return api_data
