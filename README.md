# deepracer-submit

## install (raspberrypi, ubuntu)

```bash
sudo apt update
sudo apt install -y xvfb jq
sudo apt install -y chromium-browser
sudo apt install -y chromium-codecs-ffmpeg
sudo apt install -y chromium-chromedriver

pip3 install --upgrade -r requirements.txt
```

## install (Amazon Linux 2)

* <https://aws.amazon.com/ko/premiumsupport/knowledge-center/ec2-linux-2-install-gui/>

```bash
sudo amazon-linux-extras install -y mate-desktop1.x
sudo amazon-linux-extras install -y epel

sudo yum install -y git jq
sudo yum install -y chromium chromedriver

sudo pip3 install --upgrade -r requirements.txt
```

## config

```bash
vi config/deepracer.json
```

```json
{
  "userno": "123456789012",
  "username": "username",
  "password": "password",
  "mfa": "base32secret3232",
  "slack": {
    "token": "xoxb-xxx-xxx-xxx",
    "channel": "sandbox"
  },
  "races": [
    {
      "name": "pro",
      "arn": "league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F9f6ca6de-ecfa-467a-a7d9-c899a811a206",
      "models": [
        "my-model-01",
        "my-model-02"
      ]
    },
    {
      "name": "comm",
      "arn": "competition/arn%3Aaws%3Adeepracer%3A%3A968005369378%3Aleaderboard%2F290c3134-d259-4b13-a390-c899a811a206",
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
./submit.py -t open -d True
```

## crontab

```bash
10,20,30,40,50 * * * * /home/ec2-user/deepracer-submit/submit.py -t pro > /tmp/submit.log 2>&1
```

## slack

![submit](./images/submit-tt.png)
