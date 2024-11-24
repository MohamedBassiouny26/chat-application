# Chat Application

This repository contains a scalable and modular chat application built using FastAPI. The application is designed for handling real-time chat features with an organized project structure for easy maintainability and extensibility.
## System Design
![Alt text for the image](docs/chat-design.png)
[View the project diagram](https://excalidraw.com/#json=tUaPcGE98dErpsxo6sb6G,00YrlzU1Hmq3e-GmId1D1A)
## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:MohamedBassiouny26/chat-application.git
   cd chat_application
   ```

2. Make bin files executable 
   ```bash
   poetry install
   ```

3. Build and start the services using Docker Compose:
    ```bash
      docker-compose up --build
    ```
# Chat Application

## Schema

### Applications

| **Column**    | **Type** | **Constraint**       |
|---------------|----------|----------------------|
| `id`          | `int`    | Primary Key (PK)    |
| `token`       | `string` | Unique              |
| `name`        | `string` | Not Null            |
| `chats_count` | `int`    | Not Null, Default (0) |
| `created_at`  | `date`   | Not Null            |
| `updated_at`  | `date`   | Not Null            |

---

### Chats

| **Column**     | **Type** | **Constraint**       |
|----------------|----------|----------------------|
| `id`           | `int`    | Primary Key (PK)    |
| `app_token`    | `string` | Foreign Key (FK) (applications.token) |
| `number`       | `int`    | Not Null            |
| `message_count`| `int`    | Not Null            |
| `created_at`   | `date`   | Not Null            |
| `updated_at`   | `date`   | Not Null            |

**Composite Unique Constraint**:

```python
UniqueConstraint("app_token", "number", name="uq_app_token_number")
```

---

### Messages

| **Column**     | **Type** | **Constraint**       |
|----------------|----------|----------------------|
| `id`           | `int`    | Primary Key (PK)    |
| `chat_id`      | `int`    | Foreign Key (FK) (chats.id) |
| `number`       | `int`    | Not Null            |
| `body`         | `string` | Not Null            |
| `created_at`   | `date`   | Not Null            |
| `updated_at`   | `date`   | Not Null            |

**Composite Unique Constraint**:

```python
UniqueConstraint("chat_id", "number", name="uq_chat_id_number")
```

## Project Structure

```
chat_application
├── .venv/                # Virtual environment directory
├── alembic/             # Database migration files
├── app/                 # Core application code
│   ├── actions/         # Action classes for business logic
│   ├── jobs/            # Background tasks and job management
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── tasks.py
│   ├── models/          # Database models
│   ├── providers/       # External service integrations
│   └── routers/         # API route definitions
│       ├── __init__.py
│       ├── applications.py
│       ├── chats.py
│       └── messages.py
├── bin/                 # Scripts for task execution
│   └── consumer/        # Consumer scripts for event handling
│       └── main.py
├── tests/               # Unit and integration tests
├── .gitignore           # Git ignore file
├── alembic.ini          # Alembic configuration file
├── docker-compose.yaml  # Docker Compose configuration
├── Dockerfile           # Dockerfile for the application
├── Dockerfile_consumer  # Dockerfile for the consumer service
├── Dockerfile_scheduler # Dockerfile for the scheduler service
├── poetry.lock          # Poetry lock file
├── pyproject.toml       # Poetry project configuration
├── pytest.ini           # Pytest configuration
├── README.md            # Project documentation
```
## Swagger Docs
 You can find endpoint documentation here localhost:8000/docs
## Features

- **API Routes:**
  - `applications.py`: Manages application-level routes.
  - `chats.py`: Handles chat-related routes.
  - `messages.py`: Manages message-related operations.
- **Background Jobs:** Defined in `jobs/main.py` and `jobs/tasks.py` for asynchronous processing.
- **Event Consumer (Worker):** Located in `bin/consumer/main.py` to handle event-based tasks.
- **Database Migrations:** Managed with Alembic.
- **Dockerized Services:** Includes Dockerfiles for the main app, consumer, and scheduler.
- **Unit and Integration Tests:** Applications Endpoint Organized in the `tests/` directory.

## Prerequisites

- Python 3.12+
- Poetry
- Docker and Docker Compose




## Testing
1. To run test cases need to be inside docker container
```
docker exec -it {docker_id} /bin/bash
```

2. Run all tests:
```bash
pytest
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

