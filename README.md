# Projeto Aplicado — Análise de Dados da ANEEL

Repositório oficial do Projeto Aplicado desenvolvido para a disciplina, utilizando dados abertos da **Agência Nacional de Energia Elétrica (ANEEL)**.

> ✅ **Status atual: Etapa 3 concluída.** Este projeto é desenvolvido em múltiplas etapas ao longo do semestre. O conteúdo deste repositório é atualizado progressivamente conforme novas fases são entregues.

---

## 📌 Sobre o projeto

Este projeto tem como objetivo analisar dados públicos do setor elétrico brasileiro, disponibilizados pela ANEEL, com foco na evolução da matriz de geração de energia e na participação de fontes renováveis.

- **Empresa/Organização:** Agência Nacional de Energia Elétrica (ANEEL)
- **Dataset:** [SIGA — Sistema de Informações de Geração da ANEEL](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel)
- **ODS relacionada:** ODS 7 – Energia limpa e acessível *(principal)* e ODS 13 – Ação contra a mudança global do clima *(secundária)*

### Perguntas norteadoras

1. Como está distribuída a matriz de geração de energia elétrica do Brasil por tipo de fonte?
2. Qual é a tendência de crescimento das fontes renováveis (eólica e solar) em relação às fontes convencionais ao longo do tempo?
3. Como a participação de cada fonte varia entre os estados, e existe concentração geográfica de fontes específicas?

---

## 🗂️ Sobre o dataset

O **SIGA (Sistema de Informações de Geração da ANEEL)** reúne o cadastro dos empreendimentos de geração de energia elétrica do Brasil (hidrelétricas, eólicas, solares, termelétricas etc.), com informações como fonte de energia, potência instalada, localização, fase do empreendimento e data de entrada em operação.

- **Versão utilizada:** baixada em outubro de 2026 (mantida "congelada" em `data/` para reprodutibilidade)
- **Tamanho:** 25.045 registros × 23 colunas
- **Sensibilidade:** dados públicos de empreendimentos (pessoa jurídica), sem dados pessoais sensíveis

📎 Fonte oficial: [dadosabertos.aneel.gov.br](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel)

---

## 🧭 Etapas do projeto

| Etapa | Entrega | Documento |
|---|---|---|
| Etapa 1 | Proposta: empresa, contexto do estudo, objetivos, ODS e metadados | [relatorio_etapa1_proposta.pdf](docs/relatorio_etapa1_proposta.pdf) |
| Etapa 2 | Relatório consolidado (Etapas 1 + 2): glossário, dicionário de dados, análise exploratória (EDA) e cronograma | [relatorio_etapa1_etapa2_mackenzie.pdf](docs/relatorio_etapa1_etapa2_mackenzie.pdf) |
| Etapa 3 | Storytelling com dados: cinco indicadores visuais e propostas de ação para a ANEEL | [relatorio_etapa3_mackenzie.pdf](docs/relatorio_etapa3_mackenzie.pdf) |

---

## 📊 Principais resultados até aqui

- **Matriz majoritariamente renovável:** 90,6% das usinas e 84,7% da potência instalada vêm de fontes renováveis.
- **Quantidade ≠ potência:** a fonte solar soma 75,7% das usinas cadastradas (18.962), mas o potencial hidráulico concentra cerca de 110.000 MW, quase metade da potência fiscalizada do país.
- **Concentração geográfica:** o Pará reúne 13.204 registros (52,7% do total), quase todos de pequenas usinas solares, ponto que a equipe propõe auditar.
- **Expansão em ondas:** a potência que entra em operação cresce de forma acentuada a partir de 2010, com picos ligados a projetos eólicos e solares.
- **Outliers estruturais:** pela regra do IQR, 22,4% das usinas aparecem como outliers, reflexo da mistura entre sistemas muito pequenos e grandes hidrelétricas, e não de erros na base.

---

## 📁 Estrutura do repositório

```
PROJETO_APLICADO_GRUPO_7_MACKENZIE/
├── data/
│   └── siga-empreendimentos-geracao.csv     # dataset SIGA (versão de out/2026)
├── docs/
│   ├── relatorio_etapa1_proposta.pdf        # Etapa 1
│   ├── relatorio_etapa1_etapa2_mackenzie.pdf # Etapas 1 + 2
│   └── relatorio_etapa3_mackenzie.pdf       # Etapa 3
├── src/
│   ├── eda_siga.py                          # script de análise exploratória
│   └── graficos/                            # gráficos gerados (PNG)
└── README.md
```

---

## ▶️ Como reproduzir a análise

**Pré-requisitos:** Python 3.10+ e as bibliotecas `pandas`, `numpy`, `matplotlib` e `seaborn`.

```bash
# 1. Clonar o repositório
git clone https://github.com/Fiaschiii/PROJETO_APLICADO_GRUPO_7_MACKENZIE.git
cd PROJETO_APLICADO_GRUPO_7_MACKENZIE

# 2. Instalar as dependências
pip install pandas numpy matplotlib seaborn

# 3. Executar o script a partir da pasta src/
cd src
python eda_siga.py
```

O script imprime as estatísticas descritivas no terminal e salva os seis gráficos em `src/graficos/`.

---

## 🛠️ Tecnologias

- **Python** (pandas, numpy) para tratamento e análise dos dados
- **matplotlib** e **seaborn** para visualização
- **Git/GitHub** para versionamento do código, dos dados e dos relatórios

---

## 👥 Equipe

| Nome | RA | Email |
|---|---|---|
| Lavínia Lara Pereira Sousa   | 10780727 | 10780727@mackenzista.com.br |
| Miguel Fiaschi Silva         | 10776936 | 10776936@mackenzista.com.br |
| Matheus Faganelli            | 10782660 | 10782660@mackenzista.com.br |
| Cláudio Basta Neto           | 10764325 | 10764325@mackenzista.com.br |

---

## 🎓 Disciplina

Projeto desenvolvido como parte da disciplina de **Projeto Aplicado I** — Banco de Dados - UPM.
