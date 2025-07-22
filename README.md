# Database for social media with FastAPI + PostgreSQL

A high-performance asynchronous backend API built using **FastAPI**, **SQLAlchemy (2.0 async)**, **PostgreSQL**, **Alembic**, and **Docker**. It supports user-generated posts, comments, likes, saves, and category-tagging — built for scalability and recommendation engine integration.

--------------------------------------------------------------------------------

## Features

- User and Post creation
- Commenting (with replies and likes)
- Likes and Saves on posts and comments
- Categorized posts
- Asynchronous PostgreSQL interaction with `asyncpg`
- Docker + Docker Compose setup
- Controlled DB migrations via Alembic
  
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
```bash
.
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud/            # DB interaction logic
│   ├── database.py      # Async DB setup
│   └── routers/         # Route definitions
├── alembic/             # Alembic migration env
├── docker-compose.yml   # PostgreSQL service
├── Makefile             # Development shortcuts
├── .env                 # Environment variables
├── .gitignore
└── README.md
```
---------------------------------------------------------------------------------

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create .env File
Update the values in .env as needed
```bash
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
DATABASE_URL=postgresql+asyncpg://your_username:your_password@db/your_database
```

### 3. Build and Run with Docker
```bash
make up --build
```

### 4. Run Alembic Migrations
```bash
make migrate message="initial"
```

### 5. Access the App
Visit: http://localhost:8000/docs

----------------------------------------------------------------------------------

🔗 API Endpoints
Base URL: /

Users
POST /users/ — Create a new user

Posts
POST /posts/ — Create a post

GET /feed/{user_id} — Get user feed

Comments
POST /comments/ — Comment on a post

GET /comments/{post_id} — Get comments for a post

Likes
POST /likes/ — Like a post

POST /comment-likes/ — Like a comment

Saves
POST /saves/ — Save a post
