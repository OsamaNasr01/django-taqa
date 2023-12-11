from django.shortcuts import render, redirect
from .models import Tender, Question
from django.contrib import messages
from members.views import home
from .forms import QuestionForm

# Create your views here.
def add_tender(request):
    if request.method == 'POST':
        tender = Tender.objects.create()
        tender.name = request.POST['name']
        tender.description = request.POST['description']
        tender.image = request.FILES['image']
        tender.save()
        messages.success(request, 'تم اضافة المناقصة بنجاح')
        return tender_profile(request, tender.id)
    else:
        return render(request, 'tenders/add_tender.html', {})
    
    
def tender_profile(request, id):
    tender = Tender.objects.get(id = id)
    question_form = QuestionForm()
    return render(request, 'tenders/tender_profile.html', {
        'tender': tender,
        'questions': Question.objects.filter(tender = tender),
        'question_form': question_form,
    })



def tender_update(request, id):
    tender = Tender.objects.get(id = id)
    if request.method == 'POST':
        tender.name = request.POST['name']
        tender.description = request.POST['description']
        tender.image = request.FILES['image']
        tender.save()
        messages.success(request, 'تم تعديل بيانات المناقصة بنجاح')
        return tender_profile(request, tender.id)
    else:
        return render(request, 'tenders/tender_update.html', {'tender':tender})
    
    
    
def tender_delete(request, id):
    tender = Tender.objects.get(id = id)
    tender.delete()
    messages.success(request, 'تم حذف المناقصة بنجاح')
    return home(request)
    
    
def tenders_list(request):
    tenders = Tender.objects.all()
    return render(request, 'tenders/tenders_list.html', {'tenders':tenders})



def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        question = form.save(commit=False)
        tender = Tender.objects.get(id = request.POST['tender_id'])
        question.tender = tender
        question.save()
        messages.success(request, 'تم اضافة السؤال الي نموذج المناقصة بنحاج.')
        return tender_profile(request, tender.id)
        