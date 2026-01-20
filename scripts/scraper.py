import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def scrape_books():
    base_url = "http://books.toscrape.com/catalogue/"
    current_page = "page-1.html"
    books_data = []
    
    print("Iniciando o Web Scraping completo (com categorias)... Aguarde.")

    while current_page:
        url = base_url + current_page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            rating_classes = book.find('p', class_='star-rating')['class']
            rating = rating_classes[1]
            availability = book.find('p', class_='instock availability').text.strip()
            image_url = "http://books.toscrape.com/" + book.find('img')['src'].replace('../', '')
            
            book_link = base_url + book.h3.a['href']
            book_response = requests.get(book_link)
            book_soup = BeautifulSoup(book_response.content, 'html.parser')
            
            breadcrumb = book_soup.find('ul', class_='breadcrumb')
            category = breadcrumb.find_all('li')[2].text.strip() if breadcrumb else "Desconhecida"

            books_data.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "category": category,
                "image_url": image_url
            })

        print(f"Página {current_page} processada...")

        next_btn = soup.find('li', class_='next')
        if next_btn:
            current_page = next_btn.a['href']
        else:
            current_page = None
            
    return books_data

def save_to_csv(data):
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv('data/books.csv', index=True, index_label='id')
    print(f"\nSucesso! {len(df)} livros com categorias foram salvos em 'data/books.csv'")

if __name__ == "__main__":
    start_time = time.time()
    all_books = scrape_books()
    save_to_csv(all_books)
    end_time = time.time()
    print(f"Tempo total: {round(end_time - start_time, 2)} segundos.")