from django.shortcuts import redirect


class LogoutRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(f'User authenticated: {request.user.is_authenticated}')
            return redirect('home')  
        else:
            return super(LogoutRequiredMixin,self).dispatch(request, *args, **kwargs)