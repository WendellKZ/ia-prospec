import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","dev-key")
    DB_URL = os.getenv("DB_URL","sqlite:///app.db")
    USE_MOCK = os.getenv("USE_MOCK","1") == "1"
    BD_PROJECT_ID = os.getenv("BD_PROJECT_ID","")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS","")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", os.getenv("REDIS_URL","redis://localhost:6379/0"))
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", os.getenv("REDIS_URL","redis://localhost:6379/0"))
    MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY","2"))
    CELERY_TASK_ALWAYS_EAGER = os.getenv("CELERY_TASK_ALWAYS_EAGER","0") == "1"
