from fastapi import FastAPI, Depends
from database import init_db
from routers import users, code_files, ai_suggestions, auth

app = FastAPI()

# Initialize the database
init_db()

# Include Routers
app.include_router(users.router)
app.include_router(code_files.router)
app.include_router(ai_suggestions.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the real-time collaborative code editor!"}