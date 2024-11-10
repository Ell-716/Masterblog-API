import requests
import time


def test_rate_limit(url, max_requests=12, delay=5):
    """
    Test API rate limiting by sending multiple requests.

    :param url: The API endpoint to send requests to.
    :param max_requests: Total number of requests to send.
    :param delay: Time to wait between requests (in seconds).
    """
    for i in range(max_requests):
        response = requests.get(url)

        if response.status_code == 200:
            print(f"Request {i + 1} succeeded: {response.json()}")
        elif response.status_code == 429:
            print(f"Request {i + 1} failed (Rate limit exceeded): {response.json()}")
        else:
            print(f"Request {i + 1} failed with status: {response.status_code}")

        # Wait before sending the next request
        time.sleep(delay)


# Example usage
api_url = "http://127.0.0.1:5002/api/posts"
test_rate_limit(api_url)
