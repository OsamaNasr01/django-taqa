from django.shortcuts import render, redirect
from .models import Tender, Question, Choice
from django.contrib import messages
from members.views import home
from .forms import QuestionForm, ChoiceForm

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
    choice_form = ChoiceForm()
    return render(request, 'tenders/tender_profile.html', {
        'tender': tender,
        'questions': Question.objects.filter(tender = tender),
        'question_form': question_form,
        'choice_form': choice_form,
        
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
        messages.success(request, 'تم اضافة السؤال الي نموذج المناقصة بنجاح.')
        return tender_profile(request, tender.id)
        
        
def delete_question(request, id):
    if request.method == 'POST':
        question = Question.objects.get(id =id)
        tender = Tender.objects.get(id = question.tender.id)
        question.delete()
        messages.success(request, 'تم حذف السؤال من نموذج المناقصة بنجاح. ')
        return tender_profile(request, tender.id)
    
    
def update_question(request, id):
    question = Question.objects.get(id = id)
    tender = Tender.objects.get(id = question.tender.id)
    if request.method == 'POST':
        form = QuestionForm(request.POST,instance = question)
        new_question = form.save(commit=False)
        new_question.tender = tender
        new_question.save()
        messages.success(request, 'تم تعديل صيغة السؤال بنجاح.')
        return tender_profile(request, tender.id)
    else:
        form = QuestionForm(instance = question)
        return render(request, 'tenders/question_update.html', {
            'form':form,
            'question':question,
            })
        
        
def add_choice(request):
    question_id = request.POST['question_id']
    print(question_id)
    question = Question.objects.get(id = question_id)
    print(question.text)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        choice = form.save(commit=False)
        choice.question = question
        choice.save()
        messages.success(request, 'تم اضافة الاختيار بنجاح')
        return tender_profile(request, question.tender.id)
    


def delete_choice(request, id):
    if request.method == 'POST':
        choice = Choice.objects.get(id =id)
        tender = Tender.objects.get(id = choice.question.tender.id)
        choice.delete()
        messages.success(request, 'تم حذف الاختيار من نموذج المناقصة بنجاح. ')
        return tender_profile(request, tender.id)