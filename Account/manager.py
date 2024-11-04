from django.contrib.auth.models import BaseUserManager

class BaseUser(BaseUserManager):
    def create_user(self,email,username,password,**extra_fields):
        if not username:
            raise ValueError("Please input valid UserName")
        
        if not email:
            raise ValueError("please input valid Email")
        
        email=self.normalize_email(email)
        user=self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
        
    

    def create_superuser(self,email,password,username,**extra_fields):
        user=self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.save()
        return user