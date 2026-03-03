import logging

from utils.settings import settings

logging.basicConfig(
    filename=settings.logging.path,
    level=logging.getLevelName(settings.logging.level),
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)
