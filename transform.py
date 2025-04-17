from datetime import datetime, timezone
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def transform_animal(animal: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # split friends into a list
        friends_str = animal.get("friends", "")
        friends_list = (
            [f.strip() for f in friends_str.split(",") if f.strip()]
            if friends_str
            else []
        )

        # convert born_at to ISO 8601 UTC format if not None
        born_at = animal.get("born_at")
        born_at_iso = (
            datetime.fromtimestamp(born_at / 1000, tz=timezone.utc).isoformat()
            if born_at is not None
            else None
        )

        return {
            "id": animal["id"],
            "name": animal["name"],
            "friends": friends_list,
            "born_at": born_at_iso,
        }
    except KeyError as e:
        logger.error(f"Missing key in animal data: {e}. Full data: {animal}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error transforming animal data: {e}")
        return None
