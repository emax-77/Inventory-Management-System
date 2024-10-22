from django.shortcuts import render, redirect
from .models import Product, Sale
from .forms import ProductForm, SaleForm
from django.http import HttpResponse
from django.template import loader

def product_list(request):
    sales = Sale.objects.all()
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products, "sales": sales})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

def sale_create(request):
    sales = Sale.objects.all()
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form, 'sales': sales})


def invoice_create(request):
    template = loader.get_template('invoice_form.html')
    return HttpResponse(template.render(request=request))
