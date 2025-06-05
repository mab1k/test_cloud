from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import allure
from abc import ABC, abstractmethod

EXPECTED_URL = "https://www.iana.org/help/example-domains"
EXPECTED_TEXT = "More information"
EXPECTED_TITLE = "Example"

class BasePage(ABC):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @abstractmethod
    def is_page_opened(self):
        pass

class ExamplePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.more_info_link = (By.XPATH, f"//a[contains(text(), '{EXPECTED_TEXT}')]")

    def is_page_opened(self):
        return EXPECTED_TITLE in self.driver.title

    def click_more_info(self):
        element = self.wait.until(
            EC.presence_of_element_located(self.more_info_link)
        )
        element.click()
        return self.driver.current_url == EXPECTED_URL

class IanaPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def is_page_opened(self):
        return self.driver.current_url == EXPECTED_URL

@pytest.fixture
def init_driver():
    with allure.step("Init webdriver in headless mode"):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        yield driver
        driver.quit()

@allure.story("Test example")
def tests_example(init_driver):
    try:
        with allure.step("Get url https://example.com"):
            init_driver.get("https://example.com")
            example_page = ExamplePage(init_driver)

        assert example_page.is_page_opened()

        with allure.step("Click more info link"):
            assert example_page.click_more_info()

        iana_page = IanaPage(init_driver)
        assert iana_page.is_page_opened()

    except Exception as e:
        with allure.step("Test failed"):
            allure.attach(init_driver.get_screenshot_as_png(), name="failure-screenshot",
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Test failed: {str(e)}")
