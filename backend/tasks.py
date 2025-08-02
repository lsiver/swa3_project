from celery import Celery
from chem.DC.antoine_data_scraper import build_antoine_list_oneshot
from chem.DA.bindist import BinDist
import os
from api import app

redis_url = os.environ.get('REDIS_URL','redis://localhost:6379')
celery = Celery('distillation_tasks', broker=redis_url)

@celery.task(bind=True)
def scrape_antoine_data(self):
    #background task to scrape antoine data from NIST
    try:
        build_antoine_list_oneshot()
        return {'status':'success','message':'Antoine data updated successfully'}
    except Exception as e:
        if self.request.retries < 3:
            raise self.retry(countdown = 60, exc=e)
        return {'status':'failed','error':str(e)}