from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from .utils import random_delay, wait_for_element
from config import settings
import pandas as pd

class IMDbScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.movie_data = []
    
    def accept_cookies(self):
        try:
            cookie_banner = wait_for_element(
                self.driver, 
                (By.XPATH, settings.COOKIE_BANNER)
            )
            if cookie_banner:
                accept_btn = wait_for_element(
                    self.driver,
                    (By.XPATH, settings.COOKIE_ACCEPT)
                )
                if accept_btn:
                    accept_btn.click()
                    random_delay()
        except Exception as e:
            print(f"Cookie handling failed: {str(e)}")
    
    def get_top_movies_links(self):
        self.driver.get(settings.TOP_MOVIES_URL)
        random_delay()
        
        self.accept_cookies()
        
        links = wait_for_element(
            self.driver,
            (By.XPATH, settings.MOVIE_LINKS),
            timeout=15
        )
        
        return [link.get_attribute('href') for link in links]
    
    def scrape_movie_details(self, url):
        self.driver.get(url)
        random_delay(2, 4)
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        data = {
            'title': soup.select_one(settings.MOVIE_TITLE).text if soup.select_one(settings.MOVIE_TITLE) else None,
            'year': soup.select_one(settings.MOVIE_YEAR).text if soup.select_one(settings.MOVIE_YEAR) else None,
            'rating': soup.select_one(settings.MOVIE_RATING).text if soup.select_one(settings.MOVIE_RATING) else None,
            'duration': soup.select_one(settings.MOVIE_DURATION).text if soup.select_one(settings.MOVIE_DURATION) else None,
            'url': url,
            'scraped_at': pd.Timestamp.now()
        }
        
        return data
    
    def scrape_top_movies(self, limit=10):
        movie_links = self.get_top_movies_links()[:limit]
        
        for link in movie_links:
            try:
                movie_data = self.scrape_movie_details(link)
                self.movie_data.append(movie_data)
                random_delay()
            except Exception as e:
                print(f"Failed to scrape {link}: {str(e)}")
        
        return self.movie_data
    
    def save_data(self, format='both'):
        df = pd.DataFrame(self.movie_data)
        
        if format in ('csv', 'both'):
            df.to_csv('outputs/movies_data.csv', index=False)
        if format in ('json', 'both'):
            df.to_json('outputs/movies_data.json', orient='records')
    
    def close(self):
        self.driver.quit()