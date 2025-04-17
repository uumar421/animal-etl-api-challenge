import requests
from unittest.mock import patch, Mock
from api_client import get_animal_detail, TransientAPIError

def test_retry_on_failure():
    # check whether the retry mechanism actually retries on failure
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError(response=Mock(status_code=500))

    with patch("api_client.requests.get", return_value=mock_response) as mock_get:
        try:
            get_animal_detail("1")
        except TransientAPIError:
            pass

        assert mock_get.call_count >= 2