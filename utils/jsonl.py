import json

def rename_column_in_jsonl(input_file, output_file):
    count = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        print("reading file: ", input_file)
        for line in infile:
            data = json.loads(line)
            if " dias_espera_exe" in data:
                # Rename the column
                if count == 0:
                    print("data[ dias_espera_exe]: ", data["  dias_espera_exe"])
                data["dias_espera_exe"] = data.pop(" dias_espera_exe")
                if count == 0:
                    print("data[dias_espera_exe]: ", data["dias_espera_exe"])
            
            count += 1
            outfile.write(json.dumps(data) + '\n')