from fastapi import FastAPI
from .database import  engine
from . import models
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables
# Commented out to avoid creating the tables again when the app is run. now using alembic to create the tables
# models.Base.metadata.create_all(bind=engine)


# Create the FastAPI app
app = FastAPI()

origins = ["*"]
# origins = ["http://localhost:3000", "https://www.google.com"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World!!!!!!!!!!!!!"}


# Include the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)