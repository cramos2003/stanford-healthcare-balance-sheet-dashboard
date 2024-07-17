import schedule
import time
from datetime import datetime
import logging
from utils import get_past_day
import os
from scraper import *

def run_scraper():
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f"/logs/{today}.log"
    # Creates empty log file
    if not os.path.exists(log_file):
        open(log_file, "a")
    else:
        pass
    # log file config
    logging.basicConfig(filename=log_file, encoding="utf-8", level=logging.INFO,
                        filemode="a", format='%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # start scraping
    logging.info(f"Started scraping: {datetime.now()}") # logs start time
    scraper()
    logging.info(f"Finished scraping: {datetime.now()}")

    # deletes log files 10 days and older
    del_date = get_past_day('day', 10)
    log_delete = f"/logs/{del_date}.log"
    try:
        os.remove(log_delete)
    except Exception as msg:
        print(f"Log: {log_delete}.log, skipping delete for log!")
    else:
        print(f"Deleting: {log_delete}.log")
        
        
schedule.every().day.at("01:00") # runs every day at 1 a.m.

while True:
    schedule.run_pending()
    time.sleep(1)