from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from .models import Category, Product, Brand, Price, Spec, Choice, SpecValue
from .forms import AddCategoryForm, AddProductForm, BrandForm, PriceForm, SpecForm, ChoiceForm
from django.contrib import messages
import json
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from posts.models import Post

# Create your views here.


def admin_company(user):
    return user.is_superuser or user.has_company()

def is_superuser(user):
    return  user.is_superuser



def has_company(user):
    return user.has_company()

def p_category_list(request):
    categories = Category.objects.all()
    form = AddCategoryForm()
    return render(request, 'products/categories/p_category_list.html', {
        'categories':categories,
        'form': form,
        })


 
@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def add_p_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            if request.POST.get('category_id'):
                parent_category_id = request.POST.get('category_id')
                parent_category = Category.objects.get(id=parent_category_id)
                category.parent_id = parent_category.id
            else:
                category.parent_id = 0
            category.image = request.FILES.get('image')
            category.save()
            messages.success(request, ('The Category has been Added Successfully!'))
            return p_category_profile(request, category.slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error adding the category' + error_message))
            return render(request, 'products/categories/add_p_category.html', {'form' : form, 'errors': errors})
    else:
        form = AddCategoryForm()
        return render(request, 'products/categories/add_p_category.html', {'form' : form})
    


def p_category_profile(request, slug):
    category = get_object_or_404(Category, slug=slug)
    sub_categories = Category.objects.filter(parent_id = category.id)
    form = AddProductForm()
    price_form = PriceForm()
    brand_form = BrandForm()
    category_form = AddCategoryForm()
    update_category_form = AddCategoryForm(instance = category)
    spec_form = SpecForm()
    context = {
        'category': category,
        'sub_categories': sub_categories,
        'products' : Product.objects.filter( category= category),
        'form' : form,
        'price_form' : price_form,
        'category_form': category_form,
        'update_category_form': update_category_form,
        'spec_form' : spec_form,
        'brand_form': brand_form,
        'choiceform': ChoiceForm(),
        }
    return render(request, 'products/categories/p_category_profile.html', context)



@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def update_p_category(request, slug):
    category  = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.image = request.FILES.get('image')
            cat.save()
            messages.success(request, ('تم تعديل بيانات القسم بنجاح'))
            return p_category_profile(request, category.slug)
    else:
        form = AddCategoryForm(instance=category)
    return render(request, 'products/categories/update_p_category.html', {
        'form': form,
        'category': category
        })


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def delete_p_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, ('تم حذف القسم بنجاح'))
        return redirect('p_category_list')


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        price_form = PriceForm(request.POST)
        if form.is_valid() and price_form.is_valid():
            productt = form.save(commit=False)
            category_id = request.POST.get('category_id')
            category = Category.objects.get(id=category_id)
            productt.category = category
            productt.save()                       
            messages.success(request, ('تم اضافة المنتج بنجاح'))
            price = price_form.save(commit=False)
            price.product = productt
            price.save()                       
            messages.success(request, ('تم اضافة السعر للمنتج بنجاح'))
            specs = category.specs.all()
            for spec in specs:
                if spec.type == 1:
                    new_spec_value = request.POST[f'{spec.id}']
                elif spec.type == 2:
                    if spec.choices:
                        choice = Choice.objects.get(id= request.POST[f'{spec.id}'])
                        new_spec_value = choice.text
                    else:
                        new_spec_value = request.POST[f'{spec.id}']
                elif spec.type == 3:
                        try:
                            request.POST[f'{spec.id}']
                            new_spec_value = 1
                        except:
                            new_spec_value = 0
                SpecValue.objects.create(
                    spec = spec, product = productt, value = new_spec_value
                )                       
            messages.success(request, ('تم اضافة جميع خصائص المنتج بنجاح'))
            return product(request, productt.slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('حدث خطأ اثناء اضافة المنتج' ))
            return render(request, 'products/products/add_product.html', {'form' : form, 'errors': errors})
    else:
        form = AddProductForm()
        return render(request, 'products/products/add_product.html', {'form' : form})
    
def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    specs = Spec.objects.filter(category = product.category)
    original_price = product.prices.last().value
    discount  = product.prices.last().discount
    price = (original_price * (100 - discount ))/100
    form = AddProductForm(instance = product)
    price_form = PriceForm(instance = product.prices.last())
    if request.user.is_authenticated:
        in_cart = product.cart.filter(user=request.user)
        if in_cart:
            no_in_cart = product.cart.get(user=request.user).q
        else:
            no_in_cart =0
    else:
        in_cart = 1
        no_in_cart = 0
    context = {
        'product' : product,
        'form' : form,
        'price_form' : price_form,
        'price': price,
        'original_price': original_price,
        'discount' : discount,
        'specs' : specs,
        'in_cart': in_cart,
        'no_in_cart': no_in_cart,
        'posts': Post.objects.filter(category = product.category),
        }
    return render(request, 'products/products/product.html', context)


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def update_product(request, slug):
    productt  = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=productt,)
        if form.is_valid():
            form.save()
            # for spec in productt.num_spec.all():
            #     spec_form = NumSpecForm(instance = spec)
            #     spec_value = spec_form.save(commit=False)
            #     spec_value.value = request.POST.get(spec.spec.name)
            #     spec_value.save()
            # for spec in productt.txt_spec.all():
            #     spec_form = TxtSpecForm(instance = spec)
            #     spec_value = spec_form.save(commit=False)
            #     spec_value.value = request.POST.get(spec.spec.name)
            #     spec_value.save()
            # for spec in productt.bool_spec.all():
            #     spec_form = BoolSpecForm(instance = spec)
            #     spec_value = spec_form.save(commit=False)
            #     spec_value.value = request.POST.get(spec.spec.name)
            #     spec_value.save()
            messages.success(request, ('The Product has been Updated Successfully!'))
            return product(request, productt.slug)
    else:
        form = AddProductForm(instance=product)
    return render(request, 'products/products/update_product.html', {
        'form': form,
        'product': product
        })


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        messages.success(request, ('The product has been Deleted Successfully!'))
        return redirect('p_category_list')


def brands(request):
    brands = Brand.objects.all()
    return render(request, 'products/brands/brands.html', {
        'brands': brands,
        'form' : BrandForm(),
    })


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm()
        brand = form.save(commit=False)
        brand.name = request.POST.get('name')
        brand.country =request.POST.get('country')
        brand.description = request.POST.get('description')
        brand.image = request.FILES.get('image')
        brand.save()
        brand.category.add(request.POST.get('category'))
        json_data = json.dumps({
            'brand_name': brand.name,
            'brand_id': brand.id
        })
        messages.success(request, ('The Brand has been Added Successfully!'))
        return HttpResponse(json_data, content_type="application/json")
    

def brand_profile(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    form = BrandForm(instance = brand)
    return render(request, 'products/brands/brand_profile.html', {
        'brand': brand,
        'form' : form,
    })


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def update_brand(request, slug):
    brand  = get_object_or_404(Brand, slug=slug)
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, ('The Brand Category has been Updated Successfully!'))
            return brand_profile(request, brand.slug)
    else:
        form = BrandForm(instance=brand)
    return render(request, 'products/brands/update_brand.html', {
        'form': form,
        'brand': brand
        })


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def delete_brand(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, ('The Brand has been Deleted Successfully!'))
        return redirect('brands')
    

@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def update_price(request, slug):
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            new_price = form.save(commit=False)
            productt = Product.objects.get(slug=slug)
            new_price.product = productt
            new_price.save()
            messages.success(request, ('The Price has been Updateded Successfully!'))
            return product(request, slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error adding the Brand' + error_message))
            return render(request, 'products/brands/add_brand.html', {'form' : form, 'errors': errors})

@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def add_spec(request):
    if request.method == 'POST':
        form = SpecForm(request.POST)
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.category = category
            spec.save()
            messages.success(request, ('تم اضافة الخاصية بنجاح'))
            return p_category_profile(request, category.slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('حدث خطأ أثناء اضافة الخاصية'))
            return p_category_profile(request, category.slug)


@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def update_spec(request, id):
    spec = get_object_or_404(Spec, id=id)
    if request.method == 'POST':
        form = SpecForm(request.POST, instance=spec)
        if form.is_valid():
            form.save()
            messages.success(request, ('تم تعديل خاصية المنتج بنجاح'))
            return p_category_profile(request, spec.category.slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('حدث خطأأثناء تعديل البيانات'))
            return render(request, 'products/specs/update_spec.html', {'form' : form, 'errors': errors})
    else:
        form = SpecForm(instance = spec)
        return render(request, 'products/specs/update_spec.html', {
            'form': form,
            'spec': spec,
            })
    
@login_required(login_url='login')  
@user_passes_test(admin_company, login_url='company_only')  
def delete_spec(request, id):
    spec = get_object_or_404(Spec, id=id)
    category_slug = spec.category.slug
    if request.method == 'POST':
        spec.delete()
        messages.success(request, ('تم حذف الخاصية بنجاح'))
        return p_category_profile(request, category_slug)
     


@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')      
def add_choice_spec(request):
    spec_id = request.POST['spec_id']
    spec = Spec.objects.get(id = spec_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        choice = form.save(commit=False)
        choice.spec = spec
        choice.save()
        messages.success(request, 'تم اضافة الاختيار بنجاح')
        return p_category_profile(request, spec.category.slug)
    


@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def delete_choice_spec(request, id):
    if request.method == 'POST':
        choice = Choice.objects.get(id =id)
        category = Category.objects.get(id = choice.spec.category.id)
        choice.delete()
        messages.success(request, 'تم حذف الاختيار من نموذج خصائص القسم بنجاح. ')
        return p_category_profile(request, category.slug)
    
    

@login_required(login_url='login')
@user_passes_test(is_superuser, login_url='not_auth')  
def update_choice_spec(request, id):
    choice = Choice.objects.get(id = id)
    category = Category.objects.get(id = choice.spec.category.id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST,instance = choice)
        new_choice = form.save(commit=False)
        new_choice.spec = choice.spec
        new_choice.save()
        messages.success(request, 'تم تعديل صيغة الاختيار بنجاح.')
        return p_category_profile(request, category.slug)
    else:
        form = ChoiceForm(instance = choice)
        return render(request, 'products/specs/update_choice.html', {
            'form':form,
            'choice':choice,
            })
        
