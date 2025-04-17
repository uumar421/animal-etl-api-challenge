# creating an api_client handler using retry decoraters for fault-tolerance
import requests
from typing import Any, Dict, List
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

BASE_URL = "http://localhost:3123"

"""
Custom exception handling to flag only retry-worthy HTTP errors and avoid retrying 
on other issues like 404 or bad input.
"""
RETRY_STATUS_CODES = {500, 502, 503, 504}

class TransientAPIError(Exception):
    pass

def is_transient_error(exception: Exception) -> bool:
    return isinstance(exception, requests.HTTPError) and exception.response.status_code in RETRY_STATUS_CODES

@retry(
    wait=wait_random_exponential(multiplier=1, max=20),  # wait time increases exponentially 
    stop=stop_after_attempt(5),                          # stop retrying after 5 attempts
    retry=retry_if_exception_type((TransientAPIError, requests.exceptions.ReadTimeout)),    # only retry if a TransientAPIError is raised
    reraise=True                                         # raise final error if all retries fail
)
def get_animals_page(page: int) -> Dict[str, Any]:
    try:
        response = requests.get(f"{BASE_URL}/animals/v1/animals?page={page}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code in RETRY_STATUS_CODES:
            raise TransientAPIError() from e
        raise

@retry(
    wait=wait_random_exponential(multiplier=1, max=20),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((TransientAPIError, requests.exceptions.ReadTimeout)),
    reraise=True
)
def get_animal_detail(animal_id: str) -> Dict[str, Any]:
    try:
        response = requests.get(f"{BASE_URL}/animals/v1/animals/{animal_id}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code in RETRY_STATUS_CODES:
            raise TransientAPIError() from e
        raise

@retry(
    wait=wait_random_exponential(multiplier=1, max=20),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type(TransientAPIError),
    reraise=True
)
def post_animals_home(data_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    try:
        response = requests.post(f"{BASE_URL}/animals/v1/home", json=data_batch, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code in RETRY_STATUS_CODES:
            raise TransientAPIError() from e
        raise