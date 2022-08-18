from mesa import batch_run
import pandas as pd
from pd_grid.model import PdGrid
import numpy as np

# inicio do design do experiments

# definição das variáveis dos experimentos
# que serão controladas (valor fixo) ou manipuladas
params = {
    "width": 10,
    "height": 10,
    "cooperation_reward": np.arange(0, 1, 0.25),
    "defected_reward": np.arange(0, 1, 0.25),
    "defection_reward": np.arange(0, 1, 0.25),
    "mutual_defection_reward": np.arange(0, 1, 0.25),
}

# define a quantidade de experimentos
# que serão repetidos para cada configuração de valores
# para as variáveis (de controle e independentes)
experiments_per_parameter_configuration = 50

# quantidade de passos suficientes para que a simulação
# alcance um estado de equilíbrio (steady state)
max_steps_per_simulation = 25

# executa a simulacoes / experimentos, e coleta dados em memória
results = batch_run(
    PdGrid,
    parameters=params,
    iterations=experiments_per_parameter_configuration,
    max_steps=max_steps_per_simulation,
    data_collection_period=-1,
    display_progress=True,
)

# converte os dados das simulações em planilhas (dataframes)
results_df = pd.DataFrame(results)

# gera uma string com data e hora
from datetime import datetime

now = str(datetime.now()).replace(":", "-").replace(" ", "-")

# define um prefixo para o nome do arquivo que vai guardar os dados do modelo
# contendo alguns dados dos experimentos
file_name_suffix = (
    "_iter_"
    + str(experiments_per_parameter_configuration)
    + "_steps_"
    + str(max_steps_per_simulation)
    + "_"
    + now
)

# define um prefixo para o nome para o arquivo de dados
model_name_preffix = "PrisonerDilemma"

# define o nome do arquivo
file_name = model_name_preffix + "_model_data" + file_name_suffix + ".csv"

results_df.to_csv(file_name)
