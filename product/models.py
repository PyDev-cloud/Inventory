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
    quantity=models.IntegerField()
    purchase_price=models.FloatField()
    sale_price=models.FloatField()
    thumbnail_image=models.ImageField(upload_to='images/')
    category=models.ForeignKey(category,related_name="Category",on_delete=models.CASCADE)
    SubCategory=models.ForeignKey(SubCategory,related_name="Subcategory",on_delete=models.CASCADE)
    unit_mesurement=models.FloatField()
    unit_type=models.CharField(max_length=50)
    sku=models.CharField(max_length=50)
    reorder_quantity=models.IntegerField()
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
    


class Purchase(models.Model):
    productname=models.ForeignKey(product,related_name="Product",on_delete=models.CASCADE)
    SupplierName=models.ForeignKey(Supplier,related_name="supplier",on_delete=models.CASCADE)
    totalAmount=models.FloatField()
    Discount=models.FloatField()
    DueAmount=models.FloatField()
    PaidAmount=models.FloatField()
    create_at=models.DateField(auto_now=True)
    update_at=models.DateField(auto_now=True)




class Customer(models.Model):
    name=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    Mobile=models.CharField(max_length=14)
    Address=models.CharField(max_length=100)

    def __str__(self):
        return self.name