import pytz
import requests
import subprocess
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor

def send_request():
    requests.post('https://moodscape-web-crawler.herokuapp.com/schedule.json', data={
        'project': 'crawler',
        'spider': 'article'
    })

if __name__ == '__main__':
    subprocess.run('scrapyd-deploy', shell= True, universal_newlines= True)
    scheduler = TwistedScheduler(timezone= pytz.timezone('Asia/Jakarta'))
    
    # cron trigger that schedules job every day on 12:00 PM
    scheduler.add_job(send_request, 'cron', hour= 12)
    
    # start the scheduler
    scheduler.start()
    reactor.run()
