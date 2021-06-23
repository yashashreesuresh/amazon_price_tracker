import pytz
import requests
import subprocess
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor


def send_request():
    requests.post("https://rocky-meadow-70954.herokuapp.com/schedule.json", data={
        "project": "amazon_price_tracker",
        "spider": "tracker"
    })

if __name__ == "__main__":
    subprocess.run("scrapyd-deploy local", shell=True, universal_newlines=True)
    print("Starting the periodic scheduler...")
    scheduler = TwistedScheduler(timezone=pytz.timezone('Asia/Kolkata'))
    scheduler.add_job(send_request, 'cron', day_of_week='mon-sun', hour='10', minute='00')
    scheduler.start()
    reactor.run()