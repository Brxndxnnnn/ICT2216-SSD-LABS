"""Q5 — UI testing over HTTP with Selenium (headless Chrome).

Run against a live server:
    BASE_URL=http://127.0.0.1:8000 python tests/test_selenium.py
"""

import os
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
TIMEOUT = 10


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    remote = os.environ.get("SELENIUM_REMOTE_URL")
    # Retry: Chrome occasionally crashes on launch under load; a transient
    # start-up failure should not fail the whole UI check.
    last_err = None
    for _ in range(3):
        try:
            if remote:
                return webdriver.Remote(command_executor=remote, options=opts)
            return webdriver.Chrome(options=opts)
        except WebDriverException as err:
            last_err = err
            time.sleep(2)
    raise last_err


def submit_password(driver, password):
    driver.get(BASE_URL + "/")
    old_page = driver.find_element(By.ID, "login")
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login").click()
    # Wait for the POST to render/redirect before asserting (avoids flakiness).
    WebDriverWait(driver, TIMEOUT).until(EC.staleness_of(old_page))


def test_weak_password_stays_on_home(driver):
    submit_password(driver, "password")          # common -> rejected
    assert "/welcome" not in driver.current_url, "weak password should not log in"
    assert driver.find_elements(By.ID, "error"), "an error message should be shown"
    print("PASS: weak/common password rejected, stayed on home page")


def test_strong_password_reaches_welcome(driver):
    submit_password(driver, "correct horse battery staple")
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/welcome"))
    shown = driver.find_element(By.ID, "password").text
    assert shown == "correct horse battery staple"
    print("PASS: strong password accepted, welcome page shows the password")


def test_logout_returns_home(driver):
    driver.find_element(By.ID, "logout").click()
    WebDriverWait(driver, TIMEOUT).until_not(EC.url_contains("/welcome"))
    assert "/welcome" not in driver.current_url
    print("PASS: logout returned to the home page")


def main():
    driver = make_driver()
    try:
        test_weak_password_stays_on_home(driver)
        test_strong_password_reaches_welcome(driver)
        test_logout_returns_home(driver)
        print("\nAll Selenium UI tests passed.")
        return 0
    except AssertionError as exc:
        print(f"\nUI TEST FAILED: {exc}")
        return 1
    finally:
        driver.quit()


if __name__ == "__main__":
    sys.exit(main())
