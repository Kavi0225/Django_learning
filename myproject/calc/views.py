from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'new.html',{'name':"kavi"})

def add(request):
    num_1 = request.POST['num1']
    num_2 = request.POST['num2']
    res = int(num_1) + int(num_2)
    return render(request,'result.html',{'result':res})
