import os
import pandas as pd

def mergeDataFrames(inputDir):
    folders = []
    for folder in os.listdir(inputDir):
        folders.append(inputDir + folder)

    csv_files = {}
    for folder in folders:
        for file in os.listdir(folder):
            base = folder + '/'
            if base not in csv_files:
                csv_files[base] = []
            csv_files[base].append(folder + '/' + file)
    #print(csv_files)

    for key, value in csv_files.items():
        directory = key.split('/')
        #print(directory[1])
        df = pd.read_csv(value[0], index_col=0)
        df2 = pd.read_csv(value[1], index_col=0)
        df3 = pd.read_csv(value[2], index_col=0)
        result = df.append([df2, df3])
        result.set_index('Line Item', inplace=True)
        result = result.fillna(0)
        result.to_csv(key + str(directory[1] + '_merged.csv'))

mergeDataFrames('data/')