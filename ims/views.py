from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import Product, Sale, Invoice
from .forms import ProductForm, SaleForm, InvoiceForm
import json

# Main page view
def product_list(request):
    try:
        sales = Sale.objects.all()
        products = Product.objects.all()
        invoices = sorted(Invoice.objects.all(), key=lambda x: x.invoice_number)
    except Exception as e:
        return render(request, 'error_page.html', {'error': str(e)})
    return render(request, 'product_list.html', {'products': products, "sales": sales, "invoices": invoices})

# Create a new product
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

# Edit an existing product
def product_edit(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'error_page.html', {'error': 'Product not found.'})
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

# Delete a product
def product_delete(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'error_page.html', {'error': 'Product not found.'})
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

# Create a new sale
def sale_create(request):
    try:
        sales = Sale.objects.all()
    except Exception as e:
        return render(request, 'error_page.html', {'error': str(e)})

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form, 'sales': sales})

# Create a new invoice
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            try:
                invoice = form.save(commit=False)
                
                # Calculate total amount
                total_amount = 0
                for sale in form.cleaned_data['sales']:
                    total_amount += sale.product.price * sale.quantity_sold
                
                invoice.total_amount = total_amount
                invoice.save()
                form.save_m2m()  # To save the many-to-many relationships
                
                return redirect('invoice_detail', pk=invoice.pk)
            except Exception as e:
                return render(request, 'error_page.html', {'error': str(e)})
    else:
        form = InvoiceForm()
    return render(request, 'invoice_form.html', {'form': form})

# View an invoice + download as JSON file (optional)
def invoice_detail(request, pk):
    try:
        invoice = get_object_or_404(Invoice, pk=pk)
    except Http404:
        return render(request, 'error_page.html', {'error': 'Invoice not found.'})
    
    if request.method == 'POST':
        # Convert invoice to dictionary
        invoice_dict = {
            'invoice_number': invoice.invoice_number,
            'total_amount': float(invoice.total_amount),
            'sales': [
                {
                    'product': sale.product.name,
                    'quantity_sold': sale.quantity_sold,
                    'price': float(sale.product.price),
                    'total_amount': float(sale.product.price * sale.quantity_sold)
                }
                for sale in invoice.sales.all()
            ]
        }

        # Convert dictionary to JSON string
        invoice_json = json.dumps(invoice_dict, indent=4)

        # Create the response object and set file name
        response = HttpResponse(invoice_json, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.json"'
        # Download the file (return the response object)
        return response
    return render(request, 'invoice_detail.html', {'invoice': invoice})

# List all invoices
def invoice_list(request):
    try:
        invoices = sorted(Invoice.objects.all(), key=lambda x: x.invoice_number)
    except Exception as e:
        return render(request, 'error_page.html', {'error': str(e)})
    return render(request, 'invoice_list.html', {'invoices': invoices})

# Delete an invoice
def invoice_delete(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return render(request, 'error_page.html', {'error': 'Invoice not found.'})

    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'invoice_confirm_delete.html', {'invoice': invoice})
