FROM ubuntu
USER root

ENV BUNDLE_SILENCE_ROOT_WARNING=1

RUN apt-get update && apt-get -y install curl gnupg unzip wget python python-dev python-pip

# Install python dependencies
RUN pip install pytest
RUN pip install selenium

# Set the Chrome repo
RUN wget -qO - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome
RUN apt-get update && apt-get -y install google-chrome-stable

# Chrome Driver
RUN mkdir -p /opt/selenium \
    && wget -q http://chromedriver.storage.googleapis.com/75.0.3770.90/chromedriver_linux64.zip -O /opt/selenium/chromedriver_linux64.zip \
    && cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;

WORKDIR /src
ADD . /src

CMD ["sh", "-c", "/bin/bash ./submit.sh"]
