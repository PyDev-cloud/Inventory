from django.db import models


# Create your models here.


class category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self) :
        return self.name

class SubCategory(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(category,related_name="category",on_delete=models.CASCADE)
    def __str__(self) :
        return self.name

class product(models.Model):
    name=models.CharField(max_length=100)
    purchase_price=models.FloatField()
    sale_price=models.FloatField()
    thumbnail_image=models.ImageField(upload_to='images/')
    category=models.ForeignKey(category,related_name="Category",on_delete=models.CASCADE)
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
    product = models.ForeignKey(product, related_name="stock", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock for {self.product.name}"

    def add_stock(self, quantity):
        """Increase stock quantity based on the purchase quantity."""
        self.quantity += quantity
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



class Purchase(models.Model):
    productname=models.ForeignKey(product,related_name="Product",on_delete=models.CASCADE)
    suppliername=models.ForeignKey(Supplier,related_name="supplier",on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalAmount=models.FloatField()
    discount=models.FloatField()
    dueAmount=models.FloatField()
    paidAmount=models.FloatField()
    create_at=models.DateField(auto_now=True)
    update_at=models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically calculate totalAmount and dueAmount before saving
        self.totalAmount = self.productname.purchase_price * self.quantity  # Total = Price * Quantity
        self.dueAmount = self.totalAmount - self.paidAmount - self.discount  # Due = Total - Paid - Discount
         # Add stock when purchase is made
        stock, created = Stock.objects.get_or_create(product=self.productname)
        stock.add_stock(self.quantity)  # Increase stock based on purchase quantity

        super(Purchase, self).save(*args, **kwargs)




class Customer(models.Model):
    name=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    Mobile=models.CharField(max_length=14)
    Address=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Selles(models.Model):
    product=models.ForeignKey(product,related_name="ProductP",on_delete=models.CASCADE)
    quantity=models.IntegerField()
    customer=models.ForeignKey(Customer,related_name="customerC",on_delete=models.CASCADE)
    totalPrice=models.IntegerField()
    discountAmount=models.IntegerField()
    paidAmount=models.IntegerField()
    DueAmount=models.IntegerField()
    create_at=models.DateField(auto_now=True)
    update_at=models.DateField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        # Calculate totalPrice (product price * quantity, assuming quantity field exists in Product or Selles)
        if self.product:  # Ensure the product exists
            self.totalPrice = self.product.sale_price * self.quantity  # assuming product has a price field

        # Calculate dueAmount: totalPrice - paidAmount - discountAmount
        self.DueAmount = self.totalPrice - self.paidAmount - self.discountAmount

         # Reduce stock when sale is made
        stock = Stock.objects.get(product=self.product)
        stock.reduce_stock(self.quantity)  # Decrease stock based on sale quantity

        # Now, save the instance
        super(Selles, self).save(*args, **kwargs)

    def __str__(self):
        return f'Sell of {self.product.name} to {self.customer.name}'