import os

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv


app = FastAPI()

load_dotenv()

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allowed_origins=origins,
    allowed_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("FASTAPI_PORT")))