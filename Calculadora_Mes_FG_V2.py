import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account # type: ignore
import numpy as np
import matplotlib.pyplot as plt
import time
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima_model import ARMAResults 
from datetime import datetime, timedelta
import seaborn as sns # type: ignore
import db_dtypes

# --------------------------------------------------------------------------------
credentials = service_account.Credentials.from_service_account_file(filename = r"C:\Users\Edward\Downloads\abstract-water-292819-6363adf76099.json", 
                                                                   scopes=["https://www.googleapis.com/auth/cloud-platform"])
# --------------------------------------------------------------------------------
def Q_Joy():
    escolha = 0
    escolha = int(input('Qual categoria analisar:\n[1] JOY; \n[2] Ecohouse; \n[3] Negócio Cocção\n[4] Negócio Cond. Ar; \n[5] Negócio Lavanderia; \n[6] Negócio Microondas\n[7] Negócio Lava Louças; \n[8] Refrigeração; \n[9] Eletroportáteis \n[0] Full\n'))

    if escolha == 1:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2

        --SELECT distinct format_date('%Y',Data_Criacao) as DataCriacao, SUM(Contagem_OS) as OS ,Negocio FROM `abstract-water-292819.teste.teste2` group by Negocio,DataCriacao

        where Negocio = 'Joy'  order by Data_Criacao asc
            '''
    elif escolha == 2:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Ecohouse'  order by Data_Criacao asc
            '''
    elif escolha == 3:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Negócio Cocção'  order by Data_Criacao asc
            '''
    elif escolha == 4:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Negócio Cond. Ar'  order by Data_Criacao asc
            '''
    elif escolha == 5:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Negócio Lavanderia'  order by Data_Criacao asc
            '''
    elif escolha == 6:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Negócio Microondas'  order by Data_Criacao asc
            '''
    elif escolha == 7:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Negócio Lava Louças'  order by Data_Criacao asc
            '''
    elif escolha == 8:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Negócio Refrigeração'  order by Data_Criacao asc
            '''
    elif escolha == 9:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        where Negocio = 'Negócio Eletroportáteis'  order by Data_Criacao asc
            '''
    elif escolha == 0:
        query= '''
        SELECT Data_Criacao, Contagem_OS from abstract-water-292819.teste.teste2
        --where Negocio = 'Joy'  order by Data_Criacao asc
            '''
    return query


#---------------------- GRÁFICO -----------------------------------
#df_mes.plot(figsize=(12,5))
#plt.plot(df.index, df.OS)
#plt.plot(df.index, df.Contagem_OS)
#plt.xlabel('Data')
#plt.ylabel('Contagem de Mensal')
#plt.title('Volume de OS Mensal')
#plt.show()

# ------------------------------- ARIMA ---------------------------
def Arima(df_mes):
    bruteforce_modelo = auto_arima(df_mes,
                                start_p = 0,
                                start_d = 0,
                                start_q = 0,
                                max_p = 8,
                                max_d = 8,
                                max_q = 8,
                                m = 12,
                                start_P = 0,
                                seasonal = True,
                                d = 1,
                                D = 1,
                                trace = True,
                                error_action = 'ignore',
                                suppress_warnings = True,
                                stepwise = False)

    print(f"Resultado AIC: {bruteforce_modelo.aic()}")  #coments se pah
    print(f"Resultado melhores parametros (p,d,q): {bruteforce_modelo.order}\n") #coments se pah

    futuro_forecast = bruteforce_modelo.predict(n_periods=20)
    futuro_forecast.head(7) # isso nao aparece n sei pq
    return bruteforce_modelo

def Datas(): # ISSO É INDEPENDENTE NÃO É PRA BUGAR ---> retorna ultimo dia do mes

    from datetime import datetime, timedelta
    # Definir a data inicial e final    
    data_inicial = datetime(2024, 1, 31)
    data_final = datetime(2025, 9, 30)

# Criar uma lista vazia para armazenar as datas
    datas_ultimo_dia_mes = []

# Definir a data inicial como o primeiro dia do próximo mês
    data_atual = datetime(data_inicial.year, data_inicial.month, 1) + timedelta(days=32)

# Iterar até a data final, adicionando o último dia de cada mês à lista
    while data_atual <= data_final:
        proximo_mes = datetime(data_atual.year, data_atual.month, 1)
        ultimo_dia_mes = proximo_mes - timedelta(days=1)
        datas_ultimo_dia_mes.append(ultimo_dia_mes)
        data_atual = proximo_mes + timedelta(days=32)
   
# Converter as datas em strings formatadas
    datas_ultimo_dia_mes = [datetime.strftime(i, '%Y-%m-%d') for i in datas_ultimo_dia_mes]
    return datas_ultimo_dia_mes   


# ----------------------------- PARTE QUE INTERESSA DA PREVISAO -------------------
#datas_ultimo_dia_mes = Datas()
def Previsao(datas_ultimo_dia_mes):
    futuro_forecast = bruteforce_modelo.predict(n_periods=10)
    futuro_forecast = pd.DataFrame(futuro_forecast,index = datas_ultimo_dia_mes,columns=["Contagem_OS"])
    futuro_forecast.index.name = 'Data_Criacao'
    futuro_forecast.index = pd.to_datetime(futuro_forecast.index)
    futuro_forecast.Contagem_OS = round(futuro_forecast.Contagem_OS,0)
    print(futuro_forecast.head(10).sort_values(by="Data_Criacao", ascending=True))
    final = pd.concat([df_mes,futuro_forecast])
    final.head(2)

# -------------------------------- MAIN? -------------------------------------------

query = Q_Joy()
df = pd.read_gbq(credentials=credentials, query = query, index_col = 'Data_Criacao') 
df.head(5)
print(df.iloc[-1]) 
df.index = pd.to_datetime(df.index)

data_atual = datetime.now()
ultimo_dia_mes_anterior = data_atual.replace(day=1) - timedelta(days=1)
dados_filtrados = df[df.index <= ultimo_dia_mes_anterior]

print(dados_filtrados.iloc[-1])
df_mes = dados_filtrados.groupby(pd.Grouper(freq='M')).sum()
df_mes.head(10)

bruteforce_modelo = Arima(df_mes)
datas_ultimo_dia_mes = Datas()
Previsao(datas_ultimo_dia_mes)