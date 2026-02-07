import sys
import time
import requests

NGINX_HOST = "http://nginx"
HTML_PORT = 8080
ERROR_PORT = 8081


def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)


def test_html_server():
    url = f"{NGINX_HOST}:{HTML_PORT}"
    r = requests.get(url)

    if r.status_code != 200:
        fail(f"HTML server returned {r.status_code}, expected 200")

    if "Nginx is running" not in r.text:
        fail("HTML content is not as expected")

    print("[OK] HTML server test passed")


def test_error_server():
    url = f"{NGINX_HOST}:{ERROR_PORT}"
    r = requests.get(url)

    if r.status_code != 500:
        fail(f"Error server returned {r.status_code}, expected 500")

    print("[OK] Error server test passed")


def test_rate_limit():
    url = f"{NGINX_HOST}:{HTML_PORT}"

    import concurrent.futures

    def send_request():
        return requests.get(url).status_code

    status_codes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(send_request) for _ in range(20)]
        for future in concurrent.futures.as_completed(futures):
            status_codes.append(future.result())

    if 429 not in status_codes:
        fail(f"Rate limiting not triggered, status codes: {status_codes}")

    print("[OK] Rate limiting test passed")

if __name__ == "__main__":
    # Give nginx a moment to start
    time.sleep(3)

    test_html_server()
    test_error_server()
    test_rate_limit()

    print("\nAll tests passed ✔")
    sys.exit(0)
