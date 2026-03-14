from django.contrib import admin
from django.urls import path
from escrituras.views import calculo

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', calculo, name="calculo"),

]