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

pip3 install --upgrade -r requirements.txt
```

## config

```bash
export ACCOUNT_ID='123456789012'

export DR_USERNAME='username'
export DR_PASSWORD='password'
export MFA_SECRET='' # BASE32_MFA_SECRET

export SLACK_TOKEN='xoxb-xxx-xxx-xxx'
export SLACK_CHANNEL='sandbox'
```

```bash
cat <<EOF > config/deepracer.json
{
  "debug": "False",
  "userno": "${ACCOUNT_ID}",
  "username": "${DR_USERNAME}",
  "password": "${DR_PASSWORD}",
  "mfa": "${MFA_SECRET}",
  "slack": {
    "token": "${SLACK_TOKEN}",
    "channel": "${SLACK_CHANNEL}"
  },
  "races": [
    {
      "name": "pro",
      "arn": "league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F689a6905-08c6-4589-b609-c54eca7ffd9e",
      "models": [
        "DR-MODEL-01", "DR-MODEL-02"
      ]
    },
    {
      "name": "comm",
      "arn": "competition/arn%3Aaws%3Adeepracer%3A%3A968005369378%3Aleaderboard%2F4fce8098-0a1f-4730-9fae-58c26397c043",
      "models": [
        "DR-MODEL-01", "DR-MODEL-02"
      ]
    }
  ]
}
EOF
```

## submit

```bash
./submit.py -t pro -d True
```

## crontab

```bash
cat <<EOF > config/crontab.sh
*/15 * * * * /home/ec2-user/deepracer-submit/submit.py -t pro > /tmp/submit-pro.log 2>&1
59 * * * * bash /home/ec2-user/run.sh restore
EOF
```

```bash
crontab config/crontab.sh
```

## slack

![submit](./images/submit-pro.png)
