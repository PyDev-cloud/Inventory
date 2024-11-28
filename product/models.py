
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
    



class Stock(models.Model):
    product = models.ForeignKey(Product, related_name="stock", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock for {self.product.name}"

    def add_stock(self, quantity):
        """Increase stock quantity based on the purchase quantity."""
        self.quantity+= quantity # Simply add the exact purchase quantity
          # Simply add the exact purchase quantity
        self.save()

    def reduce_stock(self, quantity):
        """Reduce stock quantity based on the sale quantity."""
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
        else:
            raise ValueError(f"Not enough stock for {self.product.name}. Available: {self.quantity}")

    def get_available_stock(self):
        """Return the current stock quantity."""
        return self.quantity
class PurchaseInvoice(models.Model):
    
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.FloatField()
    due_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Due', 'Due')], default='Due')
    
    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        self.due_amount = self.total_amount - self.paid_amount
        super().save(*args, **kwargs)



class Purchase(models.Model):
    productname = models.ForeignKey(Product, related_name="Product", on_delete=models.CASCADE)
    suppliername = models.ForeignKey(Supplier, related_name="supplier", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    dueAmount = models.DecimalField(max_digits=10, decimal_places=2)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now=True)
    invoice = models.ForeignKey(PurchaseInvoice, related_name="purchase", on_delete=models.CASCADE, null=True, blank=True)  # Link to Invoice

    def save(self, *args, **kwargs):
        # Automatically calculate totalAmount and dueAmount before saving
        self.totalAmount = (self.productname.purchase_price - self.discount) * self.quantity
        self.dueAmount = self.totalAmount - self.paidAmount

        # Add stock when purchase is made
        stock, created = Stock.objects.get_or_create(product=self.productname)
        stock.add_stock(self.quantity) # Add stock based on purchase quantity 

        # Check if an invoice already exists for this purchase, if not, create one and link it to the purchase
        if not self.invoice:  # Ensure only one invoice is created, and it's linked to the Purchase instance
            invoice = PurchaseInvoice.objects.create(
                invoice_number=str(uuid.uuid4()),  # Generate a unique invoice number
                total_amount=self.totalAmount,
                discount=self.discount,
                paid_amount=self.paidAmount,
            )
            self.invoice = invoice  # Assign the created invoice to the Purchase instance

        super(Purchase, self).save(*args, **kwargs) 

    def delete(self, *args, **kwargs):
        # Before deleting the purchase, reduce stock by the quantity of the purchase
        stock = Stock.objects.get(product=self.productname)
        stock.reduce_stock(self.quantity)  # Reduce stock based on purchase quantity

        super(Purchase, self).delete(*args, **kwargs)
        # Automatically create PurchaseInvoice when purchase is saved
        

    def __str__(self):
        return f'Purchase of {self.productname.name} from {self.suppliername.name}'
    



class Customer(models.Model):
    name=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    Mobile=models.CharField(max_length=14)
    Address=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Selles(models.Model):
    product = models.ForeignKey(Product, related_name="ProductP", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    customer = models.ForeignKey(Customer, related_name="customerC", on_delete=models.CASCADE)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    discountAmount = models.DecimalField(max_digits=10, decimal_places=2)
    paidAmount = models.DecimalField(max_digits=10, decimal_places=2)
    DueAmount = models.IntegerField()
    create_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now=True)
    invoice = models.ForeignKey(PurchaseInvoice, related_name="sales", on_delete=models.CASCADE)  # Link to Invoice
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
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
        
        # Calculate totalPrice (product price * quantity)
        if self.product:
            self.totalPrice = (self.product.sale_price - self.discountAmount) * self.quantity

        # Calculate DueAmount: totalPrice - paidAmount - discountAmount
        self.DueAmount = self.totalPrice - self.paidAmount

        # Reduce stock when sale is made
        stock = Stock.objects.get(product=self.product)
        stock.reduce_stock(self.quantity)  # Decrease stock based on sale quantity

        # For Profit Calculation 
        product = self.product
        purchase_price = product.purchase_price
        self.profit = Decimal(purchase_price) * self.quantity - self.totalPrice
        
        super(Selles, self).save(*args, **kwargs)

    def __str__(self):
        return f'Sell of {self.product.name} to {self.customer.name}'
    



    
