import requests
import time
import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def cache_and_track(func):
    def wrapper(url):
        # Check if URL is cached
        cached_html = redis_client.get(f"html:{url}")
        if cached_html:
            # URL is cached, return cached HTML
            return cached_html.decode('utf-8')

        # URL is not cached, fetch HTML content
        response = requests.get(url)
        html_content = response.text

        # Cache HTML content with expiration time of 10 seconds
        redis_client.setex(f"html:{url}", 10, html_content)

        # Track URL access count
        redis_client.incr(f"count:{url}")

        return html_content
    return wrapper


@cache_and_track
def get_page(url):
    return requests.get(url).text


if __name__ == "__main__":
    # Test the get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.google.com"
    start_time = time.time()
    html_content = get_page(url)
    end_time = time.time()
    print("HTML content:", html_content)
    print("Time taken:", end_time - start_time, "seconds")
