from django import template

register = template.Library()


@register.filter
def moeda(valor):

    if valor is None:
        return ""

    try:
        valor = float(valor)
    except:
        return ""

    texto = f"{valor:,.2f}"

    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")

    return "R$ " + texto