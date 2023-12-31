from django.shortcuts import render, redirect, HttpResponse
from .models import Tender, Question, Choice, TenderCategory, TenderRequest, Answer, OfferItem, TenderOffer, Terms
from django.contrib import messages
from members.views import home, users_only
from members.forms import AddAddressForm
from members.models import Gov, City
from products.models import Category, Product
from .forms import QuestionForm, ChoiceForm
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



def is_superuser(user):
    return  user.is_superuser



def has_company(user):
    return user.has_company()
# Create your views here.



@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def add_tender(request):
    if request.method == 'POST':
        tender = Tender.objects.create()
        tender.name = request.POST['name']
        tender.description = request.POST['description']
        tender.image = request.FILES['image']
        tender.save()
        messages.success(request, 'تم اضافة المناقصة بنجاح')
        return tender_dashboard(request, tender.id)
    else:
        return render(request, 'tenders/add_tender.html', {})
    
@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def tender_dashboard(request, id):
    tender = Tender.objects.get(id = id)
    question_form = QuestionForm()
    choice_form = ChoiceForm()
    categories = Category.objects.all()
    return render(request, 'tenders/tender_dashboard.html', {
        'tender': tender,
        'questions': Question.objects.filter(tender = tender),
        'question_form': question_form,
        'choice_form': choice_form,
        'categories': categories,  
        
    })
    
    
def not_allowed_page(request):
    return render(request, 'not_allowed.html', status=403)



@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def tender_update(request, id):
    tender = Tender.objects.get(id = id)
    if request.method == 'POST':
        tender.name = request.POST['name']
        tender.description = request.POST['description']
        tender.image = request.FILES['image']
        tender.save()
        messages.success(request, 'تم تعديل بيانات المناقصة بنجاح')
        return tender_dashboard(request, tender.id)
    else:
        return render(request, 'tenders/tender_update.html', {'tender':tender})
    
    

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def tender_delete(request, id):
    tender = Tender.objects.get(id = id)
    tender.delete()
    messages.success(request, 'تم حذف المناقصة بنجاح')
    return home(request)
    
    
def tenders_list(request):
    tenders = Tender.objects.all()
    return render(request, 'tenders/tenders_list.html', {'tenders':tenders})



@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        question = form.save(commit=False)
        tender = Tender.objects.get(id = request.POST['tender_id'])
        question.tender = tender
        question.save()
        messages.success(request, 'تم اضافة السؤال الي نموذج المناقصة بنجاح.')
        return tender_dashboard(request, tender.id)
        

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')          
def delete_question(request, id):
    if request.method == 'POST':
        question = Question.objects.get(id =id)
        tender = Tender.objects.get(id = question.tender.id)
        question.delete()
        messages.success(request, 'تم حذف السؤال من نموذج المناقصة بنجاح. ')
        return tender_dashboard(request, tender.id)
    

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')     
def update_question(request, id):
    question = Question.objects.get(id = id)
    tender = Tender.objects.get(id = question.tender.id)
    if request.method == 'POST':
        form = QuestionForm(request.POST,instance = question)
        new_question = form.save(commit=False)
        new_question.tender = tender
        new_question.save()
        messages.success(request, 'تم تعديل صيغة السؤال بنجاح.')
        return tender_dashboard(request, tender.id)
    else:
        form = QuestionForm(instance = question)
        return render(request, 'tenders/question_update.html', {
            'form':form,
            'question':question,
            })
        

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')      
def add_choice(request):
    question_id = request.POST['question_id']
    question = Question.objects.get(id = question_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        choice = form.save(commit=False)
        choice.question = question
        choice.save()
        messages.success(request, 'تم اضافة الاختيار بنجاح')
        return tender_dashboard(request, question.tender.id)
    


@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def delete_choice(request, id):
    if request.method == 'POST':
        choice = Choice.objects.get(id =id)
        tender = Tender.objects.get(id = choice.question.tender.id)
        choice.delete()
        messages.success(request, 'تم حذف الاختيار من نموذج المناقصة بنجاح. ')
        return tender_dashboard(request, tender.id)
    
    

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def update_choice(request, id):
    choice = Choice.objects.get(id = id)
    tender = Tender.objects.get(id = choice.question.tender.id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST,instance = choice)
        new_choice = form.save(commit=False)
        new_choice.question = choice.question
        new_choice.save()
        messages.success(request, 'تم تعديل صيغة الاختيار بنجاح.')
        return tender_dashboard(request, tender.id)
    else:
        form = ChoiceForm(instance = choice)
        return render(request, 'tenders/choice_update.html', {
            'form':form,
            'choice':choice,
            })
        

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')        
def add_category_to_tender(request):
    if request.method == 'POST':
        tender_id = request.POST['tender_id']
        tender = Tender.objects.get(id = tender_id)
        category = Category.objects.get(id = request.POST['category_id'])
        new_category = TenderCategory.objects.create(category= category , tender = tender)
        new_category.save()
        messages.success(request, 'تم اضافة القسم الي المناقصة بنجاح')
        return tender_dashboard(request, tender.id)
    

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def delete_category_from_tender(request, id):
    if request.method == 'POST':
        cat = TenderCategory.objects.get(id =id)
        tender = Tender.objects.get(id = cat.tender.id)
        cat.delete()
        messages.success(request, 'تم حذف القسم من نموذج المناقصة بنجاح. ')
        return tender_dashboard(request, tender.id)

@login_required(login_url='register')    
def tender_request(request, id):
    if request.user.has_company:
        return users_only(request)
    else:
        tender = Tender.objects.get(id = id)
        if request.method == 'POST':
            address_form = AddAddressForm(request.POST)
            new_address = address_form.save(commit=False)
            new_address.city = City.objects.get(id=request.POST['city'])
            new_address.details = request.POST['details']
            new_address.save()
            print('ok')
            new_request = TenderRequest.objects.create(
                user = request.user, location = new_address, tender = tender
            )
            for question in tender.questions.filter(re_of = 1):
                if question.type == 1:
                    new_answer_text = request.POST[f'{question.id}']
                elif question.type == 2:
                    if question.choices:
                        choice = Choice.objects.get(id= request.POST[f'{question.id}'])
                        new_answer_text = choice.text
                    else:
                        new_answer_text = request.POST[f'{question.id}']
                elif question.type == 3:
                        try:
                            x =  request.POST[f'{question.id}']
                            new_answer_text = 1
                        except:
                            new_answer_text = 0
                new_answer = Answer.objects.create(
                    question = question, request = new_request, text = new_answer_text
                )
            messages.success(request, 'تم قبول الطلب بنجاح')
            return tender_request_profile(request, new_request.id)
        else:   
            address_form = AddAddressForm()
            return render(request, 'tenders/requests/add_request.html', {
                'tender':tender,
                'questions': tender.questions.filter(re_of = 1),
                'address_form':address_form,
                'govs': Gov.objects.all()
                })
        


def tender_profile(request, id):
    tender = Tender.objects.get(id = id)
    return render(request, 'tenders/tender_profile.html', {
        'tender':tender
    })
    
def tender_request_profile(request, id):
    tender_request = TenderRequest.objects.get(id = id)
    return render(request, 'tenders/requests/profile.html', {
        'tender_request': tender_request,
    })
    

@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only')  
def product_selection(request, id):
    tender_request =  TenderRequest.objects.get(id = request.POST['tender_request'])
    offer = TenderOffer.objects.get(id =id)
    count = int(request.POST['count'])
    i=0
    for category in tender_request.tender.categories.all():
        if category == tender_request.tender.categories.last():  
            return render(request, 'tenders/requests/add_offer.html',  {
                'category': category,
                'tender_request':tender_request,
                'count':'الاخيرة',
                'offer':offer,
                })
        else:
            if i == count: 
                count +=1   
                return render(request, 'tenders/requests/add_offer.html',  {
                    'category': category,
                    'tender_request':tender_request,
                    'count':count,
                    'offer':offer,
                    })
            i+=1
    

@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only')    
def add_offer(request):
    tender_request =  TenderRequest.objects.get(id = request.POST['tender_request'])
    if request.method  == 'POST':
        offer = TenderOffer.objects.create(
            request = tender_request,
            company = request.user.company.last(),
        )
        return product_selection(request, offer.id)


@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only') 
def add_product_offer(request):
    product = Product.objects.get(id = request.POST['product_id'])
    offer_product = OfferItem.objects.create(
        product = product,
        offer = TenderOffer.objects.get(id = request.POST['offer_id']),
        qty = request.POST['qty'],
        price = request.POST['price'],
    )
    offer_product.save()
    messages.success(request, f'تم اضافة {product.name} بنجاح')
    json_data = json.dumps({'data':'added'})
    return HttpResponse(json_data, content_type="application/json")

@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only') 
def remove_product_offer(request):
    offer_product = OfferItem.objects.get(
        product = Product.objects.get(id = request.POST['product_id']),
        offer = TenderOffer.objects.get(id = request.POST['offer_id']),
        )
    offer_product.delete()
    messages.error(request, f'تم حذف {offer_product.product.name} بنجاح')
    json_data = json.dumps({'data':'removed'})
    return HttpResponse(json_data, content_type="application/json")


@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only')  
def offer_terms(request, id):
    if request.method == 'POST':
        offer = TenderOffer.objects.get(id = id)
        questions = Question.objects.filter(re_of = 2, tender = offer.request.tender)
        return render(request, 'tenders/requests/offer_terms.html', {
            'offer': offer,
            'questions': questions,
        })

@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only')  
def submit_terms(request, id):
    offer = TenderOffer.objects.get(id = id)
    if request.method == 'POST':
        for question in offer.request.tender.questions.filter(re_of = 2):
            if question.type == 1:
                new_answer_text = request.POST[f'{question.id}']
            elif question.type == 2:
                if question.choices:
                    choice = Choice.objects.get(id= request.POST[f'{question.id}'])
                    new_answer_text = choice.text
                else:
                    new_answer_text = request.POST[f'{question.id}']
            elif question.type == 3:
                    try:
                        request.POST[f'{question.id}']
                        new_answer_text = 1
                    except:
                        new_answer_text = 0
                    
            new_term = Terms.objects.create(
                question = question, offer = offer, text = new_answer_text
            )
        messages.success(request, 'تم إضافة الشروط الي العرض بنجاح')
        return confirm_offer(request, id)
        

@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only')              
def confirm_offer(request, id):
    if request.method == 'POST':
        return render(request, 'tenders/requests/confirm_offer.html', {
            'offer': TenderOffer.objects.get(id = id)
        })

@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only')    
def send_offer(request):
    if request.method == 'POST':
        offer = TenderOffer.objects.get(id = request.POST['offer_id'])
        offer.submit = True
        offer.save()
        messages.success(request, 'تم ارسال العرض للعميل، وسيتم موافاتكم اذا تم قبول العرض  .')
        return render(request, 'tenders/requests/offer_profile.html', {
            'offer': offer,
        })
        

@login_required(login_url='login')
def offer_profile(request, id):
    offer = TenderOffer.objects.get(id = id )
    return render(request, 'tenders/requests/offer_profile.html', {
        'offer': offer,
    })
    
    

@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only') 
def change_item_price(request):
    data = json.loads(request.body)
    item = OfferItem.objects.get(id = data['item_id'])
    offer = TenderOffer.objects.get(id = item.offer.id)
    offer.value -= item.item_value
    item.price = data['new_price']
    item.save()
    offer.value += item.item_value
    offer.save()
    return_data = {
        'item_value': item.item_value,
        'offer_value': offer.value,
    }
    json_data = json.dumps(return_data)
    print(json_data)
    return HttpResponse(json_data, content_type="application/json")



@login_required(login_url='login')  
@user_passes_test(has_company, login_url='company_only') 
def change_item_q(request):
    data = json.loads(request.body)
    item = OfferItem.objects.get(id = data['item_id'])
    offer = TenderOffer.objects.get(id = item.offer.id)
    offer.value -= item.item_value
    item.qty = data['new_q']
    item.save()
    offer.value += item.item_value
    offer.save()
    return_data = {
        'item_value': item.item_value,
        'offer_value': offer.value,
    }
    json_data = json.dumps(return_data)
    print(json_data)
    return HttpResponse(json_data, content_type="application/json")
