# Week 5 — Web Proxy (Nginx / TLS) + GitHub Actions

**Lab goal:** run an Nginx web server/reverse proxy in Docker, add TLS with Let's
Encrypt + Certbot, and create a GitHub Actions CI job that tests the page.

## Files (`nginx-proxy/`)

| File | Purpose |
|------|---------|
| `index.html` | Simple "Hello World" page served by Nginx. |
| `nginx.conf` | Plain HTTP (port 80) config serving `index.html`. |
| `nginx-compose.yml` | Compose file for the HTTP-only proxy. |
| `nginx-tls.conf` | HTTPS config: port 80 → redirect to 443, ACME challenge location, SSL certs. |
| `nginx-compose-tls.yml` | Compose file adding a `certbot` container + cert volumes. |
| `test-nginx.yml` | GitHub Actions workflow that boots Nginx and greps the page for "Hello World". |

> **Note on `worker_processes`/`events` in `nginx.conf`:** these files are full
> top-level Nginx configs (they replace `/etc/nginx/nginx.conf`), which is why they
> include the `events {}` block, not just a `server {}` snippet.

## Part A — HTTP proxy

```bash
cd nginx-proxy
docker compose -f nginx-compose.yml up -d
curl http://localhost/          # -> Hello, World!
```

`nginx-compose.yml` mounts `nginx.conf` read-only at `/etc/nginx/nginx.conf` and
`index.html` at `/var/www/html/index.html`, and puts the container on a custom
bridge network with a fixed IP.

## Part B — Add TLS with Let's Encrypt + Certbot

Let's Encrypt (the CA) must **verify domain ownership** before issuing a cert. Two
challenge types:

1. **ACME / HTTP-01 challenge** — Certbot places a token at
   `http://<DOMAIN>/.well-known/acme-challenge/<TOKEN>`; the CA fetches it. Requires
   port **80** reachable, which is why the TLS compose keeps `80:80` open.
2. **DNS-01 challenge** — put a given value in a **TXT** record under your domain.
   Use this when you can't expose port 80 but can edit DNS.

Steps:

```bash
# 1. Edit nginx-tls.conf and the compose file: replace yourdomain.com / email.
# 2. Bring up nginx + certbot
cp nginx-compose-tls.yml nginx-compose.yml      # or use -f nginx-compose-tls.yml
docker compose -f nginx-compose-tls.yml up -d
```

**Obtain the certificate** (webroot / ACME):

```bash
# entrypoint used by the certbot container (already parameterised in the lab):
certbot certonly --webroot -w /var/www/certbot \
  --email your-email@example.com --agree-tos --no-eff-email \
  --rsa-key-size 4096 --expand --force-renewal \
  -d yourdomain.com -d www.yourdomain.com && nginx -s reload
```

Or **DNS challenge** if you can't expose port 80:

```bash
sudo certbot certonly --manual --preferred-challenges dns \
  -d yourdomain.com -d www.yourdomain.com \
  --agree-tos -m your-email@example.com --no-eff-email
# then create the TXT record it prints, and continue.
```

`nginx-tls.conf` references the issued cert:

```nginx
ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

Test:

```bash
curl https://yourdomain.com/
```

## Part C — Auto-renewal (optional)

Let's Encrypt certs expire every **90 days**. Cron job:

```bash
crontab -e
0 3 * * * docker compose -f certbot-compose.yml run --rm certbot renew && docker compose restart nginx
```

## Part D — GitHub Actions CI (`test-nginx.yml`)

To use it, copy into `.github/workflows/` at the repo root. It:

1. Checks out the code.
2. Runs Nginx in Docker, mounting `index.html`.
3. Waits, then `curl`s the page and `grep`s for **"Hello World"** (test fails if absent).
4. Stops the container.

This is a minimal CI smoke test — the pattern (build → run → assert on output) is the
foundation for the richer test pipelines in Weeks 6–9.

## Exam-relevant takeaways

- A reverse proxy handles **TLS/SSL termination** in front of your app.
- ACME (HTTP-01) vs DNS-01 challenge, and when to use each.
- Certs expire at 90 days → automate renewal.
- CI/CD (GitHub Actions) reduces security risk by automatically building/testing on
  every push — **workflows live in `.github/workflows/*.yml`**.
