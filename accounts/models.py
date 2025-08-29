from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



#Criando autenticação personalisada
#Colocando E-mail como campo principal do login


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('O email é um campo obrigatório')
        
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin=True
        user.save(using=self._db)
        return user
        
        

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email



class NaturalPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoa_fisica')
    name = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False, unique=True)
    date_birth = models.DateField()
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LegalPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoa_juridica')
    name = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=14, null=False, blank=False, unique=True)
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
