from django.shortcuts import render
from apps.settings.models import Config, Gym, Room


# Create your views here.
def frontpage(request):
    return render(request,'frontpage.html')

def contact(request):
    return render(request,'contact.html')

def settings(request):
    configs = Config.objects.all()
    context = {
        'configs' : configs
    }
    return render(request, 'settings.html',context)