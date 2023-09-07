from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from .models import Category, Product, Brand, Price, Spec
from .forms import AddCategoryForm, AddProductForm, BrandForm, PriceForm, SpecForm, NumSpecForm, TxtSpecForm, BoolSpecForm
from django.contrib import messages
import json
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

# Create your views here.

def p_category_list(request):
    categories = Category.objects.filter(parent_id = 0)
    form = AddCategoryForm()
    return render(request, 'products/categories/p_category_list.html', {
        'categories':categories,
        'form': form,
        })



@login_required(login_url='login')
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
        }
    return render(request, 'products/categories/p_category_profile.html', context)



@login_required(login_url='login')
def update_p_category(request, slug):
    category  = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.image = request.FILES.get('image')
            cat.save()
            messages.success(request, ('The Company Category has been Updated Successfully!'))
            return p_category_profile(request, category.slug)
    else:
        form = AddCategoryForm(instance=category)
    return render(request, 'products/categories/update_p_category.html', {
        'form': form,
        'category': category
        })


@login_required(login_url='login')
def delete_p_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, ('The category has been Deleted Successfully!'))
        return redirect('p_category_list')


@login_required(login_url='login')
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
            price = price_form.save(commit=False)
            price.product = productt
            price.save()
            specs = category.specs.all()
            for spec in specs:
                spec_type = spec.type
                if spec_type == 1:
                    spec_form = NumSpecForm(request.POST)
                    spec_value = spec_form.save(commit=False)
                    spec_value.value = request.POST.get(spec.name)
                    spec_value.spec = spec
                    spec_value.product = productt
                    spec_value.save()
                if spec_type == 2:
                    spec_form = TxtSpecForm(request.POST)
                    spec_value = spec_form.save(commit=False)
                    spec_value.value = request.POST.get(spec.name)
                    spec_value.spec = spec
                    spec_value.product = productt
                    spec_value.save()
                if spec_type == 3:
                    spec_form = BoolSpecForm(request.POST)
                    spec_value = spec_form.save(commit=False)
                    if request.POST.get(spec.name):
                        print(request.POST.get(spec.name))
                        spec_value.value = True
                    else:
                        spec_value.value = False
                    spec_value.spec = spec
                    spec_value.product = productt
                    spec_value.save()                       
            messages.success(request, ('The Product has been Added Successfully!'))
            return product(request, productt.slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error adding the category' + error_message))
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
    in_cart = product.cart.filter(user=request.user)
    if in_cart:
        no_in_cart = product.cart.get(user=request.user).q
    else:
        no_in_cart =0
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
        }
    return render(request, 'products/products/product.html', context)


@login_required(login_url='login')
def update_product(request, slug):
    productt  = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=productt,)
        if form.is_valid():
            form.save()
            for spec in productt.num_spec.all():
                spec_form = NumSpecForm(instance = spec)
                spec_value = spec_form.save(commit=False)
                spec_value.value = request.POST.get(spec.spec.name)
                spec_value.save()
            for spec in productt.txt_spec.all():
                spec_form = TxtSpecForm(instance = spec)
                spec_value = spec_form.save(commit=False)
                spec_value.value = request.POST.get(spec.spec.name)
                spec_value.save()
            for spec in productt.bool_spec.all():
                spec_form = BoolSpecForm(instance = spec)
                spec_value = spec_form.save(commit=False)
                spec_value.value = request.POST.get(spec.spec.name)
                spec_value.save()
            messages.success(request, ('The Product Category has been Updated Successfully!'))
            return product(request, productt.slug)
    else:
        form = AddProductForm(instance=product)
    return render(request, 'products/products/update_product.html', {
        'form': form,
        'product': product
        })


@login_required(login_url='login')
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
def delete_brand(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if request.method == 'POST':
        brand.delete()
        messages.success(request, ('The Brand has been Deleted Successfully!'))
        return redirect('brands')
    

@login_required(login_url='login')
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
def add_spec(request):
    if request.method == 'POST':
        form = SpecForm(request.POST)
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.category = category
            spec.save()
            messages.success(request, ('The Specification has been Added Successfully!'))
            return p_category_profile(request, category.slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error adding the specification' + error_message))
            return p_category_profile(request, category.slug)


@login_required(login_url='login')
def update_spec(request, id):
    spec = get_object_or_404(Spec, id=id)
    if request.method == 'POST':
        form = SpecForm(request.POST, instance=spec)
        if form.is_valid():
            form.save()
            messages.success(request, ('The Specification has been Updateded Successfully!'))
            return p_category_profile(request, spec.category.slug)
        else:
            errors = form.errors
            error_message = errors.as_text().split(':')[0]
            messages.error(request, ('There Was An Error adding the Brand' + error_message))
            return render(request, 'products/specs/update_spec.html', {'form' : form, 'errors': errors})
    else:
        form = SpecForm(instance = spec)
        return render(request, 'products/specs/update_spec.html', {'form': form})
    
@login_required(login_url='login')
def delete_spec(request, id):
    spec = get_object_or_404(Spec, id=id)
    category_slug = spec.category.slug
    if request.method == 'POST':
        spec.delete()
        messages.success(request, ('The specification has been Deleted Successfully!'))
        return p_category_profile(request, category_slug)
    
def order_spec(request):
    pass