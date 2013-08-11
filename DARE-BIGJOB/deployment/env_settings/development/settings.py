EMAIL_HOST_PASSWORD = 'tiger@123'
site = 2

BROKER_URL = 'redis://localhost:6379/0'
CELERY_SEND_EVENTS = True
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ("darewap.tasks", )
CELERY_RESULT_BACKEND = "redis://localhost/results"
CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.


#CELERY_ANNOTATIONS = {"tasks.add": {"rate_limit": "10/s"}}
#CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"

COMPRESS_OFFLINE = True
DEBUG = False

GITHUB_APP_ID = '4e5e370fc2b67f60391c'
GITHUB_API_SECRET = '9954bcb156932a3e7d677e26f2e3c63047a2e250'
