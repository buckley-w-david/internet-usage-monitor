from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


LOGIN_PAGE='https://xplornet.force.com/customers/loginCommunity'

def check(username, password):
    options = Options()
    options.headless = True

    with webdriver.Firefox(options=options) as driver:
        driver.get(LOGIN_PAGE)

        # Login to site
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "j_id0:j_id1:j_id5"))
        )
        username_field.send_keys(username)

        password_field = driver.find_element_by_name('j_id0:j_id1:j_id7')
        password_field.send_keys(password)

        submit_button = driver.find_element_by_name('j_id0:j_id1:j_id9')
        submit_button.click()

        # Switch into iframe
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "066F00000025Gjm"))
        )
        driver.switch_to.frame(iframe)

        # Click the usage button
        usage_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-buttonname='ViewUsage']"))
        )
        usage_button.click()

        # Switch to new window
        driver.close()
        driver.switch_to_window(driver.window_handles[0])


        # Switch to outer iframe
        outer_frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "canvas-outer-_:UsageTracker:j_id0:j_id29:canvasapp"))
        )
        driver.switch_to_frame(outer_frame)

        # Switch to inner iframe
        inner_frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "canvas-inner-_:UsageTracker:j_id0:j_id29:canvasapp"))
        )
        driver.switch_to_frame(inner_frame)

        # Get the percentage
        usage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p[class='usageAmt']"))
        )
        return usage.text

if __name__ == '__main__':
    import sys
    print(check(sys.argv[1], sys.argv[2]))
