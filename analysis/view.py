from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from analysis import models


@method_decorator(csrf_exempt, name='dispatch')
class Analysis(View):
    def get(self, request, handle):
        print("Handle: ", handle)

        responseData = models.base64image()

        return HttpResponse(responseData, content_type='application/json')
