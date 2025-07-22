# Database for social media with FastAPI + PostgreSQL

A high-performance asynchronous backend API built using **FastAPI**, **SQLAlchemy (2.0 async)**, **PostgreSQL**, **Alembic**, and **Docker**. It supports user-generated posts, comments, likes, saves, and category-tagging — built for scalability and recommendation engine integration.

--------------------------------------------------------------------------------

## Features

- Fully async FastAPI backend
- PostgreSQL as primary data store (via Docker)
- Alembic for schema migrations
- User creation
- Posts, nested comments, likes, saves, categories
- Docker + Docker Compose ready
- Feed endpoint for user-specific post curation

------------------------------------------------------------------------------

## Tech Stack

| Layer         | Tool                         |
|--------------|------------------------------|
| Backend       | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM           | [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/) |
| DB            | [PostgreSQL](https://www.postgresql.org/) |
| Migrations    | [Alembic](https://alembic.sqlalchemy.org/) |
| Async Driver  | [`asyncpg`](https://github.com/MagicStack/asyncpg) |
| Containerization | [Docker](https://www.docker.com/) |
| API Docs      | Auto-generated Swagger (via FastAPI) |

-------------------------------------------------------------------------------

## Project Structure
.
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # DB interaction logic
│   ├── database.py      # Async DB setup
│   └── routers/         # Route definitions
├── alembic/             # Alembic migration env
├── docker-compose.yml   # PostgreSQL service
├── Makefile             # Development shortcuts
├── .env                 # Environment variables
├── .gitignore
└── README.md
