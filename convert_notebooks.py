import json

def convert(nb_path, py_path):
    with open(nb_path, 'r') as f:
        nb = json.load(f)
    with open(py_path, 'w') as f:
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                for line in cell.get('source', []):
                    # ignore pip installs and shell commands
                    if not line.strip().startswith('!'):
                        f.write(line)
                f.write('\n\n')

convert('DataSetForABCXRecords.ipynb', 'step1_extract_data.py')
convert('Preprocessing_and_Feature_Extraction.ipynb', 'step2_preprocess.py')
convert('ML_model_Building.ipynb', 'step3_train.py')
print("Conversion done.")
