from django.shortcuts import render
from .models import Static



# Create your views here.




def about(request):
    about = Static.objects.get(id=1).about
    return render(request, 'site/about.html', {
        'about': about,
    })
    


def privacy(request):
    privacy = Static.objects.get(id=1).privacy
    return render(request, 'site/privacy.html', {
        'privacy': privacy,
    })
    
    
    

def return_policy(request):
    return_policy = Static.objects.get(id=1).return_policy
    return render(request, 'site/return.html', {
        'return_policy': return_policy,
    })