# URLs
BASE_URL = "https://www.imdb.com"
TOP_MOVIES_URL = f"{BASE_URL}/chart/top/"

COOKIE_BANNER = '//div[@data-testid="cookie-policy-banner"]'
COOKIE_ACCEPT = '//button[contains(@data-testid, "accept-button")]'
MOVIE_LINKS = '//li[contains(@class, "ipc-metadata-list-summary-item")]//a[contains(@href, "/title/")]'

MOVIE_TITLE = 'h1[data-testid="hero-title-block__title"]'
MOVIE_YEAR = 'a[href*="releaseinfo"]'  # Year link
MOVIE_RATING = 'div[data-testid="hero-rating-bar__aggregate-rating__score"] span:first-child'
MOVIE_DURATION = 'ul[data-testid="hero-title-block__metadata"] li:last-child'