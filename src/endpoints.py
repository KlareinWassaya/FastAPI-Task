from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.config.definitions import ROOT_PATH
from src.config.definitions import SERVICE_NAME
from src.middleware.error_handler import ErrorHandlerMiddleware
from src.routes import user, tasks

app = FastAPI(
    title=f"{SERVICE_NAME} APIs",
    openapi_url=ROOT_PATH + "/openapi.json",
    redoc_url=ROOT_PATH + "/redoc",
    docs_url=ROOT_PATH + "/docs",
    swagger_ui_oauth2_redirect_url=ROOT_PATH + "/docs/oauth2-redirect",
)

origins = ["*"]

app.add_middleware(ErrorHandlerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(tasks.router)

# Add BearerAuth security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=f"{SERVICE_NAME} APIs",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply lock ONLY to /tasks/*
    for path in openapi_schema["paths"]:
        if path.startswith("/tasks"):
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
        if path.startswith("/users"):
            get_method = openapi_schema["paths"][path].get("get")
            if get_method: 
                get_method["security"] = [{"BearerAuth": []}]


    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi