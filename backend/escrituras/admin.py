from django.contrib import admin
from .models import Escritura


class EscrituraAdmin(admin.ModelAdmin):

    readonly_fields = ("codigo",)

    list_display = (
        "codigo",
        "data_lavratura",
        "outorgante",
        "outorgado",
        "livro",
        "paginas",
        "status",
    )

    search_fields = (
        "codigo",
        "outorgante",
        "outorgado",
        "livro",
        "paginas",
    )


admin.site.register(Escritura, EscrituraAdmin)