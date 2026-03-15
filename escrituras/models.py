from django.db import models
import datetime

class Escritura(models.Model):

    codigo = models.CharField(max_length=20, blank=True)

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

    andamento = models.TextField(blank=True)

    observacoes = models.TextField(blank=True)

    def save(self, *args, **kwargs):

        if not self.codigo:

            ano = datetime.date.today().year

            ultimo = Escritura.objects.filter(codigo__startswith=f"ESC-{ano}").order_by("id").last()

            if ultimo:
                numero = int(ultimo.codigo.split("-")[-1]) + 1
            else:
                numero = 1

            self.codigo = f"ESC-{ano}-{numero:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo

from django.db import models

class Calculo(models.Model):

    valor_base = models.FloatField()
    tipo_ato = models.CharField(max_length=100)

    imposto = models.FloatField()
    escritura = models.FloatField()
    registro = models.FloatField()
    matricula = models.FloatField()

    total = models.FloatField()

    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_ato} - {self.valor_base}"