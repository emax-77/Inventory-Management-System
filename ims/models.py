from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=True)
    quantity_in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    # Method to check stock level and send email if low
    def check_stock(self):
        if self.quantity_in_stock < 2:
            send_mail(
                'Low Stock Alert',
                f'Stock for {self.name} is low: {self.quantity_in_stock}',
                'my_testing_email77@gmail.com',
                ['peter.wirth@gmail.com'],
            )

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    # decrement quantity_in_stock when a sale is created
    def save(self, *args, **kwargs):
        self.product.quantity_in_stock -= self.quantity_sold
        self.product.save()
        self.product.check_stock()
        super().save(*args, **kwargs)
    
    # increment quantity_in_stock when a sale is deleted
    def delete(self, *args, **kwargs):
        self.product.quantity_in_stock += self.quantity_sold
        self.product.save()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f"Sale of {self.quantity_sold} {self.product.name}"
    
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    sales = models.ManyToManyField('Sale')  # Link to Sale model
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.invoice_number

