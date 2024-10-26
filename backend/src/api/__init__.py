# This file can be left empty
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import agents, seeds, twitter, users

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # React app default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users.router)
app.include_router(agents.router)
app.include_router(twitter.router)
app.include_router(seeds.router)
