from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import random

def random_delay(min=1, max=3):
    """Random delay between actions to mimic human behavior"""
    delay = random.uniform(min, max)
    time.sleep(delay)

def wait_for_element(driver, locator, timeout=10):
    """Wait for element to be present and visible"""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    except TimeoutException:
        print(f"Timeout waiting for element: {locator}")
        return None
    except WebDriverException as e:
        print(f"WebDriver error waiting for element: {str(e)}")
        return None