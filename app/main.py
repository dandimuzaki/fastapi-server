from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.router import router as process_router
from app.config import settings

app = FastAPI()

origins = [
  "http://localhost:5173",
  settings.CLIENT_URL
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(process_router)
