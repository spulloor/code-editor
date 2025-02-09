# Real-Time Collaborative Code Editor

This is a real-time collaborative code editor with features like signing up users, logging users, adding code files, integrating AI models for code suggestions.

### THIS IS A WORK IN PROGRESS!!!

## Codebase Structure

The codebase is divided into two parts:
1. **Frontend**
2. **Backend**

### Frontend

The frontend is mainly written in Next.js. You can start the development server by running:

```bash
npm run dev
```

### Backend

The backend is mainly written in FASTAPI and uses SQLAlchemy, Pydantic, and Alembic for database migrations. You can start the development server by running:

```bash
./run.sh
```

Additionally, I have provided the `db-migrate.sh` file to aid with database migrations.

# Future Enhancements:
* The Front-end portion needs to be polished. Needs a lot of unit testing to squash the bugs!!
* The Back-end needs to provide endpoints for collaboration with different users.
* Currently uses the open source Ollama model 3.2 that runs locally on my machine to get the AI suggestions part. Can use an OpenAI API for much better availiability.