## Amazon Price Tracker :moneybag:

A cool scrapy spider that is used to notify the price drop in a product that you crave to buy!

1. Tracks availability and price of an amazon product of your wish. :gift:
2. Scheduled to run periodically everyday. :hourglass_flowing_sand:
3. Notifies through email on price drop. :email:
4. Deployed and scheduled periodically on Heroku for free. :money_with_wings:

### Deploying Scrapy Spider :spider:
You can deploy your scrapy spider locally and on [Heroku](https://dashboard.heroku.com/apps) by following the steps below.
You can deploy your scrapy spider peridically on Heroku for free similar to peridic scrapy spiders scheduled on [scrapy-cloud](https://www.zyte.com/scrapy-cloud/) that comes with paid account upgrade.

#### Steps to deploy to scrapyd

1. Install scrapy daemon by executing `pip3 install scrapyd`.
2. Install scrapy-client byexecuting `pip3 install git+https://github.com/iamumairayub/scrapyd-client.git --upgrade`.
3. Execute `scrapyd` in one terminal.
4. Change `[deploy]` to `[deploy:local] or [deploy:<str>]` in scrapy.cfg.
5. Uncomment the `url = http://localhost:6800/` under `[deploy]` in scrapy.cfg.
5. Execute `scrapyd-deploy local` in another terminal.
6. Execute `curl http://localhost:6800/schedule.json -d project=myntra -d spider=gadgets` to start the spider ececution.
7. Execute step 6 and step 7 whenever a change is made in the project to update the same in scrapy daemon.
8. Execute `curl http://localhost:6800/cancel.json -d project=myntra -d job=<job_id>` to stop the running spider.

#### Steps to deploy to Heroku

1. Install herokuify_scrapyd by executing `pip3 install herokuify_scrapyd`.
2. Create requirement.txt file by executing `pip3 freeze > requirements.txt`.
3. Create Procfile and runtime.txt file.
4. Login to Heroku: `heroku login -i`.
5. Create heroku app by executing `heroku create`.
6. Copy the url (eg, `https://limitless-waters-77333.herokuapp.com/`) returned and paste it under [deploy] section in scrapy.cfg.
7. Add `[scrapyd]` section in scrapy.cfg.
8. Add heroku to remote `heroku git:remote -a <app_name>`, for example, `heroku git:remote -a limitless-waters-77333`.
9. Push the code to heroku. `git init` -> `git add .` -> `git commit -m <commit_message>` -> `git push heroku master`.
10. Deploy the app. `scrapyd-deploy local` -> `curl https://limitless-waters-77333.herokuapp.com/schedule.json -d project=myntra -d spider=gadgets`.

#### Steps to periodically schedule scrapy spider in Heroku

Follow the above [steps 1-9](https://github.com/yashashreesuresh/amazon_price_tracker#steps-to-deploy-to-heroku) on deploying to Heroku. Continue with the steps below:
1. Install schedule module by executing `pip3 install schedule`.
2. Create [periodic_scheduler.py](https://github.com/yashashreesuresh/amazon_price_tracker/blob/master/periodic_scheduler.py) python file to create a scheduler.
3. Update the Procfile to create a clock dyno `clock: python3 periodic_scheduler.py`.
4. Update the requirement.txt file by executing `pip3 freeze > requirements.txt`.
5. Push the code changes to heroku. `git add .` -> `git commit -m <commit_message>` -> `git push heroku master`.
6. Execute `heroku ps:scale clock=1` to ensure the clock dyno component is a singleton process thereby avoiding scheduling duplicate jobs.

### Sending email in python :envelope_with_arrow:

Refer [this](https://realpython.com/python-send-email/) doc.

1. Using SMTP_SSL()
```
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
server.login(os.environ.get("sender_email"), os.environ.get("password"))
server.sendmail(os.environ.get("sender_email"), os.environ.get("receiver_email"), message)
```

2. Using .starttls()
```
context = ssl.create_default_context()
erver = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls(context=context)
server.ehlo()
server.login(os.environ.get("sender_email"), os.environ.get("password"))
server.sendmail(os.environ.get("sender_email"), os.environ.get("receiver_email"), message)
server.quit()
```