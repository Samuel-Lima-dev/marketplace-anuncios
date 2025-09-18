from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


#Criando autenticação personalisada
#Colocando E-mail como campo principal do login
class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é um campo obrigatório')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        #Garantindo que os campos de permissão do superusuario seja True por padrão
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        #Verificar se os valores estão corretamente como True
        if extra_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must have is_superuser=True')
       
        return self.create_user(email, password, **extra_fields)
        
class User(AbstractUser):
    username = None
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
