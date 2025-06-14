# URLs
BASE_URL = "https://www.imdb.com"
TOP_MOVIES_URL = f"{BASE_URL}/chart/top/"

# XPATHS
COOKIE_BANNER = '//div[@data-testid="cookie-policy-banner"]'
COOKIE_ACCEPT = '//button[contains(text(), "Accept")]'
MOVIE_LINKS = '//td[@class="titleColumn"]/a'
NEXT_PAGE = '//a[contains(text(), "Next")]'

# CSS Selectors
MOVIE_TITLE = 'h1'
MOVIE_YEAR = 'span.sc-8c396aa2-2'
MOVIE_RATING = 'span.sc-7ab21ed2-1'
MOVIE_DURATION = 'ul.sc-8c396aa2-0 li:nth-child(3)'