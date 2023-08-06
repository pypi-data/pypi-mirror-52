__all__ = ['endpoint']
import os
import sys

def create(myvdfile,myvdefile,myvdsfile):
    os.system("python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/entete.py" + 
    " " + "VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json" + " " + myvdfile)

    os.system("python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/sets.py" + 
    " " + "VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json" + " " + myvdefile)
    
    os.system("python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/dimensionContent.py" + 
    " " + "VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json" + " " + myvdefile + " " + myvdsfile)
    os.system("python3 VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/resultat.py" + 
    " " + "VEDA/takatel-veda-api/takatel-veda-db/vedadb/vedadb/connectParameters.json" + " " + myvdfile)

# if __name__ == "__main__":
#     create("connectParameters.json","/home/archange/VEDA/base/DemoS_012.VD","/home/archange/VEDA/base/DemoS_012.VDE","/home/archange/VEDA/base/DemoS_012.VDS")