# Insta-Post API

A FastAPI-based REST API for managing user profiles and posts, inspired by Instagram's functionality. Built with modern async/await patterns, SQLModel ORM, and PostgreSQL database.

## Features

- **User Management**: Create, read, update, and delete user accounts
- **Profile Management**: Create and manage user profiles with bio information
- **Post Management**: Create and manage posts within user profiles
- **Email Validation**: Only Gmail email addresses are accepted
- **Async/Await**: Full async support for high-performance database operations
- **Data Validation**: Pydantic-based request/response validation
- **Cascading Deletes**: Automatic cleanup of related data when users are deleted
- **Interactive API Documentation**: Built-in Swagger UI and ReDoc documentation

## Tech Stack

- **Framework**: FastAPI 0.128.0+
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLModel 0.0.31 (SQLAlchemy 2.0+)
- **Async Runtime**: asyncpg, uvloop
- **Validation**: Pydantic 2.12.5+
- **Python**: 3.13+

## Project Structure

```
insta-post/
├── main.py                      # Application entry point
├── pyproject.toml              # Project configuration and dependencies
├── .env                        # Environment variables (not included)
├── db/
│   ├── db_connection.py        # Database connection setup
│   └── db_tables.py            # SQLModel table definitions
├── router/
│   ├── __init__.py
│   ├── user.py                 # User CRUD endpoints
│   ├── profile.py              # Profile management endpoints
│   └── post.py                 # Post management endpoints (placeholder)
└── validation/
    └── pydantic_schema.py      # Pydantic validation schemas
```

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL database running
- pip or conda package manager

### Setup Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd insta-post
```

2. **Create a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -e .
```

4. **Configure environment variables**
   Create a `.env` file in the project root:

```env
DB_URL=postgresql+asyncpg://username:password@localhost/dbname
DB_POOL_SIZE=10
DB_POOL_RECYCLE=3600
DB_ECHO=False
```

5. **Run the application**

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Users (`/users`)

- **POST** `/users/create` - Create a new user
  - Request body: `{ "username": "string", "email": "user@gmail.com" }`
- **GET** `/users/{user_id}` - Get user by ID
- **PUT** `/users/{user_id}/update` - Update user information
  - Request body: `{ "username": "string", "email": "user@gmail.com" }`
- **DELETE** `/users/{user_id}/delete` - Delete user (cascades to profiles and posts)

### Profiles (`/profile`)

- **GET** `/profile/` - Get all profiles
- **GET** `/profile/{profile_id}` - Get profile by ID with associated posts
- **POST** `/profile/create/{user_id}` - Create a new profile for a user
  - Request body: `{ "bio": "string (10-40 characters)" }`
- **PUT** `/profile/{profile_id}/update` - Update profile bio
  - Query parameter: `bio` - New bio text
- **DELETE** `/profile/{profile_id}/delete` - Delete profile

## Data Models

### User

- `id`: UUID (auto-generated)
- `username`: String (3-20 characters, title-cased)
- `email`: Email (Gmail only, must be unique)
- `created_at`: Date (auto-generated)
- `profiles`: List of Profile objects (one-to-many relationship)

### Profile

- `id`: UUID (auto-generated)
- `user_id`: Foreign key to User (with cascade delete)
- `bio`: String (10-40 characters, title-cased)
- `created_at`: Date (auto-generated)
- `posts`: List of Post objects (one-to-many relationship)

### Post

- `id`: UUID (auto-generated)
- `profile_id`: Foreign key to Profile
- `title`: String
- `content`: String
- `created_at`: Date

## Environment Configuration

The application uses Pydantic Settings for configuration management. Configure the following via `.env` file:

| Variable          | Type    | Default | Description                            |
| ----------------- | ------- | ------- | -------------------------------------- |
| `DB_URL`          | String  | -       | PostgreSQL connection string           |
| `DB_POOL_SIZE`    | Integer | 10      | Connection pool size                   |
| `DB_POOL_RECYCLE` | Integer | 3600    | Connection pool recycle time (seconds) |
| `DB_ECHO`         | Boolean | False   | Enable SQL query logging               |

## Database Initialization

The database tables are automatically created on application startup through the FastAPI lifespan context manager. No manual migrations required.

## Error Handling

The API returns appropriate HTTP status codes:

- `201 Created` - Resource successfully created
- `200 OK` - Successful GET request
- `204 No Content` - Resource not found
- `302 Found` - User found
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## API Documentation

Once the application is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Documentation is disabled in production mode.

## Validation Rules

- **Username**: 3-20 characters, automatically title-cased
- **Email**: Gmail only (validation enforced), must be unique
- **Bio**: 10-40 characters, automatically title-cased
- **Post Title**: No minimum length enforced
- **Post Content**: No minimum length enforced

## Development

### Run tests

```bash
pytest
```

### Enable debug logging

Set `DB_ECHO=True` in `.env` to see SQL queries

### Async Support

All endpoints use async/await for non-blocking database operations. The application uses uvloop for improved async performance.

## Performance Considerations

- Connection pooling enabled (default: 10 connections)
- Connection recycling set to 1 hour
- Pre-ping enabled for stale connection detection
- Async operations prevent blocking on I/O
- FastAPI uses uvloop for high performance

## Future Enhancements

- Post management endpoints implementation
- Like/Comment functionality
- User authentication and JWT tokens
- Post search and filtering
- Pagination for large result sets
- Rate limiting
- Input sanitization and security hardening

## License

This project is provided as-is.

## Author

Created as a FastAPI learning project.
