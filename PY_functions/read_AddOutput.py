"""
This function look, read AddOutput_1h.prn
Returning {ID:temperature}
"""
import os

ModelPath = "c:\\Users\\vhoang\\Desktop\\LizardSurfTemp\\TRNLizard_Files\\Model\\" #this will be an input from GH component in the future
Variant = "BASIS2" #this will be an input from GH component in the future
AddOutputPath = os.path.join(ModelPath,Variant,"Results\\AddOutput_1h.prn")

def readSurfaceTemp(AddOutputPath):
    """Read in AddOutput_1h.prn
    Return a dictionary {surfacename:[hourly values]}"""
    if not os.path.isfile(AddOutputPath):
        print("AddOutput_1h.prn file not found! Please check if you have surface temperature connected!")
        pass
    else:
        SurfTempF = open(AddOutputPath,'r')
        SurfTempLines = SurfTempF.readlines()
        #take first line to get surface name and ID
        firstline = SurfTempLines[0].split()
        srfname, srfID = [], []
        SurfaceTemperature = dict() #{srfname:[hourly surface temperature]}
        for item in firstline:
            itemname = item.split("_")[-1]
            srfname.append(itemname)
            srfID.append(int(item.split("S")[-1]))
            SurfaceTemperature[itemname] = [] #empty list later to store hourly temperature
        SurfTempLines.pop(0)
        SurfTempLines.pop(0)
        hour = []
        for line in SurfTempLines:
            line = line.split()
            try:
                hour.append(float(line[0]))
                line.pop(0)
                for id,values in enumerate(line):
                    SurfaceTemperature[srfname[id]].append(float(values))
            except:
                break
        SurfTempF.close()
        return SurfaceTemperature

SurfaceTemperature = readSurfaceTemp(AddOutputPath)
#print(SurfaceTemperature)
