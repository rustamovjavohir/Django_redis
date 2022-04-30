from django.urls import path
from .views import test_celery_func

urlpatterns = [
    path('', test_celery_func, name='test'),
]
