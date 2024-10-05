from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse

def product_list(request):
    context = {
        "products": Product.objects.all()
    }
    sort = request.GET.get('sort')
    if sort == "1":
        context['products'] = Product.objects.filter(is_available=True)
    elif sort == "2":
        context['products'] = Product.objects.all().order_by('-price')
    elif sort == "3":
        context['products'] = Product.objects.all().order_by('price')
        
    try:
        first_range = int(request.POST.get("first-range").replace(',', ''))
        second_range = int(request.POST.get("second-range").replace(',', ''))
    except:
        first_range = None
        second_range = None
    if first_range is not None and second_range is not None:
        context['products'] = Product.objects.filter(price__range=(first_range, second_range))

    search = request.GET.get('#')

    if search:
        context['products'] = Product.objects.filter(name__icontains=search)
        
    return render(request, 'products.html', context)


def product_detail(request, *args, **kwargs):
    product = Product.objects.get(id = kwargs['pk'])
    context = {
        'product': product
    }

    return render(request, 'single-product.html', context)
