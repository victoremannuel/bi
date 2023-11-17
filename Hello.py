# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
subprocess.run(["pip", "install", "plotly"])

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
        layout="wide"
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    # st.markdown(
        
    # )
    # st.set_page_config(layout="wide") #comando para usar a pagina toda

    #-----------------------------
    #TRATAMENTO DE DADOS
    df = pd.read_csv("dados.csv", sep=";", decimal=",") #lendo o arquivo csv
    df["Date"] = pd.to_datetime(df["Date"]) #convertendo a colina Date para formato de data
    df = df.sort_values("Date") #ordenando por data
    df["Mês"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month)) #criando uma coluna mes para concatenar mes e ano extraindo da coluna date original usando a lambida, uma funcao de uma linha so

    #-----------------------------
    #MENU LATERAL
    #filtros
    mouth = st.sidebar.selectbox("Mês", df["Mês"].unique())
    df_filtrado = df[df["Mês"] == mouth]

    #-----------------------------
    #LAYOUT
    caixa1, caixa2 = st.columns(2)
    caixa3, caixa4, caixa5 = st.columns(3)

    #-----------------------------
    #GRÁFICOS
    grafico_data_faturamento = px.bar(df_filtrado, x="Date", y="Total", color="City", title="Faturamento do mês")

    grafico_data_produto = px.bar(df_filtrado, x="Date", y="Product line", color="City", orientation="h", title="Faturamento por tipo de produto")

    total_cidade = df_filtrado.groupby("City")[["Total"]].sum().reset_index()
    grafico_volume_cidade = px.bar(total_cidade, x="City", y="Total", title="Faturamento por filial")

    grafico_tipo_pagamento = px.pie(df_filtrado, values="Total", names="Payment", title="Faturamento por tipo de pagamento")

    ranking = df_filtrado.groupby("City")[["Rating"]].mean().reset_index()
    grafico_ranking_cidade = px.bar(ranking, x="City", y="Rating", title="Avaliação")

    #-----------------------------
    #IMPRIMINDO
    caixa1.plotly_chart(grafico_data_faturamento, use_container_width=True)
    caixa2.plotly_chart(grafico_data_produto, use_container_width=True)
    caixa3.plotly_chart(grafico_volume_cidade, use_container_width=True)
    caixa4.plotly_chart(grafico_tipo_pagamento, use_container_width=True)
    caixa5.plotly_chart(grafico_ranking_cidade, use_container_width=True)


if __name__ == "__main__":
    run()
