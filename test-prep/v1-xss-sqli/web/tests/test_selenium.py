"""Q5 — UI testing over HTTP with Selenium (headless Chrome).

Run against a live server:
    BASE_URL=http://127.0.0.1:8000 python tests/test_selenium.py
"""

import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    remote = os.environ.get("SELENIUM_REMOTE_URL")
    if remote:
        return webdriver.Remote(command_executor=remote, options=opts)
    return webdriver.Chrome(options=opts)


def submit_term(driver, term):
    driver.get(BASE_URL + "/")
    driver.find_element(By.ID, "search_term").send_keys(term)
    driver.find_element(By.ID, "submit").click()


def test_xss_is_blocked(driver):
    submit_term(driver, "<script>alert(1)</script>")
    assert driver.find_elements(By.ID, "error"), "an error should be shown"
    assert not driver.find_elements(By.ID, "term"), "should not reach the result page"
    # input cleared
    assert driver.find_element(By.ID, "search_term").get_attribute("value") == ""
    print("PASS: XSS payload blocked, input cleared, stayed on home page")


def test_sqli_is_blocked(driver):
    submit_term(driver, "' OR '1'='1")
    assert driver.find_elements(By.ID, "error"), "an error should be shown"
    assert not driver.find_elements(By.ID, "term"), "should not reach the result page"
    print("PASS: SQL injection payload blocked, stayed on home page")


def test_valid_term_reaches_result(driver):
    submit_term(driver, "laptop")
    term = driver.find_element(By.ID, "term").text
    assert term == "laptop", f"result page should show the term, got {term!r}"
    print("PASS: valid term accepted, result page shows the search term")


def test_back_button_returns_home(driver):
    driver.find_element(By.ID, "back").click()
    assert driver.find_elements(By.ID, "search_term"), "should be back on the home page"
    print("PASS: back button returned to the home page")


def main():
    driver = make_driver()
    try:
        test_xss_is_blocked(driver)
        test_sqli_is_blocked(driver)
        test_valid_term_reaches_result(driver)
        test_back_button_returns_home(driver)
        print("\nAll Selenium UI tests passed.")
        return 0
    except AssertionError as exc:
        print(f"\nUI TEST FAILED: {exc}")
        return 1
    finally:
        driver.quit()


if __name__ == "__main__":
    sys.exit(main())
