__all__ = ['entete']
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import vedadb.connexion as connexion

def writeEnteteInDb(db,line):
    db.insert('entete', importidveda=line["ImportID"],gdx2vedaversion=line["GDX2VEDAversion"],
    vedaflavor=line["VEDAFlavor"],dimensions=line["Dimensions"],
    parentdimensions=line["ParentDimensions"],setallowed=line["SetsAllowed"],fieldsize=line["FieldSize"],
    notindexed=line["NotIndexed"],defaultvaluedim=line["DefaultValueDim"],fieldseparator=line["FieldSeparator"],textdelim=line["TextDelim"])

def readAndWriteEntete(myfile):
    vd_file = open(myfile,'r')
    x=0
    result = {}
    while (x<12):
        if x == 0:
            line = vd_file.readline()
            resultline=line.split("GDX2VEDAversion-")[1].strip()
            keyline=line.split("-")[0].split("*")[1].strip()
            # in python 3
            result.update({keyline: resultline})
        else:
 
            # read line
            line = vd_file.readline()
            
            keyline=line.split("-")[0].split("*")[1].strip()
            resultline=line.split("-")[1].strip()
            # in python 3
            result.update({keyline: resultline})

        # check if line is not empty
        if not line:
            break
        x=x+1
    return result
    vd_file.close()

#Read importId from db entete table
def readImportIdFromDb(db):
        
        for r in db.query(  # just for example
                "SELECT importid FROM entete ORDER BY importid DESC LIMIT 1"
                ).dictresult():
                result=r['importid'] 
        return result
                # print(r['idset'])
def execution(parameters_path,myvdfile):
    r=connexion.connect(parameters_path)
    writeEnteteInDb(r,readAndWriteEntete(myvdfile))

if __name__ == '__main__':
    parameters_path = sys.argv[1]
    myvdfile = sys.argv[2]
    # t=readAndWriteEntete(myfile)
    # print(t["ImportID"])

    r=connexion.connect(parameters_path)
 
    writeEnteteInDb(r,readAndWriteEntete(myvdfile))

    # d=readImportIdFromDb(r)
    # print(d)
