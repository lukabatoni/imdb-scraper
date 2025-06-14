from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from .utils import random_delay, wait_for_element
from config import settings
import pandas as pd
import time

class IMDbScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.movie_data = []
    
    def accept_cookies(self):
        try:
            cookie_banner = wait_for_element(
                self.driver, 
                (By.XPATH, settings.COOKIE_BANNER),
                timeout=3
            )
            if cookie_banner:
                accept_btn = wait_for_element(
                    self.driver,
                    (By.XPATH, settings.COOKIE_ACCEPT),
                    timeout=3
                )
                if accept_btn:
                    accept_btn.click()
                    print("Accepted cookies")
                    random_delay(1, 2)
        except Exception as e:
            print(f"No cookie banner found or could not accept: {str(e)}")
    
    def get_top_movies_links(self):
        print("Loading top movies page...")
        self.driver.get(settings.TOP_MOVIES_URL)
        random_delay(2, 3)
        
        self.accept_cookies()
        
        print("Finding movie links...")
        try:
            links = wait_for_element(
                self.driver,
                (By.XPATH, settings.MOVIE_LINKS),
                timeout=10
            )
            if links:
                movie_links = [link.get_attribute('href') for link in self.driver.find_elements(By.XPATH, settings.MOVIE_LINKS)]
                print(f"Found {len(movie_links)} movie links")
                return movie_links
        except Exception as e:
            print(f"Failed to find movie links: {str(e)}")
        
        return []
    
    def scrape_movie_details(self, url):
        try:
            print(f"Scraping: {url}")
            self.driver.get(url)
            random_delay(2, 4)
            
            # Check if page loaded
            if "imdb.com/title/" not in self.driver.current_url:
                print(f"Redirected to {self.driver.current_url}, skipping")
                return None
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract data with fallbacks
            title_elem = soup.select_one(settings.MOVIE_TITLE)
            year_elem = soup.select_one(settings.MOVIE_YEAR)
            rating_elem = soup.select_one(settings.MOVIE_RATING)
            duration_elem = soup.select(settings.MOVIE_DURATION)
            
            data = {
                'title': title_elem.text.strip() if title_elem else 'N/A',
                'year': year_elem.text.strip() if year_elem else 'N/A',
                'rating': rating_elem.text.strip() if rating_elem else 'N/A',
                'duration': duration_elem[-1].text.strip() if duration_elem else 'N/A',
                'url': url,
                'scraped_at': pd.Timestamp.now()
            }
            
            print(f"Scraped: {data['title']} ({data['year']})")
            return data
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def scrape_top_movies(self, limit=10):
        movie_links = self.get_top_movies_links()[:limit]
        
        if not movie_links:
            print("No movie links found. Check your selectors or website structure.")
            return []
        
        for i, link in enumerate(movie_links, 1):
            try:
                print(f"\nProcessing movie {i}/{len(movie_links)}")
                movie_data = self.scrape_movie_details(link)
                if movie_data:
                    self.movie_data.append(movie_data)
                random_delay(2, 4)  # Longer delay between movies
            except KeyboardInterrupt:
                print("\nScraping interrupted by user")
                break
            except Exception as e:
                print(f"Unexpected error processing movie: {str(e)}")
                continue
        
        return self.movie_data
    
    def save_data(self, format='both'):
        if not self.movie_data:
            print("No data to save")
            return
            
        df = pd.DataFrame(self.movie_data)
        
        import os
        os.makedirs('outputs', exist_ok=True)
        
        if format in ('csv', 'both'):
            csv_path = 'outputs/movies_data.csv'
            df.to_csv(csv_path, index=False)
            print(f"Saved to {csv_path}")
        if format in ('json', 'both'):
            json_path = 'outputs/movies_data.json'
            df.to_json(json_path, orient='records', indent=2)
            print(f"Saved to {json_path}")
    
    def close(self):
        try:
            if self.driver:
                self.driver.quit()
                print("Browser closed")
        except Exception as e:
            print(f"Error closing browser: {str(e)}")