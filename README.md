# devops-home-assignment

## Overview
This project builds an Ubuntu-based Nginx container with two HTTP endpoints:

- `http://localhost:8080` serves a static HTML page and enforces per-IP rate limiting.
- `http://localhost:8081` always returns a `500 Internal Server Error` response.

A self-signed TLS certificate is also included and an HTTPS server is configured to listen on port `443` inside the container, though it is not published by default in `docker-compose.yml`.

## Implementation Details

- **Base image**: `ubuntu:22.04` (per assignment requirement).
- **Nginx configuration**: `nginx/nginx.conf` defines a `limit_req_zone` (5 requests/sec per IP).
- **Server blocks**:
  - `nginx/sites/html.conf`: listens on `8080`, serves `nginx/html/index.html`, uses `limit_req` with `burst=1` and `limit_req_status 429`.
  - `nginx/sites/error.conf`: listens on `8081`, returns a `500` with a short message.
  - `nginx/sites/https.conf`: listens on `443` with a self-signed cert from `nginx/certs/`.
- **Tests**: `tests/test_nginx.py` validates HTML response, 500 response, and rate limiting using a Python test container.

## Design Notes

- **Ubuntu base**: required by the assignment, even though a slimmer Nginx image exists; size is reduced by cleaning `apt` lists.
- **Single Nginx container, two server blocks**: keeps runtime simple while still demonstrating multi-service behavior.
- **Self-signed TLS**: satisfies HTTPS requirement without external dependencies.
- **Rate limit at the Nginx layer**: avoids application changes and is easy to tune centrally.

## Assumptions

- Docker Engine and Docker Compose V2 are available (`docker compose`).
- Local ports `8080` and `8081` are free for binding.
- The self-signed certificate is acceptable for local testing only.

## Rate Limiting

**How it works**

- A shared memory zone (`limit_req_zone`) tracks requests per client IP address.
- The `limit_req` directive applies the 5 requests/second limit to the HTML server on port `8080`.
- Requests exceeding the burst threshold are rejected with HTTP `429`.

**How to change the threshold**

- Update the rate in `nginx/nginx.conf`:
  - `limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=5r/s;`
- Optionally adjust burst behavior in `nginx/sites/html.conf`:
  - `limit_req zone=req_limit_per_ip burst=1;`
  - Increase `burst` to allow short spikes, or set `limit_req_status` to change the response code.

## Build and Run

### Prerequisites

- Docker
- Docker Compose

### Build and start the stack

```bash
docker compose build
docker compose up
```

Nginx will be available at:

- `http://localhost:8080`
- `http://localhost:8081`

### Run tests

In a separate terminal:

```bash
docker compose up --build --abort-on-container-exit --exit-code-from tests
```

This will start the Nginx container and run the Python test container. The exit code will reflect the test result.

## Optional: Enable HTTPS Port Mapping

To expose HTTPS locally, add this to the `ports` section of the `nginx` service in `docker-compose.yml`:

```yaml
- "443:443"
```

Then access `https://localhost` in your browser. Because the certificate is self-signed, your browser will show a warning.
