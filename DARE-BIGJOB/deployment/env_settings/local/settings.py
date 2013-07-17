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

GITHUB_APP_ID = 'aafd354d36d01b5c0cd9'
GITHUB_API_SECRET = 'b3d567fbd131b347bffaf4514cc40db69746f4d9'
