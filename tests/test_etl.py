from unittest.mock import patch
from etl import run_etl


def test_etl_happy_path():
    # simulate a successful end-to-end ETL run by mocking all external APIs
    with patch("etl.get_animals_page") as mock_page, patch(
        "etl.get_animal_detail"
    ) as mock_detail, patch("etl.post_animals_home") as mock_post:

        mock_page.return_value = {"items": [{"id": 1}], "total_pages": 1}
        mock_detail.return_value = {
            "id": 1,
            "name": "A",
            "friends": "B,C",
            "born_at": 1234567890000,
        }
        mock_post.return_value = {}

        run_etl()
        mock_post.assert_called()
