# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as product_router
from db import create_db_and_tables

app = FastAPI(
    title="Customer Order API",
    description="API for customer order management",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables on startup
@app.on_event("startup")
def startup_event():
    create_db_and_tables()

app.include_router(product_router)
