from django.shortcuts import render
from .models import Static
# Create your views here.
def about(request):
    about = Static.objects.get(id=1).about
    return render(request, 'site/about.html', {
        'about': about,
    })