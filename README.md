### Clone this repo
$ git clone <url>

### Create virtual environment
$ mkvirtualenv -p "$(which python3)" -a "$(pwd)" -i scrapy==2.5.0 nepremicnine

### Settings
$ cp nepremicninespider/secrets.py.example nepremicninespider/secrets.py
$ cp cron.sh.example cron.sh
Edit accordingly

### Run spiders manually
$ scrapy crawl <spider_name>

### Set cron job (every day at 8am)
$ chmod a+x cron.sh
$ crontab -e
  0 8 * * * <project_directory>/cron.sh

