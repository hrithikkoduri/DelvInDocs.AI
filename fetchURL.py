from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time

class URLFetcher:
    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = webdriver.Chrome()  

    def fetch_urls(self):
        try:
            self.driver.get(self.base_url)
            
            time.sleep(5)

            links = self.driver.find_elements(By.TAG_NAME, 'a')

            urls = [urljoin(self.base_url, link.get_attribute('href')) for link in links if link.get_attribute('href')]
            
            print(f"Found {len(urls)} URLs")
            return urls
        except Exception as e:
            print(f"Error fetching URLs: {e}")
            return []
        finally:
            self.driver.quit()


