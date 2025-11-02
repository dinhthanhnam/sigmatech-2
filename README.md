```bash
docker compose build
```


```bash
docker compose run --rm api poetry install
```


```bash
docker compose run --rm web npm install
```


```bash
docker compose run --rm api poetry run alembic upgrade head
```


```bash
docker compose run --rm api poetry run python -m db.seed
```