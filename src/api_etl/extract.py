import requests
import json
from api_etl.utils import get_logger
from typing import Dict, Any
from pathlib import Path

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

    api_response = requests.get(url, headers=headers, timeout=20)
    api_response.raise_for_status()
    api_data = api_response.json()

    with open(RAW_FILE, 'w') as f:
        json.dump(api_data, f, indent=2)
        
    logger.info(f"Successfully extracted {len(api_data)} records.")

    return api_data
