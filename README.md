# deepracer-submit

## install (raspberrypi, ubuntu)

```bash
sudo apt update
sudo apt install -y xvfb jq
sudo apt install -y chromium-browser
sudo apt install -y chromium-codecs-ffmpeg
sudo apt install -y chromium-chromedriver

pip3 install pytest
pip3 install selenium
pip3 install xvfbwrapper
pip3 install slacker
```

## install (Amazon Linux 2)

* <https://aws.amazon.com/ko/premiumsupport/knowledge-center/ec2-linux-2-install-gui/>

```bash
sudo amazon-linux-extras install -y mate-desktop1.x
sudo amazon-linux-extras install -y epel

sudo yum install -y git jq
sudo yum install -y chromium chromedriver

sudo pip3 install pytest
sudo pip3 install selenium
sudo pip3 install xvfbwrapper
sudo pip3 install slacker
```

## config

```bash
vi config/deepracer.json
```

```json
{
  "userno": "",
  "username": "username",
  "password": "password",
  "slack": {
    "token": "",
    "channel": "#sandbox"
  },
  "leaderboards": [
    {
      "name": "2022-04-pro",
      "arn": "league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F2487f90e-3cd5-48e0-a264-bb8a1742f54c",
      "models": [
        "my-model-01",
        "my-model-02"
      ]
    }
  ]
}
```

## submit

```bash
./submit.py -t 2022-04-pro -d True
```

## crontab

```bash
10,20,30,40,50 * * * * /home/ec2-user/deepracer-submit/submit.py -t 2022-04-pro > /tmp/submit.log 2>&1
```

## slack

![submit](./images/submit-tt.png)
