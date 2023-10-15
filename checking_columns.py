from finding_headers import headers
from utils.basic_functions import *
import pandas as pd
from io import StringIO


# headers = ['auto_agendamento', 'bairro', 'categoria', 'cep', 'cid', 'cnes_exe', 'cnes_sol', 'cns', 'cod_mun_res', 'cod_mun_sol', 'cod_procedimento_sisreg', 'cod_sigtap', 'cod_solicitacao', 'cod_vaga_sol', 'complemento', 'cpf_exe', 'cpf_sol', 'data_aut', 'data_exe', 'data_nasc', 'data_sol', 'dias_de_espera_exe', 'dias_espera_exe', 'ds_exe', 'ds_sol', 'grupo_procedimento', 'hora_exe', 'idade_anos', 'idade_meses', 'logradouro', 'mae', 'municipio_res', 'municipio_sol', 'numero', 'operador_aut', 'operador_sol', 'procedimento_sisreg', 'profissional_exe', 'profissional_sol', 'qtd', 'rede_exe', 'rede_sol', 'sexo', 'status_exe', 'sub_categoria', 'subtipo_acesso', 'tel', 'tipo_acesso', 'tipo_logradouro', 'tipo_vaga', 'unid_exe', 'unid_sol', 'unidade_exe', 'unidade_sol', 'usuario', 'valor_proced']

directory_to_read = "finalJsonFiles"

files_to_read = get_files_to_read(directory_to_read, ".jsonl")

print("length: ", len(files_to_read))

for filename in files_to_read:
    print('reading file: ', filename)

    # ! Read the .jsonl file and get the first line
    with open(os.path.join(directory_to_read, filename), "r") as file:
        first_line = next(file)

    # ! Parse the first line as JSON and create a DataFrame
    df = pd.read_json(StringIO(first_line), lines=True)

    # ! Iterate through the columns and convert possible Unix timestamps to dates
    columns = [column for column in df.columns]
    if columns == headers:
        print(f"{filename} has all {len(headers)} headers")
    else:
        print(f"the number of columns: {len(columns)}")