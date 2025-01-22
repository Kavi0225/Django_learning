from django.shortcuts import render
from .models import Destination
# Create your views here.
def index(request):
    dest1 = Destination()
    dest1.name = "Mumbai"
    dest1.desc = "The City That Never Sleep"
    dest1.img = "destination_4.jpg"
    dest1.price = 750
    dest1.offer = False

    dest2 = Destination()
    dest2.name = "Dehli"
    dest2.desc = "The City Capital Of India"
    dest2.img = "destination_3.jpg"
    dest2.price = 800
    dest2.offer = False

    dest3 = Destination()
    dest3.name = "Pune"
    dest3.desc = "High Tech City"
    dest3.img = "destination_9.jpg"
    dest3.price = 650
    dest3.offer = True

    dest = [dest1, dest2 , dest3]

    return render(request, "index.html", {'dest' : dest})
def about(request):
    return render(request, "about.html")

