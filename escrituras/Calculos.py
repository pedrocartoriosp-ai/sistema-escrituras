import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

tabela_escritura = pd.read_excel(BASE_DIR / "TabelaEscritura.xlsx")
tabela_registro = pd.read_excel(BASE_DIR / "TabelaRegistro.xlsx")


def buscar_escritura(valor):

    linha = tabela_escritura[tabela_escritura["ValorVenal"] >= valor].iloc[0]

    return float(linha["ValorEscritura"])


def buscar_registro(valor):

    linha = tabela_registro[tabela_registro["ValorVenal"] >= valor].iloc[0]

    registro = float(linha["ValorRegistro"])

    matricula = tabela_registro["Matrícula"].dropna().iloc[0]

    return registro, float(matricula)

def venda_compra(valor_base, aliquota=3.5):

    escritura = buscar_escritura(valor_base)

    registro, matricula = buscar_registro(valor_base)

    itbi = valor_base * (aliquota / 100)

    total = escritura + itbi + registro + matricula

    return {
        "base": valor_base,
        "escritura": escritura,
        "imposto": itbi,
        "registro": registro,
        "matricula": matricula,
        "total": total
    }

def venda_desconto(valor_base, aliquota=3.5):

    resultado = venda_compra(valor_base, aliquota)

    resultado["escritura"] = resultado["escritura"] * 0.6

    resultado["total"] = (
        resultado["escritura"]
        + resultado["imposto"]
        + resultado["registro"]
        + resultado["matricula"]
    )

    return resultado

def venda_usufruto(valor_base, aliquota=3.5):

    venda = venda_compra(valor_base, aliquota)

    base_usufruto = valor_base / 3

    registro_usufruto, _ = buscar_registro(base_usufruto)

    venda["registro_usufruto"] = registro_usufruto

    venda["total"] += registro_usufruto

    return venda

def doacao(valor_base):

    escritura = buscar_escritura(valor_base)

    registro, matricula = buscar_registro(valor_base)

    itcmd = valor_base * 0.04

    total = escritura + itcmd + registro + matricula

    return {
        "base": valor_base,
        "escritura": escritura,
        "imposto": itcmd,
        "registro": registro,
        "matricula": matricula,
        "total": total
    }

