from django.shortcuts import render, redirect
from .models import Product, Sale
from .forms import ProductForm, SaleForm
from .forms import InvoiceForm
from .models import Invoice


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
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            
            # Calculate total amount
            total_amount = 0
            for sale in form.cleaned_data['sales']:
                total_amount += sale.product.price * sale.quantity_sold  
            
            invoice.total_amount = total_amount
            invoice.save()
            
            # Add the selected sales to the invoice
            form.save_m2m()
            
            return redirect('invoice_detail', pk=invoice.pk)  
    else:
        form = InvoiceForm()

    return render(request, 'invoice_form.html', {'form': form})

def invoice_detail(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    return render(request, 'invoice_detail.html', {'invoice': invoice})

def invoice_list(request):
    invoices = sorted(Invoice.objects.all(), key=lambda x: x.invoice_number)
    return render(request, 'invoice_list.html', {'invoices': invoices})

def invoice_delete(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'invoice_confirm_delete.html', {'invoice': invoice})
