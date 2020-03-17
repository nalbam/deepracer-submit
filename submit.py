# -*- coding: utf-8 -*-

import argparse
import os
import time
import urllib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from slacker import Slacker


USERNO = os.environ.get("USERNO")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

LEAGUE = os.environ.get("LEAGUE", "tt")
SEASON = os.environ.get("SEASON", "season")
MODEL = os.environ.get("MODEL", "model")

SLACK_TOKEN = os.environ.get("SLACK_TOKEN", "")
SLACK_CHANNAL = os.environ.get("SLACK_CHANNAL", "#sandbox")


def parse_args():
    p = argparse.ArgumentParser(description="deepracer submit")
    p.add_argument("--userno", default=USERNO, help="userno")
    p.add_argument("--username", default=USERNAME, help="username")
    p.add_argument("--password", default=PASSWORD, help="password")
    p.add_argument("-l", "--league", default=LEAGUE, help="league")
    p.add_argument("-s", "--season", default=SEASON, help="season")
    p.add_argument("-m", "--model", default=MODEL, help="model")
    p.add_argument("--slack-token", default=SLACK_TOKEN, help="slack token")
    p.add_argument("--slack-channal", default=SLACK_CHANNAL, help="slack channal")
    return p.parse_args()


def open_browser(args):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    # browser = webdriver.Chrome("/usr/local/bin/chromedriver")

    browser.set_window_size(1600, 1200)

    return browser


def colse_browser(args, browser):
    try:
        browser.close()
    except Exception as ex:
        print("Error", ex)


def login_aws(args, browser):
    print("login_aws", args.username)

    url = "https://{}.signin.aws.amazon.com/console".format(args.userno)

    browser.get(url)

    time.sleep(5)

    browser.save_screenshot("build/login-{}.png".format(args.league))

    browser.find_element_by_id("username").send_keys(args.username)
    browser.find_element_by_id("password").send_keys(args.password)

    browser.find_element_by_id("signin_button").click()

    time.sleep(5)

    browser.save_screenshot("build/login-{}.png".format(args.league))

    # post_slack(args,"login")


def load_model(args, browser):
    print("load_model")

    url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/{}".format(
        args.model
    )

    try:
        browser.get(url)

        time.sleep(10)

        browser.save_screenshot("build/load-{}.png".format(args.league))

        browser.find_element_by_class_name("awsui-button-variant-primary").click()

        time.sleep(10)

        browser.save_screenshot("build/load-{}.png".format(args.league))
    except Exception as ex:
        print("Error", ex)

    # post_slack(args,"load")


def submit_model(args, browser):
    print("submit_model", args.model)

    arn = urllib.parse.quote_plus(
        "arn:aws:deepracer:us-east-1::leaderboard/virtual-season"
    )

    # url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/{}/leaderboard/{}-{}/submitModel".format(
    #     args.model, arn, args.season
    # )

    url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#league/{}-{}/submitModel".format(
        arn, args.season
    )

    try:
        browser.get(url)

        time.sleep(10)

        browser.save_screenshot("build/submit-{}.png".format(args.league))

        browser.find_element_by_class_name("awsui-dropdown-trigger").click()

        for data in browser.find_elements_by_xpath(
            "//*[contains(@data-value)]/@data-value"
        ):
            print(data.text)

            arn = "arn:aws:deepracer:us-east-1:{}:model/reinforcement_learning/{}".format(
                args.userno, args.model
            )

            if data == arn:
                data.click()

        # element = browser.find_element_by_class_name("awsui-select-trigger-label")
        # browser.execute_script(
        #     'arguments[0].innerHTML = "{}";'.format(args.model), element
        # )

        browser.find_element_by_class_name("awsui-button-variant-primary").click()

        time.sleep(10)

        browser.save_screenshot("build/submit-{}.png".format(args.league))
    except Exception as ex:
        print("Error", ex)

    post_slack(args, "submit")


def result(args, browser):
    print("result")

    url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#league"

    try:
        browser.get(url)

        time.sleep(25)

        browser.save_screenshot("build/result-{}.png".format(args.league))
    except Exception as ex:
        print("Error", ex)

    post_slack(args, "result")


def post_slack(args, step):
    print("post_slack")

    millis = int(round(time.time() * 1000))

    file = "{}/build/{}-{}.png".format(os.getcwd(), step, args.league)
    text = "{} : {} : {} : {}".format(args.league, args.model, step, millis)

    try:
        slack = Slacker(args.slack_token)

        slack.files.upload(file, channels=[args.slack_channal], title=text)

    except KeyError as ex:
        print("Environment variable %s not set." % str(ex))


def main():
    args = parse_args()

    browser = open_browser(args)

    login_aws(args, browser)

    # load_model(args, browser)

    submit_model(args, browser)

    result(args, browser)

    colse_browser(args, browser)


if __name__ == "__main__":
    main()
