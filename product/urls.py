from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('category/',CategoryView.as_view(),name='category'),
    path('categoryList/',categoryViewlist.as_view(),name="categorylist"),
    path('category/<int:pk>/edit/',CategoryUpdateView.as_view(),name="categoryupdate"),

    path('subcategory/',SubCategoryView.as_view(),name='subcategory'),
    path('subcategoryList/',SubcategoryViewlist.as_view(),name="subcategorylist"),
    path('subcategory/<int:pk>/edit/',SubCategoryUpdateView.as_view(),name="subcategoryupdate"),

    path('product/', ProductView.as_view(), name='product'),
    path('productList/',Productlist.as_view(),name="productlist"),
    path('productUpdate/<int:pk>/edit/',ProductUpdateView.as_view(),name="productupdate"),

    path('supplier/',SupplierCreate.as_view(),name='supplier'),
    path('supplierlist/',SupplierList.as_view(),name="SupplierList"),

    path('customer/',CustomerCreate.as_view(),name='customer'),
    path('customerlist/',Customerlist.as_view(),name='customerlist'),
    path('customerUpdate/<int:pk>/edit/',CustomerUpdateView.as_view(),name="customerupdate"),


    
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
