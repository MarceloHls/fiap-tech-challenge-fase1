from fastapi import APIRouter, Depends, HTTPException, Query, status
from api import database, auth
from api.auth import get_current_user
from api.models import Book, UserCreate, Token
from typing import List, Optional
from sqlalchemy.orm import Session
from api.database import get_db_session
from fastapi.security import HTTPBearer

security_scheme = HTTPBearer()
router = APIRouter(prefix="/api/v1")

@router.post("/auth/register", tags=["Auth"])
async def register_user(user_data: UserCreate, db: Session = Depends(get_db_session)):
    existing_user = database.get_user(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    hashed = auth.get_password_hash(user_data.password)
    database.create_user(db, user_data.username, hashed)
    return {"message": "Sucesso!"}

@router.post("/auth/login", response_model=Token, tags=["Auth"])
async def login(user_data: UserCreate, db: Session = Depends(get_db_session)):
    user = database.get_user(db, user_data.username)
    if not user or not auth.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/scraping/trigger", tags=["Admin"])
async def trigger_scraping(current_user: str = Depends(get_current_user)):
    """Rota protegida que inicia o scraping manualmente"""
    import subprocess
    subprocess.Popen(["python", "scripts/scraper.py"])
    return {"message": f"Scraping iniciado por {current_user} em segundo plano."}

@router.get("/health", tags=["Admin"])
async def health_check():
    """Verifica se a API está online."""
    return {"status": "online", "message": "API de Livros funcionando corretamente"}

@router.get("/books", response_model=List[Book], tags=["Books"])
async def list_books(current_user: str = Depends(get_current_user)):
    """Retorna todos os livros. Agora exige o token corretamente."""
    return database.get_db_as_objects()

@router.get("/books/search", response_model=List[Book], tags=["Books"])
async def search_books(
    title: Optional[str] = Query(None, description="Parte do título do livro"),
    rating: Optional[str] = Query(None, description="Avaliação (Ex: Three, Four)"),
    category: Optional[str] = Query(None, description="Categoria do livro (Ex: Music, Classics)"),
    current_user: str = Depends(get_current_user)
):
    """Busca livros filtrando por título, avaliação ou categoria."""
    books = database.get_db_as_objects()
    if title:
        books = [b for b in books if title.lower() in b.title.lower()]
    if rating:
        books = [b for b in books if rating.lower() == b.rating.lower()]
    if category:
        books = [b for b in books if category.lower() == b.category.lower()]
    return books

@router.get("/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: int,current_user: str = Depends(get_current_user)):
    """Busca um livro específico pelo seu ID (índice do CSV)."""
    book = database.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book

@router.get("/categories", tags=["Books"])
async def list_categories(current_user: str = Depends(get_current_user)):
    """Lista dinamicamente todas as categorias encontradas na base de dados."""
    df = database.get_db_csv()
    if df is not None and 'category' in df.columns:
        categories = sorted(df['category'].dropna().unique().tolist())
        return categories
    return []