from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from authentication.constants import COURSES, USER_PERMISSIONS


class Profile(models.Model):
    '''
    Essa classe é um Perfil de usuário, relacionada a um User do sistema.
    Ela apresenta dados número de matrícula, etc...
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    course = models.IntegerField(choices=COURSES, null=True, blank=True)
    user_permissions = models.IntegerField(choices=USER_PERMISSIONS, null=False, blank=False)

    code = models.CharField(max_length=50, blank=False, null=False, unique=True)

    class Meta:
        ordering = ('name',)
