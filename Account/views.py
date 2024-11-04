from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,RegisterForm
from .mixins import LogoutRequiredMixin

# Create your views here.
@method_decorator(never_cache, name="dispatch")
class home(LoginRequiredMixin,generic.TemplateView):
    template_name = 'home.html'  # Specify your template here
    login_url = 'login'          # Redirect to the login page if not logged in

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin:index')  # Redirect to the Django admin page
        return super().get(request, *args, **kwargs)

    
@method_decorator(never_cache,name="dispatch")
class Login(LogoutRequiredMixin,generic.View):
    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(self.request, 'Account/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            user = authenticate(
            self.request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
            
            )
            
            if user:
                login(self.request, user)
                return redirect(self.request.GET.get('next', 'home'))
            
            else:
                messages.warning(self.request, "Invalid credentials. Please try again.")
                
                return redirect('login')
            
        else:
            print(form.errors)
            messages.error(self.request, "Form is not valid. Please check the input.")
            return render(self.request, 'Account/login.html', {'form': form})


class Logout(generic.View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('login')
    


class Registration(LogoutRequiredMixin,generic.CreateView):
    template_name="Account/register.html"
    form_class=RegisterForm
    success_url=reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Registration Successfull !")
        return super().form_valid(form)