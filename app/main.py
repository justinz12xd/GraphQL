import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schema.schema import schema
from app.reports.routes import router as reports_router

app = FastAPI(
    title="Love4Pets GraphQL API",
    version="1.0.0",
    description="API GraphQL para gestión de refugio animal con generación de reportes PDF"
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Reports endpoints
app.include_router(reports_router)