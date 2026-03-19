from decimal import Decimal
import pandas as pd
import os
from django.conf import settings

CAMINHO_ESCRITURA = os.path.join(settings.BASE_DIR, "Tabela_Emolumentos.xlsx")
CAMINHO_REGISTRO = os.path.join(settings.BASE_DIR, "TabelaRegistro.xlsx")


# ===============================
# FUNÇÃO DECIMAL SEGURA
# ===============================

def dec(v):

    if pd.isna(v):
        return Decimal("0")

    if isinstance(v, (int, float)):
        return Decimal(str(v))

    try:
        v = str(v)
        v = v.replace("R$", "").strip()

        if "," in v:
            v = v.replace(".", "").replace(",", ".")

        return Decimal(v)

    except:
        print(f"Erro ao converter valor: {v}")
        return Decimal("0")


# ===============================
# CARREGAR TABELA ESCRITURA
# ===============================

def carregar_tabela_escritura():

    df = pd.read_excel(CAMINHO_ESCRITURA)

    df.columns = df.columns.astype(str).str.strip()

    if "ValorVenal" not in df.columns or "TOTAL" not in df.columns:
        raise Exception("❌ Planilha inválida: precisa ter 'ValorVenal' e 'TOTAL'")

    df = df[["ValorVenal", "TOTAL"]].copy()
    df = df.dropna()

    df["ValorVenal"] = df["ValorVenal"].apply(dec)
    df["TOTAL"] = df["TOTAL"].apply(dec)

    df = df.sort_values(by="ValorVenal")

    return df


tabela_escritura = carregar_tabela_escritura()


# ===============================
# BUSCAR ESCRITURA
# ===============================

def buscar_escritura(valor):

    valor = dec(valor)

    for _, linha in tabela_escritura.iterrows():
        if valor <= linha["ValorVenal"]:
            return linha["TOTAL"]

    return tabela_escritura.iloc[-1]["TOTAL"]


# ===============================
# REGISTRO
# ===============================

tabela_registro = pd.read_excel(CAMINHO_REGISTRO)


def buscar_registro(valor):

    valor = dec(valor)

    for _, linha in tabela_registro.iterrows():

        limite = dec(linha["ValorVenal"])

        if valor <= limite:
            return dec(linha["ValorRegistro"]), Decimal("78.01")

    return dec(tabela_registro.iloc[-1]["ValorRegistro"]), Decimal("78.01")


# ===============================
# IMPOSTO (CORRIGIDO)
# ===============================

def calcular_imposto(valor, aliquota):

    valor = dec(valor)
    aliquota = dec(aliquota)

    # sem tributação
    if aliquota == 0:
        return Decimal("0.00")

    return (valor * (aliquota / Decimal("100"))).quantize(Decimal("0.01"))


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

    base["escritura"] *= Decimal("0.60")

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

    base = venda_compra(valor, aliquota)

    base_usufruto = dec(valor) / Decimal("3")

    registro_usufruto, _ = buscar_registro(base_usufruto)

    base["registro_usufruto"] = registro_usufruto
    base["total"] += registro_usufruto

    return base


# ===============================
# VENDA + CESSÃO
# ===============================

def venda_cessao(valor, valor_cessao, aliquota):

    venda = venda_compra(valor, aliquota)

    valor_cessao = dec(valor_cessao)

    escritura_cessao = buscar_escritura(valor_cessao) * Decimal("0.60")
    imposto_cessao = calcular_imposto(valor_cessao, aliquota)

    total_cessao = escritura_cessao + imposto_cessao

    return {
        "venda": venda,
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

    venda = venda_compra(valor, aliquota)

    divida = dec(divida)

    escritura_divida = buscar_escritura(divida) * Decimal("0.60")
    registro_divida, _ = buscar_registro(divida)

    total_divida = escritura_divida + registro_divida

    return {
        "venda": venda,
        "divida": {
            "base": divida,
            "escritura": escritura_divida,
            "registro": registro_divida,
            "total": total_divida
        }
    }


# ===============================
# DOAÇÃO / INVENTÁRIO (CORRIGIDO)
# ===============================

def doacao_inventario(valor, aliquota):

    valor = dec(valor)

    # regra: se não for zero, usa 4%
    if dec(aliquota) != 0:
        aliquota = Decimal("4")

    escritura = buscar_escritura(valor)
    registro, matricula = buscar_registro(valor)

    imposto = calcular_imposto(valor, aliquota)

    total = escritura + registro + matricula + imposto

    return {
        "escritura": escritura,
        "registro": registro,
        "matricula": matricula,
        "imposto": imposto,
        "total": total
    }


# ===============================
# DOAÇÃO COM USUFRUTO (CORRIGIDO)
# ===============================

def doacao_usufruto(valor, aliquota):

    valor = dec(valor)

    # regra ITCMD
    if dec(aliquota) != 0:
        aliquota = Decimal("4")

    valor_doacao = valor * Decimal("0.6666667")
    valor_usufruto = valor * Decimal("0.3333333")

    escritura = buscar_escritura(valor_doacao)
    registro, matricula = buscar_registro(valor_doacao)

    escritura_usufruto = buscar_escritura(valor_usufruto) / Decimal("4")
    registro_usufruto, _ = buscar_registro(valor_usufruto)

    imposto = calcular_imposto(valor, aliquota)

    total = (
        escritura
        + registro
        + matricula
        + escritura_usufruto
        + registro_usufruto
        + imposto
    )

    return {
        "escritura": escritura,
        "registro": registro,
        "matricula": matricula,
        "escritura_usufruto": escritura_usufruto,
        "registro_usufruto": registro_usufruto,
        "imposto": imposto,
        "total": total
    }