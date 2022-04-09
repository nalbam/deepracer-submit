# -*- coding: utf-8 -*-

import argparse
import os
import time
import urllib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from slacker import Slacker


USERNO = os.environ.get("USERNO")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

ARN = os.environ.get("ARN", "arn")
TARGET = os.environ.get("TARGET", "tt")
LEAGUE = os.environ.get("LEAGUE", "league")
SEASON = os.environ.get("SEASON", "season")
MODEL = os.environ.get("MODEL", "model")

SLACK_TOKEN = os.environ.get("SLACK_TOKEN", "")
SLACK_CHANNAL = os.environ.get("SLACK_CHANNAL", "#sandbox")


def parse_args():
    p = argparse.ArgumentParser(description="deepracer submit")
    p.add_argument("--userno", default=USERNO, help="userno")
    p.add_argument("--username", default=USERNAME, help="username")
    p.add_argument("--password", default=PASSWORD, help="password")
    p.add_argument("-a", "--arn", default=ARN, help="arn")
    p.add_argument("-t", "--target", default=TARGET, help="target")
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

    browser.set_window_size(1600, 1700)

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

    browser.save_screenshot("build/login-{}.png".format(args.target))

    browser.find_element(By.ID, "username").send_keys(args.username)
    browser.find_element(By.ID, "password").send_keys(args.password)

    browser.find_element(By.ID, "signin_button").click()

    time.sleep(5)

    browser.save_screenshot("build/login-{}.png".format(args.target))

    # post_slack(args,"login")


def result(args, browser):
    print("result")

    # #league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F463824f5-78a6-4184-8bea-379e7b4219a1

    arn = urllib.parse.quote_plus(args.arn)

    url = (
        "https://console.aws.amazon.com/deepracer/home?region=us-east-1#{}/{}{}".format(
            args.league, arn, args.season
        )
    )

    # url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#{}".format(
    #     args.league
    # )

    try:
        browser.get(url)

        time.sleep(5)

        browser.save_screenshot("build/result-{}.png".format(args.target))
    except Exception as ex:
        print("Error", ex)

    post_slack(args, "result")


def post_slack(args, step):
    print("post_slack")

    if args.slack_token == "":
        return

    millis = int(round(time.time() * 1000))

    file = "{}/build/{}-{}.png".format(os.getcwd(), step, args.target)
    text = "{} : {} : {} : {}".format(args.target, args.model, step, millis)

    try:
        slack = Slacker(args.slack_token)

        slack.files.upload(file, channels=[args.slack_channal], title=text)

    except KeyError as ex:
        print("Environment variable %s not set." % str(ex))


def main():
    args = parse_args()

    if args.userno == "":
        return

    browser = open_browser(args)

    login_aws(args, browser)

    result(args, browser)

    colse_browser(args, browser)


if __name__ == "__main__":
    main()
