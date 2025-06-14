from src.scraper import IMDbScraper
import time
import signal
import sys

def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C! Closing scraper gracefully...')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    start_time = time.time()
    scraper = IMDbScraper()
    
    try:
        print("\nIMDb Top Movies Scraper")
        print("=======================\n")
        
        # Scrape top 10 movies by default
        scraper.scrape_top_movies(limit=10)
        
        # Save data
        print("\nSaving collected data...")
        scraper.save_data()
        
        duration = time.time() - start_time
        print(f"\nScraping completed in {duration:.2f} seconds")
        
    except Exception as e:
        print(f"\nError in main execution: {str(e)}")
    finally:
        print("\nCleaning up...")
        scraper.close()

if __name__ == "__main__":
    main()