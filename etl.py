from api_client import get_animals_page, get_animal_detail, post_animals_home
from transform import transform_animal

def run_etl():
    print("Starting ETL process...")
    page = 1
    all_transformed = []

    while True:
        print(f"Fetching page {page}")
        data = get_animals_page(page)
        items = data["items"]

        if not items:
            break

        for item in items:
            detail = get_animal_detail(item["id"])
            transformed = transform_animal(detail)
            all_transformed.append(transformed)

            # post in batches of 100
            if len(all_transformed) >= 100:
                print("Posting batch of 100")
                post_animals_home(all_transformed[:100])
                all_transformed = all_transformed[100:]

        if page >= data["total_pages"]:
            break
        page += 1

    # send any remaining animals
    if all_transformed:
        print(f"Posting final batch of {len(all_transformed)}")
        post_animals_home(all_transformed)

    print("ETL process completed.")