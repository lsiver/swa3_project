from celery import Celery
from chem.DC.antoine_data_scraper import build_antoine_list_oneshot
from chem.DA.bindist import BinDist
import os

redis_url = os.environ.get('REDIS_URL','redis://localhost:6379')
celery = Celery('distillation_tasks', broker=redis_url)

celery.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    result_expires=3600,
)

@celery.task(bind=True)
def scrape_antoine_data(self):
    print("task started: scraping NIST")
    #background task to scrape antoine data from NIST
    try:
        print("calling oneshot")
        build_antoine_list_oneshot()
        print("task completed")
        return {'status':'success','message':'Antoine data updated successfully'}
    except Exception as e:
        print('task FAILED')
        if self.request.retries < 3:
            print(f"retrying... (attempt {self.request.retries +1}")
            raise self.retry(countdown = 60, exc=e)
        return {'status':'failed','error':str(e)}