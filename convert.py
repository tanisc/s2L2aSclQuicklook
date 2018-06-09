import os, sys
from osgeo import gdal,osr
import pyproj
import numpy as np
import mahotas as mh
from datetime import datetime
flistr = []
dlistr = []
flistt = os.listdir(sys.argv[1])
for f in flistt:
        try:
            if ("S2A_USER_PRD_MSIL2A_PDMC_" in f or "S2A_MSIL2A_" in f) and ".SAFE" in f:
                if "S2A_USER_PRD_MSIL2A_PDMC_" in f:
                    fname = os.path.join(sys.argv[1],f,f.replace("S2A_USER_PRD_MSIL2A_PDMC_","S2A_USER_MTD_SAFL2A_PDMC_").replace(".SAFE",".xml"))
                    dt = datetime.strptime(os.path.split(fname)[1][47:62],"%Y%m%dT%H%M%S")
                    orbit = f[40:46]
                if "S2A_MSIL2A_" in f:
                    orbit = f[32:45]
                    fname = os.path.join(sys.argv[1],f,'GRANULE')
                    for g in os.listdir(fname):
                        if "L2A_" in g:
                            fname = os.path.join(fname,g,'IMG_DATA')
                            break
                    for g in ['R10m','R20m','R60m']:
                        for h in os.listdir(os.path.join(fname,g)):
                            if "SCL" in h:
                                fname = os.path.join(fname,g,h)
                                break
                        if "SCL" in fname:
                            break
                    dt = datetime.strptime(os.path.split(f)[1][11:26],"%Y%m%dT%H%M%S")
                if os.path.isfile(fname):
                    flistr.append(fname)
                    dlistr.append(dt)
        except:
            pass

for j,fname in enumerate(flistr):
    try:
        date = dlistr[j]
        lat = []
        lon = []
        data = []
        ds_safe = None
        if os.path.splitext(fname)[1] == '.jp2':
            sds = [fname]
            bandid = 1
        else:
            ds_safe = gdal.Open(fname)
            sds = []
            for i,s in enumerate(ds_safe.GetSubDatasets()):
                if "SCL" in s[1]:
                    sds.append(s[0])
            bandid = 14
        for i,s in enumerate(sds):
            gtif = gdal.Open(s)
            raster = gtif.GetRasterBand(bandid)
            raster = np.array(raster.ReadAsArray())
            gtif = None

        ds_safe = None
        snow = raster == 11
        nosnow = (raster == 5) + (raster == 4)
        img = np.dstack((snow.astype('uint8'),nosnow.astype('uint8'),(snow*0).astype('uint8')))
        raster = raster.astype('uint8')
        mh.imsave(os.path.join(sys.argv[1],date.strftime('%Y%m%dT%H%M%S')+orbit+'SCL.png'),raster*20)
        mh.imsave(os.path.join(sys.argv[1],date.strftime('%Y%m%dT%H%M%S')+orbit+'SNS.png'),img*255)
    except:
        print 'Cannot read/write for ',
        print date.strftime('%Y%m%dT%H%M%S'+orbit)
        pass
