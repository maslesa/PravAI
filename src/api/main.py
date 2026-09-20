from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import health, query


app = FastAPI(
    title='Pravai API',
    description='Evidence-grounded legal research assistant for Serbian legislation.',
    version='1.0.0',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(health.router, prefix='/api/v1')
app.include_router(query.router, prefix='/api/v1')