from django.shortcuts import render
from django.views.generic import View
from .models import todo
from .forms import todoForm
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from .models import todo
import json
import re
# Create your views here.

class todoView(View):
    """
    todo list 的视图
    """
    def get(self,request):
        return render(request,"api_todo.html")

    def post(self,request):
        a_dict = request.POST
        data = list((a_dict.keys()))[0]
        pattern = re.compile(r'\{.*?\}')
        for i in pattern.findall(data):
            temp = json.loads(i)
            item = todo(id=temp['id'], title=temp['title'], completed=temp['completed'])
            if not item in todo.objects.all():
                item.save()
        return HttpResponse('OK')

    def delete(self, request, id):
        todo.objects.get(id=id).delete()
        return HttpResponse('DELETE!')
def todojson(request):
    data = serializers.serialize('json', todo.objects.all())
    return HttpResponse(data,content_type="application/json, charset=utf-8")

