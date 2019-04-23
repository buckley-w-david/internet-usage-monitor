from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from usage_monitor.config import Driver

LOGIN_PAGE = "https://xplornet.force.com/customers/loginCommunity"


def calculate_usage(username: str, password: str, *, driver: Driver = Driver.FIREFOX) -> float:
    if driver is Driver.FIREFOX:
        driver_choice = webdriver.Firefox
        options = FirefoxOptions()
    else:
        driver_choice = webdriver.Chrome
        options = ChromeOptions()

    options.headless = False

    with driver_choice(options=options) as driver:
        driver.get(LOGIN_PAGE)

        # Login to site
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "j_id0:j_id1:j_id5"))
        )
        username_field.send_keys(username)

        password_field = driver.find_element_by_name("j_id0:j_id1:j_id7")
        password_field.send_keys(password)

        submit_button = driver.find_element_by_name("j_id0:j_id1:j_id9")
        submit_button.click()

        # Switch into iframe
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "066F00000025Gjm"))
        )

        # Click the usage button
        usage_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[data-buttonname='ViewUsage']")
            )
        )
        usage_button.click()

        # Switch to new window
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

        # Switch to outer iframe
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, "canvas-outer-_:UsageTracker:j_id0:j_id29:canvasapp")
            )
        )

        # Switch to inner iframe
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, "canvas-inner-_:UsageTracker:j_id0:j_id29:canvasapp")
            )
        )

        # NOTE: I Don't know how this will react at the very beginning of the month before any usage.
        #       Ideally it will display "0%" and this will all still work, but it may display something like
        #       "N/A", and that won't satisfy the condition of it containing a '%'
        #
        #       The reason we're checking for a '%' is that there is a race condition where the page will create the
        #       paragraph element, but before it fills that paragraph with the percentage selenium will grab it, and so
        #       we would error out trying to cast it to a float
        usage_present = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "p[class='usageAmt']"), "%"
            )
        )
        if usage_present:
            usage = driver.find_element_by_css_selector("p[class='usageAmt']")
            return float(usage.text.strip("%")) / 100

        # TODO
        raise Exception("MAKE ME A SPECIFIC EXCEPTION")


if __name__ == "__main__":
    import sys

    print(check(sys.argv[1], sys.argv[2]))
