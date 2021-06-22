import requests
import schedule
import time
import subprocess

def send_request():
    requests.post("https://rocky-meadow-70954.herokuapp.com/schedule.json", data={
        "project": "amazon_price_tracker",
        "spider": "tracker"
    })

if __name__ == "__main__":
    subprocess.run("scrapyd-deploy local", shell=True, universal_newlines=True)
    print("Starting the periodic scheduler...")
    schedule.every().hour.do(send_request)
    while True:
        schedule.run_pending()
        time.sleep(1)