from django import forms
from .models import Product, Sale, Invoice

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'category', 'quantity_in_stock', 'price', 'description']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold']

class InvoiceForm(forms.ModelForm):
    sales = forms.ModelMultipleChoiceField(
        queryset=Sale.objects.all(),  # Query all sales to choose from
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for multiple selection
    )
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'sales']
