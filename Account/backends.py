from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model


User=get_user_model()

class EmailAuthenticateBackend(ModelBackend):
    def authenticate(self,request,username=None , password=None ,**kwargs):
        try:
            user=User.objects.get(email=username)
            if user.check_password(password):
                print("user is work")
                return user
            else:
                return None

        except ObjectDoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            user=User.objects.get(id=user_id)
            print(user.id)
            return user
        except ObjectDoesNotExist:
            return None

        
        
        