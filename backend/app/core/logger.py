import logging
import os

from app.core.config import settings

os.makedirs(settings.LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(
        settings.LOG_DIR,
        "jalnetra.log"
    ),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("JalNetra")