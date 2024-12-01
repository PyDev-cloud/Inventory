
from decimal import Decimal
from django.db import models

import uuid

# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self) :
        return self.name

class SubCategory(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,related_name="category",on_delete=models.CASCADE)
    def __str__(self) :
        return self.name
    


class Product(models.Model):
    name=models.CharField(max_length=100)
    purchase_price=models.DecimalField(max_digits=10, decimal_places=2)
    sale_price=models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail_image=models.ImageField(upload_to='images/')
    category=models.ForeignKey(Category,related_name="Category",on_delete=models.CASCADE)
    SubCategory=models.ForeignKey(SubCategory,related_name="Subcategory",on_delete=models.CASCADE)
    unit_mesurement=models.FloatField()
    unit_type=models.CharField(max_length=50)
    sku=models.CharField(max_length=50)
    status=models.BooleanField(default=True)
    create_at=models.DateField(auto_now=True)
    update_at=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name
    



class Supplier(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    mobile=models.CharField(max_length=14)
    Address=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    name=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    Mobile=models.CharField(max_length=14)
    Address=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.ForeignKey(Product, related_name="stock", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
   





class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dueAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice = models.OneToOneField('PurchaseInvoice', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        
        # Check if an invoice already exists for this purchase, if not, create one and link it to the purchase
        if not self.invoice:  # Ensure only one invoice is created, and it's linked to the Purchase instance
            invoice, created = PurchaseInvoice.objects.get_or_create(
                invoice_number=str(uuid.uuid4()),  # Generate a unique invoice number
                total_amount=self.totalAmount,
                discount=self.discount,
                paid_amount=self.paidAmount,
            )
            self.invoice = invoice  # Assign the created invoice to the Purchase instance

        super(Purchase, self).save(*args, **kwargs)  # Save purchase

    def __str__(self):
        return f'Purchase of {self.supplier.name}'
    def __str__(self):
        return f'Purchase of {self.supplier.name}'



    
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchase_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    

    def save(self, *args, **kwargs):
        # Calculate totalAmount (quantity * unit_price)
        self.totalAmount = self.quantity * self.unit_price

        stock, created = Stock.objects.get_or_create(product=self.product)  # Get or create the Stock entry
        stock.quantity += self.quantity  # Increase the stock by the purchased quantity
        stock.save()  # Save the updated stock
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class PurchaseInvoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now=True)
    GrandTotal = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    dueAmount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

    
    


class Selles(models.Model):
    customer = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    discountAmount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    dueAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice = models.OneToOneField(PurchaseInvoice, null=True, blank=True, on_delete=models.SET_NULL)  # Link to Invoice
    
    
    def save(self, *args, **kwargs):
        # Ensure the invoice is created automatically if not exists
        if not self.invoice:
            invoice = PurchaseInvoice.objects.create(
                invoice_number=str(uuid.uuid4()),  # Generate a unique invoice number
                total_amount=self.totalPrice,
                discount=self.discountAmount,
                paid_amount=self.paidAmount,
            )
            self.invoice = invoice
        
        super(Selles, self).save(*args, **kwargs)

    def __str__(self):
        return f'Sell of  {self.customer.name}'
    



class SellesItem(models.Model):
    selles = models.ForeignKey(Selles, related_name='selles_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        item_names = ', '.join([str(item.product.name) for item in self.sellesitem_set.all()])
        return f'Sell of {item_names} to {self.customer.name}'

# SellesItem save method
    def save(self, *args, **kwargs):
        self.totalAmount = self.quantity * self.unit_price

        # Decrease stock on sale
        stock, created = Stock.objects.get_or_create(product=self.product)
        stock.quantity -= self.quantity  # Decrease the stock by the sold quantity
        stock.save()

        super().save(*args, **kwargs)
