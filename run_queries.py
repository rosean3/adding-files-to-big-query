from google.cloud import bigquery
from google.oauth2 import service_account
import json
from utils.basic_functions import *
from utils.constants import *

# TODO(developer): Set key_path to the path to the service account key
#                  file.
key_path = "absens-348513-7177e845c80d.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

directory_to_read = "xlsxFiles"

files_to_read = get_files_to_read(directory_to_read, "xlsx")
files_to_read.sort()

results = []

for i in range(1, 4):
    for j in range(1, 13):
        if i == 3 and j > 6:
            break

        query = """
            SELECT COUNT(*) AS result FROM `absens-348513.absenteismo.historico` WHERE EXTRACT(YEAR FROM data_exe) = 202{} AND EXTRACT(MONTH FROM data_exe) = {}
        """.format(i, j)

        query_job = client.query(query)

        for row in query_job:
            result = row["result"]
            # print(f"result of query 202{i}-{j}: {result}")

        results.append(result)

dictionary = {filename: result for filename, result in zip(files_to_read, results)}

# print("dictionary: ", dictionary)

if dictionary == NUMBER_OF_LINES:
    print("They are equal")