# Tech Challenge - Fase 1: Machine Learning Engineering

## Descricao do Projeto
Este projeto e o Tech Challenge da Fase 1 da Pos-Tech (FIAP). O objetivo e criar um pipeline de dados completo: Web Scraping, armazenamento em CSV e uma API para consulta.

---

## Arquitetura do Pipeline
1. **Ingestao**: Scraper colhe dados do 'books.toscrape.com'.
2. **Dados**: Armazenamento estruturado em 'data/books.csv'.
3. **Servico**: FastAPI expo os dados via JSON.

---

## Como Executar

### 1. Criar Ambiente Virtual
Windows:
python -m venv venv
.\\\\venv\\\\Scripts\\\\activate

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

### 2. Instalar Bibliotecas
pip install -r requirements.txt

### 3. Rodar o Scraper
python scripts/scraper.py

### 4. Rodar a API
uvicorn api.main:app --reload

---

## Documentacao da API
- GET /api/v1/health: Status do sistema.
- GET /api/v1/books: Lista todos os livros.
- GET /api/v1/books/{id}: Detalhes por ID.
- GET /api/v1/categories: Lista categorias.

---
*Projeto obrigatorio - 90% da nota da fase.*