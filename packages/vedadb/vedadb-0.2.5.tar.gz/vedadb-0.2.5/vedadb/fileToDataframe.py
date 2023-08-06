__all__ = ['filetodataframe']
import sys
import os
import pandas as pd


def vdeToDataframe(myvde):
    # def readToDataframe(myfile):
    dimension=[]
    region=[]
    codset=[]
    description=[]
    with open(myvde) as f:
        for line in f:
            line=line.split(",")
            dimension.append(line[0].split('"')[1])
            region.append(line[1].split('"')[1])
            codset.append(line[2].split('"')[1])
            description.append(line[3].split('"')[1])
            # print(line)
    df = pd.DataFrame({'dimension':dimension,
        'region':region,'codset':codset,'description':description})
    return df
    

def vdsToDataframe(myvde):
    # def readToDataframe(myfile):
    dimension=[]
    region=[]
    codset=[]
    dimensionCode=[]
    with open(myvde) as f:
        for line in f:
            line=line.split(",")
            dimension.append(line[0].split('"')[1])
            region.append(line[1].split('"')[1])
            codset.append(line[2].split('"')[1])
            dimensionCode.append(line[3].split('"')[1])
            # print(line)
    df = pd.DataFrame({'dimension':dimension,
        'region':region,'codset':codset,'dimensionCode':dimensionCode})
    return df

if __name__ == '__main__':
    myfile = sys.argv[1]
    # df=vdeToDataframe(myfile)
    df=vdsToDataframe(myfile)
    print(df)