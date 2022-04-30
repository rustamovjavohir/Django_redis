from django.http import HttpResponse
from django.shortcuts import render
from .tasks import test_func, this_is_my_first_project
# Create your views here.


def test_celery_func(request):
    res = test_func.delay()
    this_is_my_first_project.delay()
    try:
        return HttpResponse(res.status)
    except Exception as ex:
        return HttpResponse('String after 5 sec')


