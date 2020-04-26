import pandas as pd
import os

def extract_FY(input_dir):
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
        df = pd.read_csv(value[0], index_col=0)
        rows = []
        df = df.loc[df['period'] == 'FY']
        df = df.loc[df['figure'] == 'common-outstanding-basic']


        df.to_csv(key + str(directory[1] + '_fy.csv'))


extract_FY('shares_outstanding/')
