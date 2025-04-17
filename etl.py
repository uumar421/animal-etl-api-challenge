import logging
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from api_client import get_animals_page, get_animal_detail, post_animals_home
from transform import transform_animal

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def run_etl() -> None:
    logger.info("Starting ETL process...")
    page = 1
    all_transformed: List[Dict[str, Any]] = []

    while True:
        logger.info(f"Fetching page {page}")
        data = get_animals_page(page)
        items = data.get("items", [])
        total_pages = data.get("total_pages", page)

        if not items:
            break
        
        # parrallelism using thread pool to extract data concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_id = {executor.submit(get_animal_detail, item["id"]): item["id"] for item in items}
            for future in as_completed(future_to_id):
                try:
                    detail = future.result()
                    transformed = transform_animal(detail)
                    all_transformed.append(transformed)

                    # post in batches of 100
                    if len(all_transformed) >= 100:
                        logger.info("Posting batch of 100 animals")
                        post_animals_home(all_transformed[:100])
                        all_transformed = all_transformed[100:]
                except Exception as e:
                    logger.exception(f"Failed to process animal {future_to_id[future]}: {e}")

        if page >= total_pages:
            break
        page += 1

    # send any remaining animals
    if all_transformed:
        logger.info(f"Posting final batch of {len(all_transformed)} animals")
        post_animals_home(all_transformed)

    logger.info("ETL process completed")