from django.urls import path
from .views import *

urlpatterns = [
    path('category/',CategoryView.as_view(),name='category'),
    path('subcategory/',SubCategoryView.as_view(),name='subcategory'),
    path('product/', ProductView.as_view(), name='product'),
    path('supplier/',SupplierCreate.as_view(),name='supplier'),
    path('customer/',CustomerCreate.as_view(),name='customer')

]
