from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, AddCompanyForm, AddCoCategoryForm
from django.contrib.auth.models import User
from .models import Company, CoCategory
from accounting.forms import DepitForm, CreditForm
import json

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, ('You Logged in Successfully'))
            return redirect('users')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ('There Was An Error Logging in'))
            return redirect('login')
    else:
        return render(request, 'members/login.html', {})
    

    
def logout_user(request):
    logout(request)
    messages.success(request, ('You Logged Out!'))
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ('You Registred Successfully'))
            return redirect('home')
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error Registering' + error_message))
            return render(request, 'members/register.html', {'form' : form, 'errors': errors})
    else:
        form = RegisterUserForm()
        return render(request, 'members/register.html', {'form' : form})



def home(request):
    return render(request, 'home.html', {})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    pay_form = DepitForm()
    receive_form = CreditForm()
    context = {
        'user':user,
        'pay_form': pay_form,
        'receive_form': receive_form,
        }
    return render(request, 'members/user_profile.html', context)

def users(request):
    context = {'users': User.objects.all()}
    return render(request, 'members/users.html', context)



def add_company(request):
    if request.method == 'POST':
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, ('The Company has been Added Successfully!'))
            return redirect('companies')
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error Registering' + error_message))
            return render(request, 'members/add_company.html', {'form' : form, 'errors': errors})
    else:
        co_form = AddCompanyForm()
        cat_form = AddCoCategoryForm()
        return render(request, 'members/company/add_company.html', {
            'form' : co_form,
            'co_category_form': cat_form
            })
    

def update_company(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if request.method == 'POST':
        form = AddCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, ('The Company has been Updated Successfully!'))
            return redirect('co_profile', slug = slug)
    else:
        form = AddCompanyForm(instance=company)
    return render(request, 'members/company/update_company.html', {'form': form})




def delete_company(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if request.method == 'POST':
        company.delete()
        messages.success(request, ('The Company has been Deleted Successfully!'))
        return redirect('companies')





def co_profile(request, slug):
    company = get_object_or_404(Company, slug=slug)
    form = AddCompanyForm(instance = company)
    context = {
        'company': company,
        'form' : form,
        }
    return render(request, 'members/company/co_profile.html', context)



def co_list(request):
    context = {'companies': Company.objects.all()}
    return render(request, 'members/company/co_list.html', context)



def add_co_category(request):
    if request.method == 'POST':
        form = AddCoCategoryForm()
        data = json.loads(request.body)
        print(data)
        category = form.save(commit=False)
        category.name = data['name']
        category.description = data['description']
        category.save()
        print(category)
        json_data = json.dumps({
            'category' : {
                'name': category.name,
                'id' : category.id
            }
        })
        messages.success(request, ('The Category has been Added Successfully!'))
        return HttpResponse(json_data, content_type="application/json")
    

def update_co_category(request, slug):
    category  = get_object_or_404(CoCategory, slug=slug)
    if request.method == 'POST':
        form = AddCoCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, ('The Company Category has been Updated Successfully!'))
            return redirect('co_category_list')
    else:
        form = AddCoCategoryForm(instance=category)
    return render(request, 'members/company_category/update_co_category.html', {
        'form': form,
        'category': category
        })


def delete_co_category(request, slug):
    category = get_object_or_404(CoCategory, slug=slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, ('The Category has been Deleted Successfully!'))
        return redirect('co_category_list')
    

def co_category_list(request):
    context = {
        'categories': CoCategory.objects.all(),
        'co_category_form': AddCoCategoryForm()
        }
    return render(request, 'members/company_category/co_category_list.html', context)


def co_category_profile(request, slug):
    category = get_object_or_404(CoCategory, slug=slug)
    companies = Company.objects.filter(category = category)
    form = AddCompanyForm()
    context = {
        'category': category,
        'companies' : companies,
        'form' : form
        }
    return render(request, 'members/company_category/co_category_profile.html', context)

