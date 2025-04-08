# creating an api_client handler using retry decoraters for fault-tolerance
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt

BASE_URL = "http://localhost:3123"

@retry(wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(2))
def get_animals_page(page):
    response = requests.get(f"{BASE_URL}/animals/v1/animals?page={page}")
    response.raise_for_status()
    return response.json()

@retry(wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(2))
def get_animal_detail(animal_id):
    response = requests.get(f"{BASE_URL}/animals/v1/animals/{animal_id}")
    response.raise_for_status()
    return response.json()

@retry(wait=wait_random_exponential(multiplier=1, max=10), stop=stop_after_attempt(2))
def post_animals_home(data_batch):
    response = requests.post(f"{BASE_URL}/animals/v1/home", json=data_batch)
    response.raise_for_status()
    return response.json()