# app/main.py

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import customers, punchcards, visits, analytics
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(customers.router, prefix="/v1")
app.include_router(punchcards.router, prefix="/v1")
app.include_router(visits.router, prefix="/v1")
app.include_router(analytics.router, prefix="/v1")

# Custom OpenAPI schema to simplify Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the base OpenAPI schema
    openapi_schema = get_openapi(
        title="Micro Loyalty API",
        version="1.0.0",
        description="API for managing customer loyalty programs",
        routes=app.routes,
    )

    # Ensure the "components" key exists
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Add Bearer token authentication
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply security globally
    openapi_schema["security"] = [{"Bearer": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi