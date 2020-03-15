# deepracer-submit

## install

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

## config

### single league

```bash
# config/deepracer.sh
export USERNO="123456789012"
export USERNAME="username"
export PASSWORD="password"

export LEAGUE="tt"
export SEASON="2020-03-tt"
export MODEL="model"

export SLACK_TOKEN="xoxb-1111-2222-xxxx"
```

### multi league

```bash
# config/$LEAGUE.sh
export USERNO="123456789012"
export USERNAME="username"
export PASSWORD="password"

export LEAGUE_URL=""

export SLACK_TOKEN="xoxb-1111-2222-xxxx"
```

## usage

```bash
bash submit.sh
# or
bash submit.sh $LEAGUE
```

## crontab

```bash
0,15,30,45 * * * * /home/pi/deepracer-submit/submit.sh tt > /tmp/submit-tt.log 2>&1
```

## slack

![submit](./images/submit-tt.png)

![result](./images/result-tt.png)
