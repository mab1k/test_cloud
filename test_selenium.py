from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import allure

PATH_CHROMEDRIVER = "chromedriver.exe"
EXPECTED_URL = "https://www.iana.org/help/example-domains"
EXPECTED_TEXT = "More information"
EXPECTED_TITLE = "Example"


@pytest.fixture
def init_driver():
    with allure.step("Init webdriver in headless mode"):
        service = Service(PATH_CHROMEDRIVER)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()

        yield driver

        driver.quit()


@allure.story("Test example")
def tests_example(init_driver):
    with allure.step("Get url https://example.com"):
        init_driver.get("https://example.com")

    try:
        assert EXPECTED_TITLE in init_driver.title

        # Так как в Selenium в CSS селекторе не поддерживается конструкции такого вида :contains('text'), можем использовать XPath
        with allure.step("Get el with text contains 'More information'"):
            element = WebDriverWait(init_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{EXPECTED_TEXT}')]"))
            )
        # Вот как выглядит это с помощью CSS селектора
        # element = init_driver.find_element(By.CSS_SELECTOR, 'a[href*="iana.org"]')
        with allure.step("Click el"):
            element.click()

        assert init_driver.current_url == EXPECTED_URL

    except Exception as e:
        with allure.step("Test failed"):
            allure.attach(init_driver.get_screenshot_as_png(), name="failure-screenshot",
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Test failed: {str(e)}")
