from celery import Celery

# Khởi tạo Celery instance
celery = Celery(__name__, broker='redis://192.168.200.128:6379/0')
