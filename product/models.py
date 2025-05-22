
from decimal import Decimal
from django.db import models

import uuid

from django.forms import ValidationError

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
    Unite_TYPE_CHOICES = (
        
        ('KG', 'Kilogram'),
        ('PCS', 'Pieces'),
        
    )
    name=models.CharField(max_length=100)
    purchase_price=models.DecimalField(max_digits=10, decimal_places=2)
    sale_price=models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail_image=models.ImageField(upload_to='images/')
    category=models.ForeignKey(Category,related_name="Category",on_delete=models.CASCADE)
    SubCategory=models.ForeignKey(SubCategory,related_name="Subcategory",on_delete=models.CASCADE)
    unit_mesurement=models.FloatField()
    unit_type=models.CharField(max_length=10, choices=Unite_TYPE_CHOICES,null=False,blank=False)
    sku=models.CharField(max_length=50,blank=True,null=True)
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

class DamagedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        # স্টকে থাকা পরিমাণ চেক করা
        stock = Stock.objects.filter(product=self.product).first()
        if stock and self.quantity > stock.quantity:
            raise ValidationError("ড্যামেজ পরিমাণ স্টকের চেয়ে বেশি হতে পারে না।")


    def __str__(self):
        return f"Damaged: {self.product.name} ({self.quantity})"

class Stock(models.Model):
    product = models.ForeignKey(Product, related_name="stock", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
   
    @property
    def damaged_quantity(self):
        return self.product.damagedproduct_set.aggregate(total=models.Sum('quantity'))['total'] or 0




class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    alltotalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dueAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invoice = models.OneToOneField('PurchaseInvoice', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_product_amount(self):
        return sum(item.product_totalAmount for item in self.purchase_items.all())
    @property
    def grand_total(self):
        return self.alltotalAmount - self.discount

    def __str__(self):
        return f"Purchase {self.id}"


class PurchaseItem(models.Model):
    QUANTITY_TYPE_CHOICES = (
        
        ('KG', 'Kilogram'),
        ('PCS', 'Pieces'),
        
    )

    purchase = models.ForeignKey(Purchase, related_name='purchase_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    quantity_type = models.CharField(max_length=10, choices=QUANTITY_TYPE_CHOICES,null=False,blank=False, default="KG")  # <-- NEW FIELD
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        if not self.product:
            raise ValidationError("Product is required for each purchase item.")
        super().clean()

    

    def save(self, *args, **kwargs):
        if not self.product_totalAmount:
            self.product_totalAmount = self.quantity * self.unit_price
        super().save(*args, **kwargs)



def generate_invoice_number():
    last_invoice = SellesInvoice.objects.order_by('id').last()
    if not last_invoice or not last_invoice.invoice_number:
        return "INV-0001"

    try:
        last_number = int(last_invoice.invoice_number.split("-")[1])
    except (IndexError, ValueError):
        last_number = 0

    new_number = last_number + 1
    return f"INV-{new_number:04d}"




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

    
    


class SellesInvoice(models.Model):
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
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2,default=0,blank=True,null=True)
    discountAmount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    dueAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0,blank=True,null=True)
    invoice = models.OneToOneField(SellesInvoice, null=True, blank=True, on_delete=models.SET_NULL)  # Link to Invoice
    created_at = models.DateTimeField(auto_now_add=True)
    
   

    def save(self, *args, **kwargs):
        if not self.invoice:
            invoice = SellesInvoice.objects.create(
                invoice_number=generate_invoice_number(),  # ✅ Sequential Invoice Number
                total_amount=self.totalPrice or 0,
                discount=self.discountAmount,
                paid_amount=self.paidAmount,
                GrandTotal=self.totalPrice or 0,
                dueAmount=self.dueAmount or 0,
            )
            self.invoice = invoice

        super(Selles, self).save(*args, **kwargs)

    def __str__(self):
        return f'Sell of {self.customer.name}'



class SellesItem(models.Model):
    QUANTITY_TYPE_CHOICES = (
        
        ('KG', 'Kilogram'),
        ('PCS', 'Pieces'),
        
    )
    selles = models.ForeignKey(Selles, related_name='selles_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_type = models.CharField(max_length=10, choices=QUANTITY_TYPE_CHOICES,null=False,blank=False, default="KG")  # <-- NEW FIELD
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    
    def __str__(self):
        item_names = ', '.join([str(item.product.name) for item in self.selles.selles_items.all()])
        return f'Sell of {item_names} to {self.selles.customer.name}'

# SellesItem save method
    def save(self, *args, **kwargs):
        self.totalAmount = self.quantity * self.unit_price
        
        # Decrease stock on sale
        stock, created = Stock.objects.get_or_create(product=self.product)
        stock.quantity -= self.quantity  # Decrease the stock by the sold quantity
        stock.save()

        super().save(*args, **kwargs)




from django.db.models import F











