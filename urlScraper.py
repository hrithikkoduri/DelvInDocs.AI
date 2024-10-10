import requests
from bs4 import BeautifulSoup

class TextScraper:
    def __init__(self, urls):
        self.urls = urls

    def fetch_texts(self):
        texts = []
        for url in self.urls:
            # Check if the URL is valid and fetch the text content
            if url.startswith("http://") or url.startswith("https://"):
                try:
                    response = requests.get(url)
                
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        texts.append(soup.get_text())
                except requests.RequestException as e:
                    print(f"Error fetching {url}: {e}")
            else:
                print(f"Skipping invalid URL: {url}")
                
        print(f"Found {len(texts)} texts pieces")
        return texts