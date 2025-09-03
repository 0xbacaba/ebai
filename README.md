# EbAI

### Run once:
Create `.env` file or export these variables in your shell:
```bash
NTFY_USER=<ntfy username>
NTFY_PASS=<ntfy password>
NTFY_SERVER=<ntfy server>
NTFY_TOPIC=<ntfy topic>
```

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python src/main.py 0
```

**parameters:**
- *delay*: the delay between each run, or 0 to quit after first run. Default: 60

### Run in container:
```bash
docker buildx build -t ebai .
docker run --rm ebai
```

### Example docker-compose:
```yaml
services:
  ebai:
    container_name: ebai
    build: .
    pull_policy: never
    env_file:
      - .env
    volumes:
      - ./ebai.db:/app/ebai.db
    restart: unless-stopped
```
