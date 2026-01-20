from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="API de Recomendação de Livros - Tech Challenge",
    description="API para consulta de livros extraídos via Web Scraping",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Livros. Acesse /docs para documentação."}