from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.maximize_window()

driver.get("https://example.com")

# Так как в Selenium в CSS селекторе не поддерживается конструкции такого вида :contains('text'), можем использовать XPath
element = driver.find_element(By.XPATH, "//a[contains(text(), 'More information')]")

# Вот как выглядит это с помощью CSS селектора
# element = driver.find_element(By.CSS_SELECTOR, 'a[href*="iana.org"]')

element.click()
