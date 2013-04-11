from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def input_captcha(request):
    print request.POST
    print request.FILES
    return HttpResponse('OK|12345')


@csrf_exempt
def result_captcha(request):
    print request.GET
    return HttpResponse('OK|sd1fa')
