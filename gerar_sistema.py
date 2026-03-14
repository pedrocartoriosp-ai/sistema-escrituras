import os

print("Criando Sistema Escrituras Pedro Lopes...")

pastas = [
    "backend",
    "backend/config",
    "backend/escrituras",
    "frontend",
    "docker",
    "backups"
]

for pasta in pastas:
    os.makedirs(pasta, exist_ok=True)

# manage.py
manage = """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""

open("backend/manage.py","w").write(manage)

# settings.py
settings = """
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-secret'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'escrituras'
]

MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / 'templates'],
'APP_DIRS': True,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages'
],
},
},
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}

STATIC_URL = '/static/'
"""

open("backend/config/settings.py","w").write(settings)

# models
models = """
from django.db import models

class Escritura(models.Model):

    codigo = models.CharField(max_length=20)

    data_lavratura = models.DateField()

    outorgante = models.CharField(max_length=200)
    outorgado = models.CharField(max_length=200)

    intermediador = models.CharField(max_length=200)

    livro = models.CharField(max_length=50)
    paginas = models.CharField(max_length=50)

    valor_escritura = models.DecimalField(max_digits=12, decimal_places=2)

    valor_registro = models.DecimalField(max_digits=12, decimal_places=2)

    valor_certidao = models.DecimalField(max_digits=12, decimal_places=2)

    telefone = models.CharField(max_length=30)

    email = models.CharField(max_length=200)

    status = models.CharField(max_length=100)

    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.codigo
"""

open("backend/escrituras/models.py","w").write(models)

# views
views = """
from django.shortcuts import render
from .models import Escritura

def consulta(request):

    codigo = request.GET.get("codigo")

    escritura = None

    if codigo:
        try:
            escritura = Escritura.objects.get(codigo=codigo)
        except:
            pass

    return render(request,"consulta.html",{"escritura":escritura})
"""

open("backend/escrituras/views.py","w").write(views)

# urls
urls = """
from django.contrib import admin
from django.urls import path
from escrituras.views import consulta

urlpatterns = [

path('admin/', admin.site.urls),

path('', consulta),

]
"""

open("backend/config/urls.py","w").write(urls)

# docker
docker = """
version: '3'

services:

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
"""

open("docker/docker-compose.yml","w").write(docker)

print("Sistema criado com sucesso!")