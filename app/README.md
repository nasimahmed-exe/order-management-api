# order management API

Production guide order management system build with FastAPI and PostgreSQL.

## Problems this sloves
.*Double charging prevention* -> Idempotency keys ensure payment safety
.*Overselling prevention* -> Row level locking prevents race conditions
.*Unauthorized access* -> JWT auth with refresh token rotation and RBAC


## Tech Stack

FastAPI,PostgreSQL,SQLAlchemy,Docker,JWT

## How to run
docker compose up
API available at http://localhost:8000/docs

