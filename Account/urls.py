from django.urls import path
from .views import Login,Logout,home,Registration
urlpatterns = [
    path('', home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/',Registration.as_view(),name="registration"),

]
