#!/usr/bin/sh
exec docker compose run --rm api alembic downgrade base
exec docker compose run --rm api alembic upgrade head
exec python -m api.db.seed