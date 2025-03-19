import logging
import json
from datetime import datetime

# Loggerin konfigurointi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log.json", mode="a", encoding="utf-8"),
        
        # Jos haluaa myös komentoriville niin poista alempi kommentti
        # logging.StreamHandler()
    ]
)

logger = logging.getLogger("application_logger")

# Yhteinen logitusfunktio
def log_event(status: str, description: str, request=None, error_details: str = None):
    log_entry = {
        "status": status,
        "description": description,
        "method": request.method if request else "SYSTEM",
        "url": str(request.url) if request else "SYSTEM",
        "client": request.client.host if request and request.client else "unknown",
        "error_details": error_details
    }
    logger.info(json.dumps(log_entry, ensure_ascii=False))
