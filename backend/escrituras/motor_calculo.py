from decimal import Decimal
import pandas as pd
import os
from django.conf import settings


CAMINHO_ESCRITURA = os.path.join(settings.BASE_DIR, "TabelaEscritura.xlsx")
CAMINHO_REGISTRO = os.path.join(settings.BASE_DIR, "TabelaRegistro.xlsx")

tabela_escritura = pd.read_excel(CAMINHO_ESCRITURA)
tabela_registro = pd.read_excel(CAMINHO_REGISTRO)


def dec(v):
    return Decimal(str(v))


# ===============================
# BUSCAR ESCRITURA
# ===============================

def buscar_escritura(valor):

    valor = dec(valor)

    for _, linha in tabela_escritura.iterrows():

        limite = dec(linha["ValorVenal"])

        if valor <= limite:
            return dec(linha["ValorEscritura"])

    return dec(tabela_escritura.iloc[-1]["ValorEscritura"])


# ===============================
# BUSCAR REGISTRO
# ===============================

def buscar_registro(valor):

    valor = dec(valor)

    for _, linha in tabela_registro.iterrows():

        limite = dec(linha["ValorVenal"])

        if valor <= limite:

            registro = dec(linha["ValorRegistro"])
            matricula = Decimal("78.01")

            return registro, matricula

    registro = dec(tabela_registro.iloc[-1]["ValorRegistro"])
    matricula = Decimal("78.01")

    return registro, matricula


# ===============================
# IMPOSTO
# ===============================

def calcular_imposto(valor, aliquota):

    valor = dec(valor)
    aliquota = dec(aliquota)

    imposto = valor * (aliquota / Decimal("100"))

    return imposto.quantize(Decimal("0.01"))


# ===============================
# VENDA E COMPRA
# ===============================

def venda_compra(valor, aliquota):

    valor = dec(valor)

    escritura = buscar_escritura(valor)

    registro, matricula = buscar_registro(valor)

    imposto = calcular_imposto(valor, aliquota)

    total = escritura + imposto + registro + matricula

    return {
        "escritura": escritura,
        "imposto": imposto,
        "registro": registro,
        "matricula": matricula,
        "total": total
    }


# ===============================
# VENDA COM DESCONTO
# ===============================

def venda_desconto(valor, aliquota):

    base = venda_compra(valor, aliquota)

    base["escritura"] = base["escritura"] * Decimal("0.60")

    base["total"] = (
        base["escritura"]
        + base["imposto"]
        + base["registro"]
        + base["matricula"]
    )

    return base


# ===============================
# VENDA COM USUFRUTO
# ===============================

def venda_usufruto(valor, aliquota):

    valor = dec(valor)

    base = venda_compra(valor, aliquota)

    base_usufruto = valor / Decimal("3")

    registro_usufruto, _ = buscar_registro(base_usufruto)

    base["registro_usufruto"] = registro_usufruto

    base["total"] = (
        base["escritura"]
        + base["imposto"]
        + base["registro"]
        + base["matricula"]
        + registro_usufruto
    )

    return base

# ===============================
# VENDA + CESSÃO
# ===============================

def venda_cessao(valor, valor_cessao, aliquota):

    valor = dec(valor)
    valor_cessao = dec(valor_cessao)

    # VENDA
    escritura_venda = buscar_escritura(valor)
    registro, matricula = buscar_registro(valor)

    imposto_venda = calcular_imposto(valor, aliquota)

    total_venda = (
        escritura_venda
        + imposto_venda
        + registro
        + matricula
    )

    # CESSÃO
    escritura_cessao = buscar_escritura(valor_cessao) * Decimal("0.60")

    imposto_cessao = calcular_imposto(valor_cessao, aliquota)

    total_cessao = (
        escritura_cessao
        + imposto_cessao
    )

    return {

        "venda": {
            "base": valor,
            "escritura": escritura_venda,
            "imposto": imposto_venda,
            "registro": registro,
            "matricula": matricula,
            "total": total_venda
        },

        "cessao": {
            "base": valor_cessao,
            "escritura": escritura_cessao,
            "imposto": imposto_cessao,
            "total": total_cessao
        }
    }
# ===============================
# ALIENAÇÃO FIDUCIÁRIA
# ===============================

def alienacao_fiduciaria(valor, divida, aliquota):

    valor = dec(valor)
    divida = dec(divida)

    # VENDA
    escritura_venda = buscar_escritura(valor) * Decimal("0.60")

    registro, matricula = buscar_registro(valor)

    imposto = calcular_imposto(valor, aliquota)

    total_venda = (
        escritura_venda
        + imposto
        + registro
        + matricula
    )

    # DÍVIDA
    escritura_divida = buscar_escritura(divida) * Decimal("0.60")

    registro_divida, _ = buscar_registro(divida)

    total_divida = (
        escritura_divida
        + registro_divida
    )

    return {

        "venda": {
            "base": valor,
            "escritura": escritura_venda,
            "imposto": imposto,
            "registro": registro,
            "matricula": matricula,
            "total": total_venda
        },

        "divida": {
            "base": divida,
            "escritura": escritura_divida,
            "registro": registro_divida,
            "total": total_divida
        }
    }

# ===============================
# DOAÇÃO / INVENTÁRIO
# ===============================

def doacao_inventario(valor):

    valor = dec(valor)

    aliquota = Decimal("4")

    escritura = buscar_escritura(valor)

    registro, matricula = buscar_registro(valor)

    imposto = valor * (aliquota / Decimal("100"))

    total = escritura + registro + matricula + imposto

    return {
        "escritura": escritura,
        "registro": registro,
        "matricula": matricula,
        "imposto": imposto,
        "total": total
    }

# ===============================
# DOAÇÃO COM USUFRUTO
# ===============================

def doacao_usufruto(valor):

    valor = dec(valor)

    aliquota = Decimal("4")

    valor_doacao = valor * Decimal("0.6666667")
    valor_usufruto = valor * Decimal("0.3333333")

    escritura_doacao = buscar_escritura(valor_doacao)

    registro_doacao, matricula = buscar_registro(valor_doacao)

    escritura_usufruto = buscar_escritura(valor_usufruto) / Decimal("4")

    registro_usufruto, _ = buscar_registro(valor_usufruto)

    imposto = valor * (aliquota / Decimal("100"))

    total = (
        escritura_doacao
        + registro_doacao
        + matricula
        + escritura_usufruto
        + registro_usufruto
        + imposto
    )

    return {

        "valor_doacao": valor_doacao,
        "valor_usufruto": valor_usufruto,

        "escritura": escritura_doacao,
        "registro": registro_doacao,
        "matricula": matricula,

        "escritura_usufruto": escritura_usufruto,
        "registro_usufruto": registro_usufruto,

        "imposto": imposto,

        "total": total
    }
