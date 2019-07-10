# deepracer-submit

## usage

```bash
pip3 install pytest
pip3 install selenium

export userno=123456789012
export username=username
export password=password
export model=https://www.nalbam.com/deepracer/model.txt

pytest submit.py
```

## chromium

```bash
wget http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-codecs-ffmpeg_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
wget http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-codecs-ffmpeg-extra_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
wget http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
wget http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb

sudo dpkg -i chromium-codecs-ffmpeg_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
sudo dpkg -i chromium-codecs-ffmpeg-extra_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
sudo dpkg -i chromium-browser_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
sudo dpkg -i chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb
```

* https://sites.google.com/a/chromium.org/chromedriver/downloads
* http://ports.ubuntu.com/pool/universe/c/chromium-browser/
