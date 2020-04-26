import pandas as pd
import os

def merge(input_dir):
    folders = []
    for folder in os.listdir(input_dir):
        folders.append(input_dir + folder)

    csv_files = {}

    for folder in folders:
        for file in os.listdir(folder):
            base = folder + '/'
            if base not in csv_files:
                csv_files[base] = []
            csv_files[base].append(folder + '/' + file)

    for key, value in csv_files.items():
        directory = key.split('/')
        df = pd.read_csv(value[3], index_col=0)


merge("yearly data/")