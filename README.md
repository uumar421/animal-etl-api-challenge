# Animal ETL API Challenge

This project implements an ETL (Extract, Transform, Load) pipeline that interacts with a Dockerized HTTP API providing animal data.

## Overview

The API exposes endpoints to:
- Fetch paginated lists of animals
- Fetch details of individual animals
- POST batches of transformed animal data

This script fetches all animals, transforms the data, and posts it in batches of up to 100.

## Technologies Used

- Python 3.10+
- `requests` for API communication
- `concurrent.futures` for parallelism
- `pytest` for testing
- `flake8` for linting
- GitHub Actions for CI
- Docker (for the API server)

## Project Structure

```
animal-etl-api-challenge/
├── main.py                  # Entry point for the flow
├── etl.py                   # Handles the full ETL flow
├── api_client.py            # Handler for fault tolerance
├── transform.py             # Transformation logic for animal records
├── requirements.txt         # Dependencies list
├── .github/workflows/ci.yml # GitHub Actions config for linting and tests
├── tests/                   # Unit tests
├── pytest.ini               # Pytest configuration
└── README.md                # Project documentation
```

## How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/animal-etl-api-challenge.git
cd animal-etl-api-challenge
```

### 2. Install Dependencies

To set up the project, setup a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the Docker Server

Download and run the container:

```bash
docker load -i lp-programming-challenge-1-1625758668.tar.gz
docker run --rm -p 3123:3123 -ti lp-programming-challenge-1
```

Make sure the API is accessible at:
http://localhost:3123/docs

### 4. Run the Entry Point

```bash
python main.py
```

You should see logs showing:
- API requests and pagination
- Uploads to /animals/v1/home

## Transformations Applied

Each animal record is transformed before being uploaded:

- **`friends`**: Converted from a comma-delimited string to a list of names.  
  **Example:** "Cat,Dog" → ["Cat", "Dog"]

- **`born_at`**: Converted from epoch milliseconds to an ISO 8601 UTC timestamp.  
  **Example:** 1654571943094 → "2022-06-06T12:39:03Z"

## Running Tests

Make sure your PYTHONPATH is set correctly (this is auto-handled via pytest.ini):
```bash
pytest tests/
```

## Linting with Flake8

Check code formatting:
```bash
flake8 .
```

## CI with GitHub Actions

This repo includes a GitHub Actions workflow (.github/workflows/ci.yml) that:
- Runs flake8 to ensure code style compliance
- Runs pytest to verify unit tests
- Fails the workflow if either fails
To prevent code pushes with style errors, use pre-commit hooks or rely on CI failures for pull requests.


## Notes

- The ETL process handles retryable API errors (500, 502, 503, 504) with exponential backoff.
- It uses threading for concurrent data extraction to reduce latency.