import json
from pathlib import Path
from api_etl.custom_errors import FileNotFoundError, ETLErrors

RAW_DIR = Path(__file__).resolve().parent.parent.parent /"data"

def transform_raw_data(file_name):
    raw_data = RAW_DIR.resolve() / file_name
    try:
        if not raw_data:
            raise FileNotFoundError("Raw File Not found!")
        else:
            with open(raw_data, "r") as f:
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
                        str(item.get("website", "")).lower().strip(),
                        item.get("company", {}).get("name", "")
                    )

                    if record[0] is not None:
                        yield record
                    
    except Exception as e:
        print(f"Error Ocurred with Transformation: {e}")