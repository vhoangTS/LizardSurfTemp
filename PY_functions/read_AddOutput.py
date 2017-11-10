"""
This function look, read AddOutput_1h.prn
Returning {ID:temperature}
"""
import os
import re

#ModelPath = "c:\\Users\\vhoang\\Desktop\\LizardSurfTemp\\TRNLizard_Files\\Model\\" #this will be an input from GH component in the future
ModelPath = "C:\\Users\\Vu Hoang\\Desktop\\LizardSurfTemp\\TRNLizard_Files\\Model\\"
Variant = "BASIS2" #this will be an input from GH component in the future
AddOutputPath = os.path.join(ModelPath,Variant,"Results\\AddOutput_1h.prn")
b18path = os.path.join(ModelPath,Variant,"%s.b18"%Variant)

TimeStep = 1

def readSurfaceTemp(AddOutputPath,TimeStep):
    """Read in AddOutput_1h.prn
    Return a dictionary {surfacename:[hourly values]}
    Sorted based on surface ID, lower to higher"""
    if not os.path.isfile(AddOutputPath):
        print("AddOutput_1h.prn file not found! Please check if you have surface temperature connected as additional output!")
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
            itemid = int(item.split("_S")[-1])
            srfname.append(itemname)
            srfID.append(itemid)
            SurfaceTemperature[itemid] = [] #empty list later to store hourly temperature
        SurfTempLines.pop(0)
        SurfTempLines.pop(0)
        hour = []
        for line in SurfTempLines:
            line = line.split()
            try:
                hour.append(float(line[0]))
                line.pop(0)
                for id,values in enumerate(line):
                    SurfaceTemperature[srfID[id]].append(float(values))
            except:
                break
        SurfTempF.close()
        #now get all the temperature at timestep
        SrfTempAtTimeStep = []
        for key in sorted(SurfaceTemperature.keys()):
            SrfTempAtTimeStep.append(SurfaceTemperature[key][TimeStep-1]) #sorted smaller id to higher id
        return SurfaceTemperature, SrfTempAtTimeStep

def getDataParagraph(startpattern,stoppattern,datararray):
    """by Mark Sen Dong for TRNLizard b18 geometry visualization
    Get paragraph between start and stop pattern"""
    output = []
    inparagraph = 'FALSE'
    lines=datararray
    for i in range(len(lines)):
        search_start=re.search(r'{0}'.format(startpattern),lines[i])
        if search_start is not None or inparagraph == 'TRUE':
            inparagraph = 'TRUE'
            lines[i] = lines[i].split('\n')[0]
            if lines[i].startswith('*'):
                pass
            else:
                output.append(lines[i])
            search_stop=re.search(r'{0}'.format(stoppattern),lines[i])
            if search_stop is not None:
                return output
                pass

def readSurfaceGeo(b18path):
    """Read b18 building file
    Return surface and vertices, as well as construction"""
    if not os.path.isfile(b18path):
        print("b18 building file not found! Please check!")
        pass
    else:
        b18file = open(b18path,"r")
        b18data = b18file.readlines()
        srfGeoBlock = getDataParagraph("_EXTENSION_BuildingGeometry_START_", "_EXTENSION_BuildingGeometry_END_", b18data)
        #now get vertex's coordinate xyz
        vertexdict = dict() #{vertexID:[x,y,z]}
        srfbasicinfo = dict() #{surfaceID:[vertexID]}
        srfInfo = dict() #{surfaceID:[vertices coordinate]}
        for line in srfGeoBlock:
            dline = line.split()
            if "vertex" in dline:
                vertexdict[int(dline[1])] = [float(xyz) for xyz in dline[2:]] #{vertexID:[x,y,z]}
            if "wall" in dline or "window" in dline or "floor" in dline or "ceiling" in dline or "roof" in dline:
                srfbasicinfo[int(dline[1])] = [[int(nrID) for nrID in dline[2:]],dline[0]] #{surfaceID:[[vertexID],construction]}
                #print srfbasicinfo[int(dline[1])]
        for key in srfbasicinfo.keys():
            srfInfo[key] = []
            for vertices in srfbasicinfo[key][0]:
                srfInfo[key].append(vertexdict[vertices])
        b18file.close()
        return srfInfo,vertexdict,srfbasicinfo
        #actually only need srfInfo
        #just getting everything out for now, incase will need to use those

SrfTempAll, SrfTempTimeStep = readSurfaceTemp(AddOutputPath, TimeStep)
srfInfo, vertexdict, srfbasicinfo = readSurfaceGeo(b18path)
print(srfInfo)
print(srfbasicinfo)
