# Nepremicnine.net spider

### Clone this repo
```$ git clone https://github.com/eleksis/nepremicnine-spider.git```

### Create virtual environment
```
$ pip install virtualenv virtualenvwrapper
$ echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bashrc
$ echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
$ mkvirtualenv -p "$(which python3)" -a "$(pwd)" -i scrapy==2.5.0 nepremicnine
```

### Settings
```$ cp nepremicninespider/secrets.py.example nepremicninespider/secrets.py```
Edit accordingly.

### Create your spider for desired category/url
Example at `nepremicninespider/spiders/example.py`.

### Run spider manually
```
$ workon nepremicnine
$ scrapy crawl <spider_name>
```

### Set cron job (every day at 8am)
```
$ cp cron.sh.example cron.sh
$ chmod a+x cron.sh
$ crontab -e
  0 8 * * * <project_directory>/cron.sh
```
