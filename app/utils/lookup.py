import hmac
import hashlib
from app.utils.key_manager import HMAC_KEY


def encrypt_hash(data:str)->str:

    if data is None:
        return None

    # Normalize data
    normalized_data = data.strip().lower()

    # Create HMAC-SHA256
    search_hash = hmac.new(
        HMAC_KEY,
        normalized_data.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return search_hash