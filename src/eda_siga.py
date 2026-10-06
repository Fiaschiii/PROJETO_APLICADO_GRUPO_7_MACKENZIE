"""
Análise Exploratória de Dados (EDA) — SIGA / ANEEL
Projeto Aplicado — Etapa 2

Dataset: siga-empreendimentos-geracao.csv
Fonte: https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel

Este script:
1. Carrega e trata o dataset (conversão de tipos, datas, decimais)
2. Produz estatísticas descritivas (shape, tipos, medidas de posição/dispersão)
3. Analisa distribuição e frequência por fonte de energia e UF
4. Calcula correlações entre variáveis numéricas
5. Identifica valores nulos/ausentes
6. Identifica outliers (potência instalada)
7. Gera gráficos (salvos em /outputs)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

CSV_PATH = "siga-empreendimentos-geracao.csv"  # ajuste o caminho conforme a pasta /data do repositório
OUTPUT_DIR = "./graficos"  # ajuste para a pasta de saída desejada (ex: "./graficos")


# 1. CARGA E TRATAMENTO DOS DADOS

df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")

# Conversão de colunas numéricas (formato brasileiro: vírgula decimal)
for col in ["MdaPotenciaOutorgadaKw", "MdaPotenciaFiscalizadaKw", "MdaGarantiaFisicaKw",
            "NumCoordNEmpreendimento", "NumCoordEEmpreendimento"]:
    df[col] = (
        df[col].astype(str)
        .str.replace(".", "", regex=False)   # remove separador de milhar, se houver
        .str.replace(",", ".", regex=False)  # vírgula decimal -> ponto
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Conversão de datas
for col in ["DatEntradaOperacao", "DatGeracaoConjuntoDados", "DatInicioVigencia", "DatFimVigencia"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Ano de entrada em operação (para análises temporais)
df["AnoEntradaOperacao"] = df["DatEntradaOperacao"].dt.year

# Classificação renovável x não renovável (abstração sugerida no problema de estudo)
# Categorias conforme valores reais da coluna DscFonteCombustivel no SIGA
FONTES_RENOVAVEIS = [
    "Radiação solar", "Cinética do vento", "Potencial hidráulico",
    "Agroindustriais", "Floresta", "Resíduos sólidos urbanos",
    "Resíduos animais", "Biocombustíveis líquidos",
]
df["ClasseFonte"] = np.where(
    df["DscFonteCombustivel"].isin(FONTES_RENOVAVEIS), "Renovável", "Não renovável"
)

print("=" * 70)
print("1. SHAPE E TIPOS DE DADOS")
print("=" * 70)
print(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}")
print()
print(df.dtypes)


# 2. VALORES NULOS / AUSENTES

print("\n" + "=" * 70)
print("2. VALORES NULOS POR COLUNA")
print("=" * 70)
nulos = df.isnull().sum()
nulos_pct = (nulos / len(df) * 100).round(1)
print(pd.DataFrame({"nulos": nulos, "pct": nulos_pct}).query("nulos > 0"))

# 3. MEDIDAS DE POSIÇÃO E DISPERSÃO

print("\n" + "=" * 70)
print("3. ESTATÍSTICA DESCRITIVA — POTÊNCIA FISCALIZADA (kW)")
print("=" * 70)
print(df["MdaPotenciaFiscalizadaKw"].describe())
print(f"\nModa: {df['MdaPotenciaFiscalizadaKw'].mode().iloc[0]}")
print(f"Variância: {df['MdaPotenciaFiscalizadaKw'].var():.2f}")
print(f"Coeficiente de variação: {df['MdaPotenciaFiscalizadaKw'].std() / df['MdaPotenciaFiscalizadaKw'].mean():.2f}")


# 4. DISTRIBUIÇÃO E FREQUÊNCIA

print("\n" + "=" * 70)
print("4. DISTRIBUIÇÃO POR FONTE DE ENERGIA")
print("=" * 70)
freq_fonte = df["DscFonteCombustivel"].value_counts()
print(freq_fonte)

print("\n" + "=" * 70)
print("5. DISTRIBUIÇÃO POR UF (TOP 10)")
print("=" * 70)
print(df["SigUFPrincipal"].value_counts().head(10))

print("\n" + "=" * 70)
print("5b. DISTRIBUIÇÃO POR TIPO DE GERAÇÃO (SigTipoGeracao)")
print("=" * 70)
print(df["SigTipoGeracao"].value_counts())

print("\n" + "=" * 70)
print("6. DISTRIBUIÇÃO POR FASE DO EMPREENDIMENTO")
print("=" * 70)
print(df["DscFaseUsina"].value_counts())

print("\n" + "=" * 70)
print("7. RENOVÁVEL x NÃO RENOVÁVEL (quantidade e potência total)")
print("=" * 70)
print(df.groupby("ClasseFonte").agg(
    qtd_usinas=("CodCEG", "count"),
    potencia_total_mw=("MdaPotenciaFiscalizadaKw", lambda x: x.sum() / 1000)
).round(1))


# 5. CORRELAÇÕES

print("\n" + "=" * 70)
print("8. CORRELAÇÃO ENTRE VARIÁVEIS NUMÉRICAS")
print("=" * 70)
num_cols = ["MdaPotenciaOutorgadaKw", "MdaPotenciaFiscalizadaKw", "MdaGarantiaFisicaKw"]
print(df[num_cols].corr().round(3))


# 6. OUTLIERS (regra do IQR sobre potência fiscalizada)

print("\n" + "=" * 70)
print("9. OUTLIERS — POTÊNCIA FISCALIZADA (regra IQR)")
print("=" * 70)
q1 = df["MdaPotenciaFiscalizadaKw"].quantile(0.25)
q3 = df["MdaPotenciaFiscalizadaKw"].quantile(0.75)
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr
outliers = df[df["MdaPotenciaFiscalizadaKw"] > limite_superior]
print(f"Q1={q1:.0f} kW | Q3={q3:.0f} kW | IQR={iqr:.0f} kW | Limite superior={limite_superior:.0f} kW")
print(f"Quantidade de outliers: {len(outliers)} ({len(outliers)/len(df)*100:.1f}% do dataset)")
print("\nTop 5 maiores usinas (outliers extremos):")
print(outliers.nlargest(5, "MdaPotenciaFiscalizadaKw")[
    ["NomEmpreendimento", "SigUFPrincipal", "DscFonteCombustivel", "MdaPotenciaFiscalizadaKw"]
])


# GRÁFICOS


# Gráfico 1 — Quantidade de usinas por fonte de energia
plt.figure(figsize=(9, 5))
freq_fonte.plot(kind="barh", color="#1a3c5e")
plt.title("Quantidade de Usinas por Fonte de Energia — SIGA/ANEEL")
plt.xlabel("Número de usinas")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_usinas_por_fonte.png", dpi=150)
plt.close()

# Gráfico 2 — Potência total instalada por fonte (MW)
pot_fonte = df.groupby("DscFonteCombustivel")["MdaPotenciaFiscalizadaKw"].sum().sort_values() / 1000
plt.figure(figsize=(9, 5))
pot_fonte.plot(kind="barh", color="#8c1d3c")
plt.title("Potência Fiscalizada Total por Fonte de Energia (MW)")
plt.xlabel("Potência total (MW)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_potencia_por_fonte.png", dpi=150)
plt.close()

# Gráfico 3 — Top 10 UFs por número de usinas
plt.figure(figsize=(9, 5))
df["SigUFPrincipal"].value_counts().head(10).sort_values().plot(kind="barh", color="#2e7d32")
plt.title("Top 10 Estados (UF) por Número de Usinas")
plt.xlabel("Número de usinas")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_top10_uf.png", dpi=150)
plt.close()

# Gráfico 4 — Evolução temporal (entrada em operação) por classe de fonte
evolucao = (
    df[(df["AnoEntradaOperacao"] >= 1990) & (df["AnoEntradaOperacao"] <= 2026)]
    .groupby(["AnoEntradaOperacao", "ClasseFonte"])["MdaPotenciaFiscalizadaKw"]
    .sum().unstack(fill_value=0) / 1000
)
plt.figure(figsize=(11, 5))
evolucao.plot(kind="area", stacked=True, ax=plt.gca(), color=["#c62828", "#2e7d32"])
plt.title("Evolução da Potência Instalada por Ano de Entrada em Operação (1990–2026)")
plt.xlabel("Ano de entrada em operação")
plt.ylabel("Potência (MW)")
plt.legend(title="Classe da fonte")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_evolucao_temporal.png", dpi=150)
plt.close()

# Gráfico 5 — Boxplot de potência por classe de fonte (visualização de outliers)
plt.figure(figsize=(8, 5))
df_plot = df[df["MdaPotenciaFiscalizadaKw"] > 0].copy()
df_plot["MdaPotenciaFiscalizadaKw_log"] = np.log10(df_plot["MdaPotenciaFiscalizadaKw"])
sns.boxplot(data=df_plot, x="ClasseFonte", y="MdaPotenciaFiscalizadaKw_log", palette=["#2e7d32", "#c62828"])
plt.title("Distribuição da Potência Fiscalizada por Classe de Fonte (escala log10)")
plt.ylabel("log10(Potência fiscalizada em kW)")
plt.xlabel("")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_boxplot_outliers.png", dpi=150)
plt.close()

# Gráfico 6 — Mapa de correlação
plt.figure(figsize=(6, 5))
sns.heatmap(df[num_cols].corr(), annot=True, cmap="RdBu_r", center=0, fmt=".2f")
plt.title("Correlação entre Variáveis de Potência")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_correlacao.png", dpi=150)
plt.close()

print("\nGráficos salvos em:", OUTPUT_DIR)
print("Análise concluída.")
