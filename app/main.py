import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schema.schema import schema

app = FastAPI(
    title="Love4Pets GraphQL API",
    version="1.0.0",
)
@app.get("/health")
async def health_check():
    return {"status": "ok"}

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")