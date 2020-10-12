import os, time, json

from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


USERNO = os.environ.get("USERNO")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

LEAGUE = os.environ.get("LEAGUE")
MODEL = os.environ.get("MODEL")


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x720")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--v=99")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--homedir=/tmp")
    chrome_options.add_argument("--user-data-dir=/tmp/user-data")
    chrome_options.add_argument("--data-path=/tmp/data-path")
    chrome_options.add_argument("--disk-cache-dir=/tmp/cache-dir")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    )
    chrome_options.binary_location = "/opt/python/bin/headless-chromium"

    driver = webdriver.Chrome(
        "/opt/python/bin/chromedriver", chrome_options=chrome_options
    )
    return driver


# Login AWS Console URL with IAM ID
def login_aws_console(browser):
    url = "https://{}.signin.aws.amazon.com/console".format(USERNO)

    browser.get(url)
    browser.refresh()
    time.sleep(3)

    usernameInput = browser.find_elements_by_css_selector("form input")[1]
    passwordInput = browser.find_elements_by_css_selector("form input")[2]

    usernameInput.send_keys(USERNAME)
    passwordInput.send_keys(PASSWORD)
    passwordInput.send_keys(Keys.ENTER)
    time.sleep(2)

    print(
        f"Successfully logged in to AWS account number {USERNO} with username {USERNAME}"
    )


# Submit deepracer model to community races
def submit_model_to_community(browser):
    url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#{}".format(
        LEAGUE
    )

    xpath = "//span[contains(@class, 'awsui-select-option-label') and text() = '{}']".format(
        MODEL
    )

    browser.get(url)
    browser.refresh()
    time.sleep(8)

    browser.find_element_by_xpath('//*[@id="awsui-select-0-textbox"]').click()
    time.sleep(2)
    browser.find_element_by_xpath(xpath).click()
    time.sleep(1)

    submitModelButton = browser.find_element_by_xpath(
        '//button[@type="submit"]/*[text()="Submit model"]'
    )

    re_press_submit = 5
    while re_press_submit > 0:
        try:
            submitModelButton.click()
            re_press_submit -= 1
            time.sleep(2)
        except:
            # If click failed, means that submit was successful and we got re-routed to Event starting screen
            re_press_submit = 0

    time.sleep(3)
    print(
        f"[{(datetime.now() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}] Submitted model : {MODEL}"
    )


def handler(event, context):
    print(" ================ Starting Function ================ ")

    browser = get_driver()

    login_aws_console(browser)

    submit_model_to_community(browser)

    browser.quit()

    return {"statusCode": 200, "body": json.dumps("Submitted model : {MODEL}")}
