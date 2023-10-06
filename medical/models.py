from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta


class Recommendation(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)  
    phone = models.CharField(max_length=20,  null=True, blank=True)
    email = models.CharField(max_length=100,  null=True, blank=True)
    street = models.CharField(max_length=100,  null=True, blank=True)
    number = models.CharField(max_length=50,  null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Users(AbstractUser):
    Association = (('Particular', 'particular'), ('Convênio', 'convenio'),)
    UF = (
        ('RO', 'Rondônia'),
        ('AC', 'Acre'),
        ('AM', 'Amazonas'),
        ('RR', 'Roraima'),
        ('PA', 'Pará'),
        ('AP', 'Amapá'),
        ('TO', 'Tocantins'),
        ('MA', 'Maranhão'),
        ('PI', 'Piauí'),
        ('CE', 'Ceará'),
        ('RN', 'Rio Grande do Norte'),
        ('PB', 'Paraíba'),
        ('PE', 'Pernambuco'),
        ('AL', 'Alagoas'),
        ('SE', 'Sergipe'),
        ('BA', 'Bahia'),
        ('MG', 'Minas Gerais'),
        ('ES', 'Espírito Santo'),
        ('RJ', 'Rio de Janeiro'),
        ('SP', 'São Paulo'),
        ('PR', 'Paraná'),
        ('SC', 'Santa Catarina'),
        ('RS', 'Rio Grande do Sul'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('GO', 'Goiás'),
        ('DF', 'Distrito Federal'),
    )
    email = models.EmailField(unique=True)
    cpf = models.CharField('CPF', max_length=50, null=True)
    # avatar = models.ImageField(
    #     upload_to='medical/avatars/%Y/%m/%d/')
    birth_date = models.DateField('Data de Nascimento', null=True)
    street = models.CharField('Rua', max_length=100, null=True)
    number = models.CharField('Numero', max_length=50, null=True)
    district = models.CharField('Bairro', max_length=100, null=True)
    uf = models.CharField('UF', choices=UF, max_length=2, null=True)
    phone = models.CharField('Celular', max_length=20, null=True)
    procedure = models.ManyToManyField(
        'Procedure', through='UserProcedure', blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    association = models.CharField(
        'Associação', choices=Association, max_length=20, null=True)
    bariatric = models.DateField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            self.password = make_password('opera')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)


class Procedure(models.Model):

    title = models.CharField('Nome do procedimento',
                             max_length=255, null=False)
    description = models.TextField('Descrição', null=False)
    days_limit = models.IntegerField('Limite de dias', null=False)

    recommendation = models.ManyToManyField(
        Recommendation, blank=True, through='ProcedureReco')
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)


class ProcedureReco(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(
        Recommendation, on_delete=models.CASCADE)


class UserProcedure(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="procedures")
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    done = models.BooleanField('Feito', default=False)
    date_limit = models.DateField(null=True, blank=True)
    date_done = models.DateField(null=True, blank=True)
    type_procedure = models.BooleanField(null=True)


    # def save(self, *args, **kwargs):
    #     if not self.date_limit:
    #         self.date_limit = self.procedure.date_limit
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.procedure.title}'
