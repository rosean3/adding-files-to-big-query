import os
import csv
import openpyxl
from openpyxl.utils import get_column_letter

python_file_name = 'teste.py'

# Get the current directory
current_directory = os.getcwd()

# List all files in the current directory
files_in_directory = os.listdir(current_directory)

# Filter the list to include only files (not directories)
files_to_read = [file for file in files_in_directory if os.path.isfile(file) if file.endswith(".py") != python_file_name]

# filename = files_to_read[1]

def determine_delimiter(filename):
    """Determine the delimiter based on the number of semicolons in the first 100 lines."""
    with open(filename, 'r', newline='') as file:
        lines = [file.readline().strip() for _ in range(100)]
        count_semicolons = sum(line.count(';') for line in lines)
        return ',' if count_semicolons < 200 else ';'
    
def classify_string(input_str):
    # Check for date with "-" format
    if len(input_str) == 8 and (input_str[2] == '-' or input_str[2] == '/'):
        try:
            if input_str[2] == '-':
                return "Date with -"
            else:
                return "Date with /"
        except ValueError:
            return "Non-Numeric"

    # Check for integer
    try:
        int_value = int(input_str)
        return "Integer"
    except ValueError:
        try:
            float_value = float(input_str)
            return "Float"
        except ValueError:
            return "Non-Numeric"

def decide_new_value(old_value, new_value):
    # Check if either value is "Non-Numeric," and if so, return "Non-Numeric"
    if old_value == "Non-Numeric" or new_value == "Non-Numeric":
        return "Non-Numeric"
    
    if old_value == "Both types of dates":
        return "Both types of dates"

    # Check if the new value is a date with "-" and the old one is a date with "/"
    # or vice-versa, and return "both types of dates" in that case
    elif (old_value == "Date with -" and new_value == "Date with /") or (old_value == "Date with /" and new_value == "Date with -"):
        return "Both types of dates"

    # Check if the old value is an integer and the new value is a float,
    # and return "Float" in that case
    elif old_value == "Integer" and new_value == "Float":
        return "Float"
    
    elif old_value == "Float" and new_value == "Integer":
        return "Float"

    # If none of the above conditions are met, return the new value
    else:
        return new_value

files_to_read[files_to_read.index('originais_sisreg_agendamento_202101.xlsx')] = files_to_read[0]
files_to_read[0] = 'originais_sisreg_agendamento_202101.xlsx'

print("files to read: ", files_to_read)

headers = []
iterations = 0
filename = files_to_read[0]

print(f"filename: {filename}")

all_headers = ['data_exe', 'data_aut', 'data_sol', 'municipio_sol', 'rede_sol', 'ds_sol', 'cnes_sol', 'unid_sol', 'cod_mun_res', 'rede_exe', 'ds_exe', 'cnes_exe', 'unid_exe', 'categoria', 'sub_categoria', 'grupo_procedimento', 'procedimento_sisreg', 'cod_sigtap', 'profissional_exe', 'status_exe', 'tipo_vaga', 'dias_espera_exe', 'operador_sol', 'operador_aut', 'tipo_acesso', 'subtipo_acesso', 'qtd', 'auto_agendamento', ' dias_espera_exe', 'cod_solicitacao', 'cod_procedimento_sisreg', 'cpf_exe', 'hora_exe', 'cns', 'usuario', 'data_nasc', 'idade_anos', 'idade_meses', 'mae', 'tipo_logradouro', 'logradouro', 'complemento', 'numero', 'bairro', 'cep', 'tel', 'municipio_res', 'cod_mun_sol', 'unidade_sol', 'sexo', 'valor_proced', 'cid', 'cpf_sol', 'profissional_sol', 'unidade_exe', 'dias_de_espera_exe', 'cod_vaga_sol']
all_headers.sort()

is_numeric_dict = {header: "" for header in all_headers}

keeping_track = {}

for filename in files_to_read:
    if filename.endswith(".xlsx"):
        
        print(f"reading {filename}")
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active  # Assuming you're reading the first sheet

        file_headers = []
        for cell in sheet[1]:  # 1 refers to the first row
            file_headers.append(cell.value)

        if not headers:
            headers = file_headers
        else:
            new_headers = [header for header in file_headers if header not in headers]
            if new_headers:
                keeping_track[filename] = new_headers
                headers = headers + new_headers

headers.sort()
print("headers: ", headers)
print("keeping track: ", keeping_track)

# [] vê os que são prioritários de serem tipados como algo sem ser string
# [] como trata ,

# ! [] como trata valor vazio
# ! [] 

# [] gerar um arquivo que 