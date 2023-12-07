from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, AddCompanyForm, AddCoCategoryForm, DetailsForm, AccountForm
from .forms import AddAddressForm, AddGovForm, AddCityForm
from django.contrib.auth.models import User
from .models import Company, CoCategory, Details, Account
from products.models import Category, Product, Brand
from posts.models import Post
from sitestats.models import Site
from accounting.forms import DepitForm, CreditForm
import json
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, ('تم تسجيل الدخول بنجاح'))
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ('حدث خطأ اثناء الدخول! تأكد من صحة رقم التليفون ورمز الدخول..'))
            return redirect('login')
    else:
        return render(request, 'members/login.html', {})
    

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.warning(request, ('تم تسجيل الخروج بنجاح'))
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


@login_required(login_url='login')
def user_delete(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        if user == request.user or request.user.is_staff:
            user.delete()
            return users(request)
        else:
            return render(request, 'members/not_auth.html', {})

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()
    return render(request, 'home.html', {
        'categories' : categories,
        'products': products,
        'brands': brands,
        'posts': Post.objects.all()
    })

@login_required(login_url='login')
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user or request.user.is_staff:
        pay_form = DepitForm()
        receive_form = CreditForm()
        context = {
            'member':user,
            'pay_form': pay_form,
            'receive_form': receive_form,
            }
        return render(request, 'members/user_profile.html', context)
    else:
        return render(request, 'members/not_auth.html', {})

@login_required(login_url='login')
def users(request):
    context = {'users': User.objects.all()}
    return render(request, 'members/users.html', context)


@login_required(login_url='login')
def update_picture(request, username):
    user = get_object_or_404(User, username=username)
    account = Account.objects.get(user= user)
    account.image = request.FILES.get('image')
    account.save()
    return user_profile(request, user.username)
    



@login_required(login_url='login')
def add_company(request):
    if request.method == 'POST':
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.image = request.FILES.get('image')
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
    

@login_required(login_url='login')
def update_company(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if request.method == 'POST':
        form = AddCompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, ('The Company has been Updated Successfully!'))
            return redirect('co_profile', slug = slug)
    else:
        form = AddCompanyForm(instance=company)
    return render(request, 'members/company/update_company.html', {'form': form})




@login_required(login_url='login')
def delete_company(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if request.method == 'POST':
        company.delete()
        messages.success(request, ('The Company has been Deleted Successfully!'))
        return redirect('companies')





@login_required(login_url='login')
def co_profile(request, slug):
    company = get_object_or_404(Company, slug=slug)
    form = AddCompanyForm(instance = company)
    context = {
        'company': company,
        'form' : form,
        }
    return render(request, 'members/company/co_profile.html', context)



@login_required(login_url='login')
def co_list(request):
    context = {'companies': Company.objects.all()}
    return render(request, 'members/company/co_list.html', context)



@login_required(login_url='login')
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
    

@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_co_category(request, slug):
    category = get_object_or_404(CoCategory, slug=slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, ('The Category has been Deleted Successfully!'))
        return redirect('co_category_list')
    

@login_required(login_url='login')
def co_category_list(request):
    context = {
        'categories': CoCategory.objects.all(),
        'co_category_form': AddCoCategoryForm()
        }
    return render(request, 'members/company_category/co_category_list.html', context)


@login_required(login_url='login')
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



@login_required
def add_gov(request):
    if request.method == 'POST':
        form = AddGovForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_gov')
    else:
        form = AddGovForm()
        return render(request, 'members/address/add_gov.html', {'form': form})
    
    

@login_required
def add_city(request):
    if request.method == 'POST':
        form = AddCityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_city')
    else:
        form = AddCityForm()
        return render(request, 'members/address/add_city.html', {'form': form})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_city')
    else:
        form = AddAddressForm()
        return render(request, 'members/address/add_city.html', {'form': form})
    
    
def paymob(request):
    return render(request, 'members/paymob/paymob.html', {})



def payment_status(request):
    return render(request, 'members/paymob/payment_status.html', {})