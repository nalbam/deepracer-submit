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

### single league

```bash
# config/deepracer.sh
export USERNO="123456789012"
export USERNAME="username"
export PASSWORD="password"

export ARN="arn:aws:deepracer:::leaderboard/"
export TARGET="tt" # [tt, oa, h2h, s-tt, s-oa]
export LEAGUE="league" # [league, summitLeague, competition]
export SEASON="virtual-season-2020-03-tt"
export MODEL="model-name"

export SLACK_TOKEN="xoxb-1111-2222-xxxx"
export SLACK_CHANNAL="#sandbox"
```

### multi league

```bash
# config/$LEAGUE.sh
export USERNO="123456789012"
export USERNAME="username"
export PASSWORD="password"

export TARGET_URL="https://nalbam.com/deepracer/submit.json"

export SLACK_TOKEN="xoxb-1111-2222-xxxx"
export SLACK_CHANNAL="#sandbox"
```

## usage

```bash
bash submit.sh
# or
bash submit.sh $TARGET
```

## crontab

```bash
3,23,43 * * * * /home/pi/deepracer-submit/submit.sh tt  > /tmp/submit-tt.log 2>&1
6,26,46 * * * * /home/pi/deepracer-submit/submit.sh oa  > /tmp/submit-oa.log 2>&1
9,36,49 * * * * /home/pi/deepracer-submit/submit.sh h2h > /tmp/submit-h2h.log 2>&1
```

## slack

![submit](./images/submit-tt.png)

![result](./images/result-tt.png)
